
WITH sampled_events AS (
    SELECT
        PARSE_DATE('%Y%m%d', event_date) AS event_date,
        event_name,
        user_pseudo_id,
        traffic_source.source AS traffic_source,
        traffic_source.medium AS traffic_medium,
        device.category AS device_category,
        geo.country AS country,
        ecommerce.purchase_revenue_in_usd AS purchase_revenue_usd
    FROM
        `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    WHERE
        _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
        AND event_name IN (
            'session_start',
            'page_view',
            'add_to_cart',
            'begin_checkout',
            'purchase'
        )
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY event_name
        ORDER BY FARM_FINGERPRINT(
            CONCAT(
                event_name,
                CAST(event_timestamp AS STRING),
                COALESCE(user_pseudo_id, '')
            )
        )
    ) <= 2000
)
SELECT *
FROM sampled_events
ORDER BY event_date, event_name;
