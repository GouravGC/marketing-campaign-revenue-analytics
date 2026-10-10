
SELECT
  'raw' AS layer,
  COUNT(*) AS total_rows,
  COUNTIF(event_name = 'purchase') AS purchase_events
FROM
  `lofty-equinox-511206-k3.marketing_analytics.raw_ga4_events`

UNION ALL

SELECT
  'staging' AS layer,
  COUNT(*) AS total_rows,
  COUNTIF(is_purchase = TRUE) AS purchase_events
FROM
  `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`;



SELECT
  COUNTIF(event_date IS NULL) AS null_dates,
  COUNTIF(event_name IS NULL OR event_name = '') AS missing_event_names,
  COUNTIF(revenue_for_analytics_usd < 0) AS negative_revenue_rows
FROM
  `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events`;



SELECT
  'daily_performance' AS mart,
  COUNT(*) AS total_rows
FROM
  `lofty-equinox-511206-k3.marketing_analytics.mart_daily_performance`

UNION ALL

SELECT
  'traffic_source_performance' AS mart,
  COUNT(*) AS total_rows
FROM
  `lofty-equinox-511206-k3.marketing_analytics.mart_traffic_source_performance`

UNION ALL

SELECT
  'event_summary' AS mart,
  COUNT(*) AS total_rows
FROM
  `lofty-equinox-511206-k3.marketing_analytics.mart_event_summary`

UNION ALL

SELECT
  'daily_event_ranking' AS mart,
  COUNT(*) AS total_rows
FROM
  `lofty-equinox-511206-k3.marketing_analytics.mart_daily_event_ranking`;
