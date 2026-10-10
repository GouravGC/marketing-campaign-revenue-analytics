
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FILES = {
    "src/config.py": r'''
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "csv" / "ga4_ecommerce_events.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports" / "generated"
LOG_DIR = ROOT / "reports" / "logs"
''',
    "src/pipeline.py": r'''
import logging
from pathlib import Path
import pandas as pd

from src.config import RAW_DATA, PROCESSED_DIR, REPORTS_DIR, LOG_DIR

LOG_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "event_date", "event_name", "user_pseudo_id", "traffic_source",
    "traffic_medium", "device_category", "country", "purchase_revenue_usd",
]
VALID_EVENTS = {
    "session_start", "page_view", "add_to_cart", "begin_checkout", "purchase"
}


def load_data(path=RAW_DATA):
    if not Path(path).exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")
    df = pd.read_csv(path)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    logger.info("Loaded %s rows from %s", len(df), path)
    return df


def transform_data(df):
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df["event_name"] = df["event_name"].astype("string").str.strip().str.lower()
    df["user_pseudo_id"] = df["user_pseudo_id"].astype("string").str.strip()
    for col in ["traffic_source", "traffic_medium", "device_category", "country"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA).fillna("unknown")
    df["purchase_revenue_usd"] = pd.to_numeric(
        df["purchase_revenue_usd"], errors="coerce"
    )
    # Missing revenue is expected for non-purchase events. Do not turn it into
    # zero in the event-level output; retain nulls for transparent semantics.
    invalid_revenue = df["purchase_revenue_usd"].lt(0).fillna(False)
    df.loc[invalid_revenue, "purchase_revenue_usd"] = pd.NA
    df["is_purchase"] = df["event_name"].eq("purchase")
    df["revenue_for_analytics_usd"] = df["purchase_revenue_usd"].where(
        df["is_purchase"], 0
    ).fillna(0)
    df["event_date"] = df["event_date"].dt.date
    return df


def validate_data(df):
    checks = {
        "row_count_positive": len(df) > 0,
        "required_columns_present": set(REQUIRED_COLUMNS).issubset(df.columns),
        "event_dates_valid": df["event_date"].notna().all(),
        "event_names_valid": df["event_name"].isin(VALID_EVENTS).all(),
        "user_ids_present": df["user_pseudo_id"].notna().all(),
        "revenue_nonnegative": (
            df["purchase_revenue_usd"].dropna().ge(0).all()
        ),
        "nonpurchase_revenue_null": (
            df.loc[~df["is_purchase"], "purchase_revenue_usd"].isna().all()
        ),
    }
    result = pd.DataFrame(
        [{"check_name": name, "passed": bool(passed)}
         for name, passed in checks.items()]
    )
    return result


def build_marts(df):
    daily = (
        df.groupby(["event_date", "event_name"], dropna=False)
        .agg(
            event_count=("event_name", "size"),
            unique_users=("user_pseudo_id", "nunique"),
            purchase_revenue_usd=("revenue_for_analytics_usd", "sum"),
        )
        .reset_index()
    )
    traffic = (
        df.groupby(["traffic_source", "traffic_medium", "event_name"], dropna=False)
        .agg(
            event_count=("event_name", "size"),
            unique_users=("user_pseudo_id", "nunique"),
            purchase_revenue_usd=("revenue_for_analytics_usd", "sum"),
        )
        .reset_index()
    )
    funnel = (
        df.groupby("event_name")
        .agg(
            event_count=("event_name", "size"),
            unique_users=("user_pseudo_id", "nunique"),
            purchase_revenue_usd=("revenue_for_analytics_usd", "sum"),
        )
        .reset_index()
    )
    return {
        "stg_ga4_events.csv": df,
        "mart_daily_event_performance.csv": daily,
        "mart_traffic_source_performance.csv": traffic,
        "mart_event_summary.csv": funnel,
    }


def run_pipeline():
    logger.info("Pipeline started")
    raw = load_data()
    cleaned = transform_data(raw)
    checks = validate_data(cleaned)
    checks.to_csv(REPORTS_DIR / "data_quality_results.csv", index=False)
    if not checks["passed"].all():
        failed = checks.loc[~checks["passed"], "check_name"].tolist()
        raise ValueError(f"Data quality checks failed: {failed}")
    for filename, output in build_marts(cleaned).items():
        output.to_csv(PROCESSED_DIR / filename, index=False)
        logger.info("Wrote %s rows to %s", len(output), filename)
    # Duplicate profiling is reported, not automatically deduplicated:
    # repeated event rows may be legitimate.
    duplicate_count = int(raw.duplicated().sum())
    (REPORTS_DIR / "duplicate_profile.txt").write_text(
        f"Exact duplicate rows across selected columns: {duplicate_count}\n"
        "Rows were retained because the available extract lacks a unique event ID.\n",
        encoding="utf-8",
    )
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
''',
    "tests/test_pipeline.py": r'''
import pandas as pd
import pytest

from src.pipeline import transform_data, validate_data, build_marts


@pytest.fixture
def sample():
    return pd.DataFrame({
        "event_date": ["2021-01-01", "2021-01-01", "2021-01-02"],
        "event_name": ["page_view", "purchase", "add_to_cart"],
        "user_pseudo_id": ["u1", "u1", "u2"],
        "traffic_source": ["google", "google", None],
        "traffic_medium": ["organic", "organic", None],
        "device_category": ["mobile", "mobile", "desktop"],
        "country": ["India", "India", "India"],
        "purchase_revenue_usd": [None, 25.0, None],
    })


def test_transform_preserves_rows_and_marks_purchases(sample):
    result = transform_data(sample)
    assert len(result) == 3
    assert result["is_purchase"].sum() == 1
    assert result.loc[result["event_name"] == "page_view",
                      "purchase_revenue_usd"].isna().all()


def test_missing_dimensions_are_standardized(sample):
    result = transform_data(sample)
    assert result.loc[2, "traffic_source"] == "unknown"
    assert result.loc[2, "traffic_medium"] == "unknown"


def test_quality_checks_pass_for_valid_data(sample):
    result = validate_data(transform_data(sample))
    assert result["passed"].all()


def test_negative_purchase_revenue_is_not_retained(sample):
    sample.loc[1, "purchase_revenue_usd"] = -5
    result = transform_data(sample)
    assert pd.isna(result.loc[1, "purchase_revenue_usd"])


def test_marts_are_generated(sample):
    result = build_marts(transform_data(sample))
    assert "mart_daily_event_performance.csv" in result
    assert "mart_traffic_source_performance.csv" in result
    assert "mart_event_summary.csv" in result
''',
    "sql/staging/stg_ga4_events.sql": r'''
-- Staging model for the local GA4 extract.
-- For BigQuery execution, replace the source table with your uploaded table.
SELECT
  SAFE_CAST(event_date AS DATE) AS event_date,
  LOWER(TRIM(event_name)) AS event_name,
  CAST(user_pseudo_id AS STRING) AS user_pseudo_id,
  COALESCE(NULLIF(TRIM(traffic_source), ''), 'unknown') AS traffic_source,
  COALESCE(NULLIF(TRIM(traffic_medium), ''), 'unknown') AS traffic_medium,
  COALESCE(NULLIF(TRIM(device_category), ''), 'unknown') AS device_category,
  COALESCE(NULLIF(TRIM(country), ''), 'unknown') AS country,
  SAFE_CAST(purchase_revenue_usd AS NUMERIC) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.ga4_ecommerce_events`
''',
    "sql/intermediate/int_event_metrics.sql": r'''
SELECT
  event_date,
  event_name,
  traffic_source,
  traffic_medium,
  device_category,
  country,
  COUNT(*) AS event_count,
  COUNT(DISTINCT user_pseudo_id) AS unique_users,
  SUM(IF(event_name = 'purchase',
         COALESCE(purchase_revenue_usd, 0), 0)) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.stg_ga4_events`
GROUP BY 1, 2, 3, 4, 5, 6
''',
    "sql/marts/mart_daily_performance.sql": r'''
SELECT
  event_date,
  event_name,
  SUM(event_count) AS event_count,
  SUM(purchase_revenue_usd) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.int_event_metrics`
GROUP BY 1, 2
''',
    "sql/marts/mart_traffic_source_performance.sql": r'''
SELECT
  traffic_source,
  traffic_medium,
  event_name,
  SUM(event_count) AS event_count,
  SUM(purchase_revenue_usd) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.int_event_metrics`
GROUP BY 1, 2, 3
''',
    ".github/workflows/ci.yml": r'''
name: Analytics Pipeline CI
on:
  push:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest tests -v
''',
    "docs/data_dictionary.md": r'''
# Data Dictionary

| Column | Meaning | Handling |
|---|---|---|
| event_date | GA4 event date | Parsed as date |
| event_name | Interaction type | Standardized to lowercase |
| user_pseudo_id | Pseudonymous GA4 user identifier | Stored as string |
| traffic_source | GA4 traffic source | Missing/blank becomes `unknown` |
| traffic_medium | GA4 traffic medium | Missing/blank becomes `unknown` |
| device_category | Device category | Missing/blank becomes `unknown` |
| country | Event country | Missing/blank becomes `unknown` |
| purchase_revenue_usd | Purchase revenue in USD | Null for non-purchase events is expected |

## Limitations
- This is a 10,000-row stratified sample with up to 2,000 rows per selected event type.
- Event counts and funnel ratios are sample-based and are not population estimates.
- The extract does not include advertising spend, so ROAS cannot be calculated.
- The available columns do not contain a unique event identifier; exact duplicates are profiled, not automatically removed.
''',
    "docs/architecture.md": r'''
# Architecture

Google Analytics 4 public BigQuery sample
→ CSV extract
→ Python ingestion and validation
→ cleaned staging dataset
→ daily, event, and traffic-source marts
→ Excel reconciliation and Power BI reporting

The local pipeline is runnable without cloud credentials. The SQL files document the intended BigQuery transformation layer and use placeholder project/dataset names until a destination table is configured.
''',
    "src/cleaning/__init__.py": "",
    "src/validation/__init__.py": "",
    "src/ingestion/__init__.py": "",
}


def main():
    created = []
    for relative_path, content in FILES.items():
        target = ROOT / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.lstrip("\n"), encoding="utf-8")
        created.append(relative_path)
    print(f"Created/updated {len(created)} project files:")
    for item in created:
        print(f"  {item}")
    print("\nNext: python -m src.pipeline")


if __name__ == "__main__":
    main()
