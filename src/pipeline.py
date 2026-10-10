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
