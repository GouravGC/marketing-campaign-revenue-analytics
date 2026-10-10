CREATE OR REPLACE TABLE
  `lofty-equinox-511206-k3.marketing_analytics.int_event_metrics` AS
SELECT
  event_date,
  event_name,
  traffic_source,
  traffic_medium,
  device_category,
  country,
  COUNT(*) AS event_count,
  COUNT(DISTINCT user_pseudo_id) AS unique_users,
  SUM(revenue_for_analytics_usd) AS purchase_revenue_usd
FROM
  `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`
GROUP BY
  event_date,
  event_name,
  traffic_source,
  traffic_medium,
  device_category,
  country;