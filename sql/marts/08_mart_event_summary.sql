
CREATE OR REPLACE TABLE
  `lofty-equinox-511206-k3.marketing_analytics.mart_event_summary` AS

WITH event_metrics AS (
  SELECT
    event_name,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_pseudo_id) AS unique_users
  FROM
    `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`
  GROUP BY
    event_name
),

revenue_metrics AS (
  SELECT
    event_name,
    SUM(revenue_for_analytics_usd) AS purchase_revenue_usd
  FROM
    `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`
  WHERE
    is_purchase = TRUE
  GROUP BY
    event_name
)

SELECT
  e.event_name,
  e.event_count,
  e.unique_users,
  COALESCE(r.purchase_revenue_usd, 0) AS purchase_revenue_usd
FROM event_metrics AS e
LEFT JOIN revenue_metrics AS r
  ON e.event_name = r.event_name;
