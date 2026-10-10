SELECT
  traffic_source,
  traffic_medium,
  event_name,
  SUM(event_count) AS event_count,
  SUM(purchase_revenue_usd) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.int_event_metrics`
GROUP BY 1, 2, 3
