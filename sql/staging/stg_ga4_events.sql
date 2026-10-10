-- Staging model for the local GA4 extract.
-- For BigQuery execution, replace the source table with your uploaded table.
SELECT
  SAFE_CAST(event_date AS DATE) AS event_date,
  LOWER(TRIM(event_name)) AS event_name,
  CAST(user_pseudo_id AS STRING) AS user_pseudo_id,
  COALESCE(NULLIF(TRIM(traffic_source), ''), 'unknown') AS traffic_source,
  COALESCE(NULLIF(TRIM(traffic_medium), ''), 'unknown') AS traffic_medium,
  COALESCE(NULLIF(TRIM(device_category), ''), 'unknown') AS device_category,
  COALESCE(NULLIF(TRIM(country), ''), 'unknown') AS country,
  SAFE_CAST(purchase_revenue_usd AS NUMERIC) AS purchase_revenue_usd
FROM `YOUR_PROJECT.YOUR_DATASET.ga4_ecommerce_events`
