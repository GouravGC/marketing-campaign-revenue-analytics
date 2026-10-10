
CREATE OR REPLACE TABLE
  `lofty-equinox-511206-k3.marketing_analytics.mart_daily_event_ranking` AS

WITH daily_metrics AS (
  SELECT
    event_date,
    event_name,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_pseudo_id) AS unique_users,
    SUM(revenue_for_analytics_usd) AS purchase_revenue_usd
  FROM
    `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`
  GROUP BY
    event_date,
    event_name
)

SELECT
  event_date,
  event_name,
  event_count,
  unique_users,
  purchase_revenue_usd,

  ROW_NUMBER() OVER (
    PARTITION BY event_date
    ORDER BY event_count DESC, event_name
  ) AS daily_event_row_number,

  RANK() OVER (
    PARTITION BY event_date
    ORDER BY event_count DESC
  ) AS daily_event_rank

FROM daily_metrics;
