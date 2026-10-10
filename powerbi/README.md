
# Power BI Dashboard

This folder contains the Power BI dashboard and supporting assets for the **Marketing Campaign Revenue Analytics** project.

## Dashboard Pages

The Power BI report includes four pages:

1. **Executive Overview** — High-level ecommerce performance indicators.
2. **Ecommerce Journey** — Analysis of ecommerce event activity.
3. **Daily Performance** — Daily trends and performance metrics.
4. **Traffic & Revenue** — Traffic-source performance and revenue analysis.

## Folder Structure

```text
powerbi/
├── README.md
├── <your-report-name>.pbix
├── themes/
│   └── Growth-Analytics-Theme.json
└── screenshots/
    ├── executive-overview.png
    ├── ecommerce-journey.png
    ├── daily-performance.png
    └── traffic-revenue.png
```

*Replace `<your-report-name>.pbix` with the actual name of your Power BI file.*

## Dashboard Preview

### 1. Executive Overview
![Executive Overview](screenshots/executive-overview.png)

### 2. Ecommerce Journey
![Ecommerce Journey](screenshots/ecommerce-journey.png)

### 3. Daily Performance
![Daily Performance](screenshots/daily-performance.png)

### 4. Traffic & Revenue
![Traffic and Revenue](screenshots/traffic-revenue.png)

## Custom Report Theme

The `themes/Growth-Analytics-Theme.json` file contains the custom **Growth Analytics** theme.

The theme uses:
- Teal and blue as primary analytical colors.
- Orange for highlights and comparisons.
- A light background with dark navy text.
- Inter typography defaults.

To import the theme, open the report in Power BI Desktop, navigate to the report theme options, choose **Browse for themes** or **Import theme**, and select the JSON file.

Review each page after importing the theme because existing visuals may retain manually configured formatting.

## Dataset and Key Metrics

The report is based on the project's sampled GA4 ecommerce event data.

| Metric | Validated Sample Result |
|---|---:|
| Total events | 10,000 |
| Purchase events | 2,000 |
| Distinct users | 7,758 |
| Purchase revenue | $128,659 |

The working dataset contains 2,000 records for each of five event types: `session_start`, `page_view`, `add_to_cart`, `begin_checkout`, and `purchase`.

**Important:** This is a balanced sample, not the complete GA4 dataset. Event proportions must not be interpreted as representative conversion rates. Advertising spend is not included, so ROAS and campaign profitability cannot be calculated from this dataset alone.

## How to Open the Report

1. Download or clone the project repository.
2. Open the `.pbix` file using Power BI Desktop.
3. Review the four report pages and interact with the available visuals.

The screenshots provide static previews; the PBIX file contains the interactive report.

---

**Project:** Marketing Campaign Revenue Analytics  
**Tools:** Power BI, Google BigQuery, SQL, Python, Excel, and Git
