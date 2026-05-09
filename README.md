# UK Retail Operational Intelligence

## Live Dashboard

Streamlit App: https://uk-retail-operational-intelligence-d7yfknrazoxrbmsxxmmzue.streamlit.app/

## Project Overview

This project analyses transactional data from a UK-based online retailer to identify business inefficiencies, revenue opportunities, and strategic growth pathways.

The project includes two connected layers:

1. **Auto-EDA & Data Quality Validation Layer**  
   Automatically profiles the cleaned dataset, checks missing values, duplicate records, validation issues, governance risks, and reporting readiness.

2. **Business Intelligence Dashboard Layer**  
   Uses the reporting-ready dataset to analyse revenue trends, customer behaviour, product performance, geographic concentration, seasonality, and return-driven inefficiencies.

Using Python, pandas, Streamlit, and data visualisation, the project examines:

- Geographic revenue concentration
- Product performance
- Customer value and loyalty
- Seasonal sales dependency
- Return-driven operational inefficiencies
- Data quality and reporting-readiness risks

## Business Objective

To use data and technology to identify where the business creates value, where it loses value, and how strategic improvements can increase profitability, reporting trust, and operational resilience.

## Dataset

- Source: UK E-Commerce Retail Dataset (2010–2011)
- Rows: 541,909 original transactions
- Cleaned Rows: 397,884 valid purchase transactions
- Customers: 4,338 unique customers
- Countries: 37

## Tools & Technologies

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Streamlit
- Data Quality Validation
- Automated EDA
- Power BI-ready reporting outputs

## Auto-EDA & Data Quality Validation Layer

The project includes an automated EDA and data quality validation layer built with Python, pandas, Streamlit, and Matplotlib. This module validates the cleaned UK retail dataset before dashboard reporting to ensure the data is reliable, consistent, and reporting-ready.

### Auto-EDA Features

- Dataset overview with row count, column count, missing values, duplicate rows, and memory usage
- Automated data catalog with column-level metadata, data types, missingness, unique values, and sample values
- Missingness analysis to identify incomplete fields
- Duplicate row detection to flag records that may inflate reporting metrics
- Retail validation checks for negative quantities, invalid prices, missing customer IDs, invalid dates, cancelled invoices, and revenue calculation mismatches
- Governance flags with severity levels to highlight reporting risks
- Overall data quality score across completeness, uniqueness, validity, and consistency
- Business glossary and data lineage documentation
- Exportable reports for Power BI or stakeholder review

### Auto-EDA Reports

The Auto-EDA layer generates the following reports:

| Report | Purpose |
|---|---|
| `data_catalog_report.csv` | Column-level metadata and profiling summary |
| `validation_checks_report.csv` | Retail-specific data validation outputs |
| `governance_flags_report.csv` | Data quality and governance risks with severity levels |
| `quality_summary_report.csv` | Overall quality score and scoring breakdown |

### Key Auto-EDA Finding

The cleaned dataset passed all retail validation checks, with duplicate rows remaining as the main reporting-readiness issue. The Auto-EDA layer flagged 5,192 duplicate rows, representing 1.30% of the cleaned dataset. These records may affect transaction counts, product demand analysis, and revenue reporting if not reviewed before dashboarding.

## Key Findings

### 1. UK Revenue Concentration

The UK market dominates total revenue, creating strong domestic performance but exposing the business to geographic concentration risk.

### 2. Seasonal Revenue Dependency

Revenue peaks significantly during holiday periods, particularly November, while weaker months such as January highlight seasonal sales vulnerability.

### 3. Product Category Concentration

Top-performing products are heavily concentrated in gifting and decorative categories, suggesting a strong but seasonally sensitive business model.

### 4. Customer Segmentation Opportunity

Customer value is relatively distributed, but distinct differences between frequent buyers and high-revenue customers suggest targeted retention and upselling opportunities.

### 5. Return-Driven Revenue Leakage

Several top-selling products also experience high return volumes, indicating operational inefficiencies that may reduce net profitability.

## Strategic Recommendations

### Expand Internationally

Scale stronger secondary European markets to reduce overdependence on UK revenue.

### Diversify Year-Round Product Strategy

Expand beyond holiday gifting cycles to improve off-season revenue stability.

### Reduce Return-Related Inefficiencies

Audit high-selling, high-return products to improve quality, fulfilment, and customer satisfaction.

### Strengthen Data Quality Monitoring

Use the Auto-EDA validation layer before BI reporting to monitor duplicates, validation issues, and reporting-readiness risks.

## Final Business Conclusion

The business demonstrates strong revenue generation but faces strategic vulnerabilities across market concentration, seasonal dependency, operational inefficiency, and data quality monitoring. Addressing these areas could improve resilience, profitability, reporting trust, and sustainable long-term growth.

## Project Structure

```text
uk-retail-operational-intelligence/
│
├── data/
│   ├── data.csv
│   └── clean_data.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   └── 02_business_analysis.ipynb
│
├── outputs/
│   ├── data_catalog_report.csv
│   ├── validation_checks_report.csv
│   ├── governance_flags_report.csv
│   └── quality_summary_report.csv
│
├── app.py
├── auto_eda.py
├── README.md
└── requirements.txt
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/vanshikagarg26/uk-retail-operational-intelligence.git
```

Navigate into the project folder:

```bash
cd uk-retail-operational-intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the business intelligence dashboard:

```bash
streamlit run app.py
```

Run the Auto-EDA data quality validation report:

```bash
streamlit run auto_eda.py
```

## Reporting Outputs

The Auto-EDA layer exports summary reports into the `outputs/` folder. These reports can be reviewed directly in CSV format or used as Power BI-ready inputs for a data quality reporting page.

```text
outputs/
├── data_catalog_report.csv
├── validation_checks_report.csv
├── governance_flags_report.csv
└── quality_summary_report.csv
```

## What I Learned

Through this project, I learned how to:

- Clean and validate messy real-world transactional data
- Build an automated EDA and data quality validation layer
- Generate data catalogs, governance flags, and quality scores
- Identify reporting-readiness risks before dashboard development
- Separate revenue-driving data from operational leakage such as returns
- Analyse geographic, product, customer, and seasonal business performance
- Translate raw data into strategic business recommendations
- Use data analysis not just to describe trends, but to improve reporting trust and solve business inefficiencies