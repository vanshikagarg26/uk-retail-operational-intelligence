# UK Retail Operational Intelligence

## Project Overview

This project analyses transactional data from a UK-based online retailer to identify business inefficiencies, revenue opportunities, and strategic growth pathways.

Using Python, pandas, and data visualisation, the project examines:

- Geographic revenue concentration
- Product performance
- Customer value and loyalty
- Seasonal sales dependency
- Return-driven operational inefficiencies

## Business Objective

To use data and technology to identify where the business creates value, where it loses value, and how strategic improvements can increase profitability and resilience.
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
- Streamlit (dashboard phase)
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

## Final Business Conclusion

The business demonstrates strong revenue generation but faces strategic vulnerabilities across market concentration, seasonal dependency, and operational inefficiency. Addressing these areas could improve resilience, profitability, and sustainable long-term growth.
## Project Structure

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
├── app.py
├── README.md
└── requirements.txt
## What I Learned

Through this project, I learned how to:

- Clean and validate messy real-world transactional data
- Separate revenue-driving data from operational leakage (returns)
- Analyse geographic, product, customer, and seasonal business performance
- Translate raw data into strategic business recommendations
- Use data analysis not just to describe trends, but to solve business inefficiencies