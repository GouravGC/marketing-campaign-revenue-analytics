SELECT
  COUNT(*) AS total_rows,
  COUNTIF(event_name = 'purchase') AS purchase_events,
  SUM(IF(
    event_name = 'purchase',
    COALESCE(purchase_revenue_usd, 0),
    0
  )) AS purchase_revenue_usd
FROM `lofty-equinox-511206-k3.marketing_analytics.raw_ga4_events`;