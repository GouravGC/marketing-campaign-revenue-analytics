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
