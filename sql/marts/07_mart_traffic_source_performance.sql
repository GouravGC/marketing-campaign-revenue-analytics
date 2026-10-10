
CREATE OR REPLACE TABLE
  `lofty-equinox-511206-k3.marketing_analytics.mart_traffic_source_performance` AS
SELECT
  traffic_source,
  traffic_medium,
  event_name,
  COUNT(*) AS event_count,
  COUNT(DISTINCT user_pseudo_id) AS unique_users,
  SUM(revenue_for_analytics_usd) AS purchase_revenue_usd
FROM
  `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`
GROUP BY
  traffic_source,
  traffic_medium,
  event_name;
