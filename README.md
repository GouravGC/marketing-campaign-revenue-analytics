# Marketing Campaign Revenue Analytics

An end-to-end analytics engineering project using GA4 ecommerce sample data, Python, SQL, Google BigQuery, Power BI, and Excel to transform event-level data into validated analytical datasets and business performance reporting.

**Repository:** [marketing-campaign-revenue-analytics](https://github.com/GouravGC/marketing-campaign-revenue-analytics)

## Project Highlights

- **10,000 event records** processed across 5 event types.
- **$128,659 in purchase revenue** recorded in the sampled dataset.
- **7,758 distinct users** identified.
- **5/5 Python tests passed**, validating key pipeline and data-quality behaviors.

## 1. Key Analytical Findings

- **Purchase revenue:** The 2,000 sampled purchase events account for $128,659 in revenue, averaging approximately **$64.33 per sampled purchase event**. This is a sample-level average, not a population-wide ecommerce benchmark.
- **User activity:** The dataset contains 7,758 distinct users across 10,000 events, equivalent to approximately **1.29 events per distinct user** in the sample. This describes the sampled records, not necessarily complete user journeys.
- **Data quality:** The exported dataset contained **685 exact duplicate rows flagged for review**. Duplicate handling matters because repeated records can inflate event counts and revenue if not addressed appropriately.
- **Analytical outputs:** The pipeline produced **440 rows in the daily performance mart, 44 rows in the traffic-source performance mart, 5 rows in the event summary mart, and 440 rows in the daily event-ranking mart**.

> **Sampling limitation:** The dataset contains 2,000 records for each of five event types: `session_start`, `page_view`, `add_to_cart`, `begin_checkout`, and `purchase`. Because the sample is balanced by event type, event proportions must not be interpreted as actual conversion rates or representative GA4 traffic distributions.

## 2. Business Objective

Build a repeatable analytics workflow that converts raw ecommerce events into reliable datasets for reporting and analysis.

The project focuses on:

- Event-level data preparation and validation.
- Reusable SQL transformations and analytical data marts.
- Daily performance and traffic-source reporting.
- Ecommerce event summaries and event rankings.
- Reconciliation between analytical outputs and reporting artifacts.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Google BigQuery | Cloud data warehouse and SQL execution |
| SQL | Data transformations, analytical modeling, and validation |
| Python | Pipeline implementation and data-quality checks |
| pytest | Automated testing |
| Power BI | Interactive analytics dashboards |
| Microsoft Excel | Reconciliation and data-quality reporting |
| Git and GitHub | Version control and project collaboration |

## 4. Data Pipeline Architecture

```text
GA4 Ecommerce Sample Data
            |
            v
      Raw Event Data
            |
            v
     Staging Layer
            |
            v
   Intermediate Models
            |
            v
      Analytical Marts
        /         \
       v           v
   Power BI       Excel
   Dashboards     Reports
```

The workflow separates raw data, staging transformations, intermediate logic, and reporting-ready marts. This structure improves maintainability and makes data-quality checks easier to perform.

## 5. Analytical Data Marts

| Data mart | Rows produced | Purpose |
|---|---:|---|
| Daily Performance | 440 | Analyze daily ecommerce performance |
| Traffic Source Performance | 44 | Compare performance across traffic-source dimensions |
| Event Summary | 5 | Summarize the five event types |
| Daily Event Ranking | 440 | Rank events within daily reporting dimensions |

Row counts represent the validated outputs from this project's sampled dataset and current modeling logic.

## 6. Power BI Dashboard

The Power BI report contains four analytical pages:

1. **Executive Overview** — high-level performance indicators.
2. **Ecommerce Journey** — event activity across the ecommerce journey.
3. **Daily Performance** — daily trends and changes in performance.
4. **Traffic & Revenue** — performance comparisons by traffic source.

These pages provide different views of the same analytical workflow, from overall reporting to event-level and traffic-source analysis.

## 7. Excel Reconciliation

The workbook `GA4_Analytics_Reconciliation.xlsx` supports validation and reporting through worksheets for:

- Overview
- Daily Performance
- Traffic Sources
- Event Summary
- Data Quality

The workbook complements the SQL and Python workflow by providing an accessible format for reviewing analytical outputs and data-quality information.

## 8. Testing and Validation

The Python test suite passed **5 out of 5 tests**.

Coverage includes:

- Row preservation behavior.
- Standardization of missing dimension values.
- Data-quality validation.
- Rejection of negative revenue values.
- Analytical mart generation.

The BigQuery validation results also confirmed 10,000 total events, 2,000 purchase events, 7,758 distinct users, and $128,659 in purchase revenue for the sampled dataset.

## 9. Data Source and Limitations

The project uses the public GA4 obfuscated ecommerce sample table:

`bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`

The source date range used is November 1, 2020, through January 31, 2021.

Important limitations:

- The working dataset is a balanced sample of 10,000 event records, not the full GA4 dataset.
- The sample should not be used to estimate representative conversion rates without a suitable sampling strategy.
- Advertising spend and campaign-cost data are not included; therefore, ROAS, advertising profitability, and cost-per-acquisition claims are not supported.
- Duplicate records require careful handling so they do not inflate analytical results.
- The reported figures describe this project's validated dataset and should not be interpreted as current business performance.

## 10. Skills Demonstrated

- SQL-based analytical modeling.
- Cloud data warehousing with BigQuery.
- Python data processing and automated testing.
- Data-quality checks and reconciliation.
- Analytical data-mart design.
- Power BI dashboard development.
- Excel reporting.
- Git-based version control and project organization.

## Conclusion

This project demonstrates an analytics engineering workflow that transforms sampled GA4 ecommerce events into tested analytical datasets and reporting outputs. Its emphasis is on measurable results, data-quality validation, reusable transformations, and clear communication of analytical limitations.