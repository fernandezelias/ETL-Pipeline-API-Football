# ⚽ Football Data ETL Pipeline (API-Football)

🌐 Available in: [Español](README.md)

This **Data Engineering** project implements an automated **ETL pipeline** for ingesting, transforming, and storing data from the **API-Football**.  
The goal is to build a scalable, reproducible data architecture organized into layers (Bronze, Silver, Gold).

---

## 🧰 Tech Stack
- **Language:** Python 3.11  
- **Distributed processing:** PySpark  
- **Orchestration:** Prefect 3.x  
- **Storage:** Local Data Lake (Bronze/Silver/Gold folders)  
- **Version control:** Git / GitHub  
- **Visualization:** Matplotlib and Seaborn

---

## 🧩 Pipeline structure

1. **Ingestion (Bronze Layer)**  
   - Incremental extraction from the API-Football (`countries`, `leagues`, `fixtures` endpoints).  
   - Raw data stored in `.json` or `.parquet` formats.  

2. **Transformation (Silver Layer)**  
   - Cleaning and normalization of columns.  
   - Data type conversions and name standardization.  
   - Enrichment with derived variables (e.g., `total_goals`, `match_winner`).  

3. **Curation and analytics (Gold Layer)**  
   - Consolidation of datasets ready for analysis and visualization.  
   - Computation of performance metrics (average goals, home/away splits, etc.).  
   - Final exports to `.csv` or `.parquet` formats.

---

## ⚙️ General workflow

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

Each stage of the process is modular and can be executed independently via Prefect.  

---

## 📊 Key results
- Reproducible and scalable pipeline with **incremental date-based processing**.  
- Integration between **Spark and Prefect** for local orchestration.  
- Clean datasets ready for exploratory visualizations (goal Poisson distribution, home/away patterns, etc.).

---

## 🧠 Conclusion
This project demonstrates practical **Data Engineering** principles, combining best practices in data architecture and workflow automation.  
Its modular structure enables future migration to cloud environments (e.g., **Google Cloud Storage** or **Databricks**).

---

## ✍️ Author
**Elías Fernández**  
📧 Contact: [fernandezelias86@gmail.com](mailto:fernandezelias86@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/eliasfernandez208)

---

📁 **Repository:** ETL_API_Football  