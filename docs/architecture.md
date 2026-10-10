# Architecture

Google Analytics 4 public BigQuery sample
→ CSV extract
→ Python ingestion and validation
→ cleaned staging dataset
→ daily, event, and traffic-source marts
→ Excel reconciliation and Power BI reporting

The local pipeline is runnable without cloud credentials. The SQL files document the intended BigQuery transformation layer and use placeholder project/dataset names until a destination table is configured.
