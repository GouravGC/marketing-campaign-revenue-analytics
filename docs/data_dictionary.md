# Data Dictionary

| Column | Meaning | Handling |
|---|---|---|
| event_date | GA4 event date | Parsed as date |
| event_name | Interaction type | Standardized to lowercase |
| user_pseudo_id | Pseudonymous GA4 user identifier | Stored as string |
| traffic_source | GA4 traffic source | Missing/blank becomes `unknown` |
| traffic_medium | GA4 traffic medium | Missing/blank becomes `unknown` |
| device_category | Device category | Missing/blank becomes `unknown` |
| country | Event country | Missing/blank becomes `unknown` |
| purchase_revenue_usd | Purchase revenue in USD | Null for non-purchase events is expected |

## Limitations
- This is a 10,000-row stratified sample with up to 2,000 rows per selected event type.
- Event counts and funnel ratios are sample-based and are not population estimates.
- The extract does not include advertising spend, so ROAS cannot be calculated.
- The available columns do not contain a unique event identifier; exact duplicates are profiled, not automatically removed.
