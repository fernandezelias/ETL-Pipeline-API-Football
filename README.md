# ⚽ ETL Pipeline de Datos de Fútbol (API-Football)

🌐 Available in: [English](README_EN.md)

Proyecto de **Ingeniería de Datos** que implementa un pipeline **ETL automatizado** para la ingesta, transformación y almacenamiento de datos provenientes de la **API-Football**.  
El objetivo es construir una arquitectura de datos reproducible, escalable y organizada en distintas capas (Bronze, Silver, Gold).

---

## 🧰 Stack Tecnológico
- **Lenguaje:** Python 3.11  
- **Procesamiento distribuido:** PySpark  
- **Orquestación:** Prefect 3.x  
- **Almacenamiento:** Data Lake local estructurado (carpetas Bronze/Silver/Gold)  
- **Versionado y control:** Git / GitHub  
- **Visualización:** Matplotlib y Seaborn

---

## 🧩 Estructura del pipeline

1. **Ingesta (Bronze Layer)**  
   - Extracción incremental desde la API-Football (endpoints: `countries`, `leagues`, `fixtures`).  
   - Guardado de archivos crudos en formato `.json` o `.parquet`.  

2. **Transformación (Silver Layer)**  
   - Limpieza y normalización de columnas.  
   - Conversión de tipos de datos y estandarización de nombres.  
   - Enriquecimiento de datos con variables derivadas (por ejemplo, `total_goals`, `match_winner`).  

3. **Curación y análisis (Gold Layer)**  
   - Consolidación de datasets listos para análisis y visualización.  
   - Cálculo de métricas de rendimiento (promedios de goles, distribución home/away, etc.).  
   - Exportación final a formatos `.csv` o `.parquet`.

---

## ⚙️ Flujo general

```bash
etl_api_football/
│
├── bronze/
│   └── api_raw_data/
├── silver/
│   └── api_cleaned/
├── gold/
│   └── api_curated/
├── exports/
└── src/
    ├── etl_fixtures.py
    ├── etl_utils.py
    └── prefect_flow.py
```

Cada etapa del proceso es modular y puede ejecutarse de forma independiente mediante Prefect.  

---

## 📊 Resultados principales
- Pipeline reproducible y escalable con **procesamiento incremental** por fecha.  
- Integración entre **Spark y Prefect** para automatización local.  
- Datasets listos para visualizaciones y análisis exploratorio (Poisson de goles, distribución local/visitante, etc.).

---

## 🧠 Conclusión
Este proyecto muestra la aplicación práctica de principios de **Data Engineering**, combinando buenas prácticas de arquitectura de datos y orquestación de procesos.  
La estructura modular permite su extensión futura hacia plataformas cloud (por ejemplo, **Google Cloud Storage** o **Databricks**).

---

## ✍️ Autor
**Elías Fernández**  
📧 Contacto: [fernandezelias86@gmail.com](mailto:fernandezelias86@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/eliasfernandez208)

---

📁 **Repositorio:** ETL_API_Football  