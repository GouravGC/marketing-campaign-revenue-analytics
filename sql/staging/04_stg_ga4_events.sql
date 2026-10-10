CREATE OR REPLACE TABLE
  `lofty-equinox-511206-k3.marketing_analytics.stg_ga4_events` AS
SELECT
  event_date,
  LOWER(TRIM(event_name)) AS event_name,
  CAST(user_pseudo_id AS STRING) AS user_pseudo_id,
  COALESCE(NULLIF(TRIM(traffic_source), ''), 'unknown') AS traffic_source,
  COALESCE(NULLIF(TRIM(traffic_medium), ''), 'unknown') AS traffic_medium,
  COALESCE(NULLIF(TRIM(device_category), ''), 'unknown') AS device_category,
  COALESCE(NULLIF(TRIM(country), ''), 'unknown') AS country,
  SAFE_CAST(purchase_revenue_usd AS NUMERIC) AS purchase_revenue_usd,
  event_name = 'purchase' AS is_purchase,
  CASE
    WHEN event_name = 'purchase'
      THEN GREATEST(
        COALESCE(SAFE_CAST(purchase_revenue_usd AS NUMERIC), NUMERIC '0'),
        NUMERIC '0'
      )
    ELSE NUMERIC '0'
  END AS revenue_for_analytics_usd
FROM `lofty-equinox-511206-k3.marketing_analytics.raw_ga4_events`;