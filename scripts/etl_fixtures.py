# ==========================================================
# etl_fixtures.py — Orquestación ETL para API-Football
# ==========================================================

# --- Librerías estándar ---
import os
from datetime import datetime, timedelta
from configparser import ConfigParser

# --- Librerías externas ---
import requests
import pandas as pd

# --- Prefect ---
from prefect import task, flow
from prefect.runtime import flow_run

# --- Módulos propios ---
from etl_utils import (
    save_new_data_as_delta,
    read_most_recent_partition,
    read_all_from_delta,
    rename_fixture_id,
    normalize_score_cols_to_float,
    add_event_date_from_fixture_date,
    standardize_column_names,
    format_datetime_columns,
    drop_irrelevant_cols,
    add_match_winner,
    add_total_goals,
    cast_column_types,
    cast_gold_categoricals,
    ensure_event_date_utc,
)

# ==========================================================
# Configuración
# ==========================================================

parser = ConfigParser()
parser.read("pipeline.conf")
BASE_URL = parser["api-credentials"]["base_url"]
API_KEY  = parser["api-credentials"]["api_key"]

# --- Paths del Data Lake ---
DATALAKE_ROOT   = "data/etl_datalake"
BRONZE_FIXTURES = f"{DATALAKE_ROOT}/bronze/api_football/fixtures"
SILVER_FIXTURES = f"{DATALAKE_ROOT}/silver/api_football/fixtures"
GOLD_FIXTURES   = f"{DATALAKE_ROOT}/gold/api_football/fixtures"
EXPORTS_DIR     = f"{DATALAKE_ROOT}/exports"


# ==========================================================
# Tasks
# ==========================================================

@task(
    retries=3,
    retry_delay_seconds=60,
    task_run_name="extract-api-football-{endpoint}"
)
def task_extract(endpoint: str, params: dict = None) -> list:
    """Extrae datos crudos desde el endpoint indicado de API-Football."""
    url = f"{BASE_URL}/{endpoint}"

    response = requests.get(
        url,
        headers={"x-apisports-key": API_KEY},
        params=params,
        timeout=30
    )
    response.raise_for_status()

    return response.json()["response"]


@task(task_run_name="transform-bronze")
def task_transform_bronze(raw_data: list) -> pd.DataFrame:
    """Transformación inicial del JSON → DataFrame normalizado."""
    df = pd.json_normalize(raw_data)
    df = rename_fixture_id(df)
    return df


@task(task_run_name="load-bronze-{endpoint_name}")
def task_load_bronze(df: pd.DataFrame, endpoint_name: str):
    """Guarda datos en Bronze (MERGE + partición por event_date)."""
    scheduled_run = flow_run.scheduled_start_time.strftime("%Y-%m-%dT%H:%M")

    # Normalización mínima
    df = normalize_score_cols_to_float(df)
    df = add_event_date_from_fixture_date(df)

    bronze_path = f"{DATALAKE_ROOT}/bronze/api_football/{endpoint_name}"
    os.makedirs(bronze_path, exist_ok=True)

    save_new_data_as_delta(
        df,
        bronze_path,
        predicate="target.fixture_id = source.fixture_id",
        partition_cols=["event_date"],
    )

    print(f"📥 Bronze actualizado para {endpoint_name} ({scheduled_run})")


@task(task_run_name="transform-silver-{endpoint_name}")
def task_transform_silver(endpoint_name: str) -> pd.DataFrame:
    """Procesa los datos persistidos en Bronze → Silver."""
    df_bronze = read_most_recent_partition(BRONZE_FIXTURES)

    df = df_bronze.copy()
    df = standardize_column_names(df)
    df = format_datetime_columns(df)
    df = drop_irrelevant_cols(df)
    df = add_match_winner(df)
    df = add_total_goals(df)
    df = cast_column_types(df)

    # Normalización temporal
    df = add_event_date_from_fixture_date(df)
    df["event_date"] = pd.to_datetime(df["event_date"]).dt.strftime("%Y-%m-%d")

    os.makedirs(SILVER_FIXTURES, exist_ok=True)

    save_new_data_as_delta(
        df,
        SILVER_FIXTURES,
        predicate="target.fixture_id = source.fixture_id",
        partition_cols=["event_date"],
    )

    return df


@task(task_run_name="transform-gold-{endpoint_name}")
def task_transform_gold(endpoint_name: str) -> pd.DataFrame:
    """Genera la tabla Gold desde todos los datos de Silver."""
    df_silver_all = read_all_from_delta(SILVER_FIXTURES).copy()

    df_silver_all = cast_column_types(df_silver_all)
    df_silver_all = cast_gold_categoricals(df_silver_all)
    df_silver_all = ensure_event_date_utc(df_silver_all)

    df_gold = df_silver_all[[
        "fixture_id", "event_date", "league_id", "league_name",
        "teams_home_name", "teams_away_name",
        "goals_home", "goals_away", "match_winner",
    ]].copy()

    df_gold["event_date"] = pd.to_datetime(df_gold["event_date"]).dt.strftime("%Y-%m-%d")

    os.makedirs(GOLD_FIXTURES, exist_ok=True)

    save_new_data_as_delta(
        df_gold,
        GOLD_FIXTURES,
        predicate="target.fixture_id = source.fixture_id",
        partition_cols=["event_date"],
    )

    return df_gold


# ==========================================================
# Flow
# ==========================================================

@flow(name="etl-api-football")
def etl_api_football(endpoints: list):
    """Flow maestro para procesar uno o más endpoints de API-Football."""
    for endpoint in endpoints:

        # 1. Cálculo dinámico de parámetros (solo fixtures)
        params = None
        if endpoint == "fixtures":
            fecha_ayer = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
            params = {"date": fecha_ayer, "timezone": "UTC"}

        # 2. Extracción
        raw = task_extract(endpoint, params=params)

        # 3. Transformación Bronze
        df_bronze = task_transform_bronze(raw)

        # 4. Guardado Bronze
        task_load_bronze(df_bronze, endpoint)

        # 5. Transformación Silver
        task_transform_silver(endpoint)

        # 6. Transformación Gold
        task_transform_gold(endpoint)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    # Opción A — ejecución manual (una sola vez)
    etl_api_football(endpoints=["fixtures"])

    # Opción B — ejecución programada (DESACTIVADA)
    # etl_api_football.serve(
    #     name="ETL-API-Football",
    #     endpoints=["fixtures"],
    #     cron="0 6 * * *"   # todos los días a las 06:00 UTC
    # )