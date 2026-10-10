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
