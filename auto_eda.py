import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="UK Retail Auto-EDA",
    page_icon="🔍",
    layout="wide"
)

st.title("UK Retail Auto-EDA & Data Quality Report")

st.markdown(
    """
    This page automatically profiles the UK Retail dataset before business analysis.
    It helps identify data quality issues, missing values, duplicates, and reporting risks.
    """
)

st.divider()


# --------------------------------------------------
# Load dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    clean_path = "data/clean_data.csv"
    raw_path = "data/data.csv"

    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path, encoding="ISO-8859-1")
        source = clean_path
    elif os.path.exists(raw_path):
        df = pd.read_csv(raw_path, encoding="ISO-8859-1")
        source = raw_path
    else:
        return None, None

    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    return df, source


df, source = load_data()

if df is None:
    st.error("No dataset found. Please make sure `data/clean_data.csv` or `data/data.csv` exists.")
    st.stop()

st.success(f"Loaded dataset: `{source}`")


# --------------------------------------------------
# Dataset preview
# --------------------------------------------------
st.header("1. Dataset Preview")

st.dataframe(df.head(), use_container_width=True)


# --------------------------------------------------
# Dataset overview
# --------------------------------------------------
st.header("2. Dataset Overview")

total_rows = len(df)
total_columns = len(df.columns)
duplicate_rows = df.duplicated().sum()
total_missing = df.isna().sum().sum()
memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)

numeric_columns = df.select_dtypes(include=["number"]).shape[1]
categorical_columns = df.select_dtypes(include=["object"]).shape[1]
datetime_columns = df.select_dtypes(include=["datetime"]).shape[1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", f"{total_rows:,}")
col2.metric("Columns", f"{total_columns:,}")
col3.metric("Duplicate Rows", f"{duplicate_rows:,}")
col4.metric("Missing Values", f"{total_missing:,}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Numeric Columns", f"{numeric_columns:,}")
col6.metric("Categorical Columns", f"{categorical_columns:,}")
col7.metric("Datetime Columns", f"{datetime_columns:,}")
col8.metric("Memory Usage", f"{memory_usage:.2f} MB")


# --------------------------------------------------
# Basic column list
# --------------------------------------------------
st.header("3. Column Summary")

column_summary = pd.DataFrame({
    "Column": df.columns,
    "Data Type": [str(df[col].dtype) for col in df.columns],
    "Missing Values": [df[col].isna().sum() for col in df.columns],
    "Unique Values": [df[col].nunique() for col in df.columns]
})

st.dataframe(column_summary, use_container_width=True)

# --------------------------------------------------
# Data catalog
# --------------------------------------------------
st.header("4. Data Catalog")

catalog_rows = []

for column in df.columns:
    column_data = df[column]
    missing_count = column_data.isna().sum()
    missing_percent = (missing_count / len(df)) * 100
    unique_count = column_data.nunique()

    if column_data.dropna().empty:
        sample_value = "N/A"
    else:
        sample_value = column_data.dropna().iloc[0]

    if pd.api.types.is_numeric_dtype(column_data):
        min_value = column_data.min()
        max_value = column_data.max()
    else:
        min_value = "N/A"
        max_value = "N/A"

    catalog_rows.append({
        "Column": column,
        "Data Type": str(column_data.dtype),
        "Missing Count": missing_count,
        "Missing %": round(missing_percent, 2),
        "Unique Values": unique_count,
        "Sample Value": sample_value,
        "Min": min_value,
        "Max": max_value
    })

catalog_df = pd.DataFrame(catalog_rows)

st.dataframe(catalog_df, use_container_width=True)


# --------------------------------------------------
# Missingness analysis
# --------------------------------------------------
st.header("5. Missingness Analysis")

missing_df = catalog_df[["Column", "Missing Count", "Missing %"]].copy()
missing_df = missing_df[missing_df["Missing Count"] > 0]
missing_df = missing_df.sort_values("Missing %", ascending=False)

if missing_df.empty:
    st.success("No missing values found in the dataset.")
else:
    st.dataframe(missing_df, use_container_width=True)

    st.subheader("Missing Values by Column")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(missing_df["Column"], missing_df["Missing %"])
    ax.set_xlabel("Column")
    ax.set_ylabel("Missing %")
    ax.set_title("Missing Values by Column")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig, use_container_width=True)

    # --------------------------------------------------
# Duplicate row check
# --------------------------------------------------
st.header("6. Duplicate Row Check")

duplicate_count = df.duplicated().sum()
duplicate_percent = (duplicate_count / len(df)) * 100

if duplicate_count == 0:
    st.success("No duplicate rows found in the dataset.")
else:
    st.warning(
        f"{duplicate_count:,} duplicate rows found "
        f"({duplicate_percent:.2f}% of the dataset)."
    )

    st.markdown(
        """
        **Business impact:** Duplicate records may inflate revenue, order counts, product demand,
        and customer activity metrics if they are not reviewed before dashboard reporting.
        """
    )

    duplicate_rows = df[df.duplicated(keep=False)]
    st.dataframe(duplicate_rows.head(20), use_container_width=True)


# --------------------------------------------------
# Retail validation checks
# --------------------------------------------------
st.header("7. Retail Data Validation Checks")

validation_results = []

if "Quantity" in df.columns:
    negative_quantity_count = (df["Quantity"] < 0).sum()
    validation_results.append({
        "Check": "Negative Quantity",
        "Issue Count": negative_quantity_count,
        "Issue %": round((negative_quantity_count / len(df)) * 100, 2),
        "Why It Matters": "Negative quantities may indicate returns or cancellations."
    })

if "UnitPrice" in df.columns:
    invalid_price_count = (df["UnitPrice"] <= 0).sum()
    validation_results.append({
        "Check": "Zero or Negative Unit Price",
        "Issue Count": invalid_price_count,
        "Issue %": round((invalid_price_count / len(df)) * 100, 2),
        "Why It Matters": "Invalid prices can distort revenue and average order value."
    })

if "CustomerID" in df.columns:
    missing_customer_count = df["CustomerID"].isna().sum()
    validation_results.append({
        "Check": "Missing Customer ID",
        "Issue Count": missing_customer_count,
        "Issue %": round((missing_customer_count / len(df)) * 100, 2),
        "Why It Matters": "Missing customer IDs limit customer segmentation and repeat purchase analysis."
    })

if "InvoiceDate" in df.columns:
    invalid_date_count = df["InvoiceDate"].isna().sum()
    validation_results.append({
        "Check": "Invalid Invoice Date",
        "Issue Count": invalid_date_count,
        "Issue %": round((invalid_date_count / len(df)) * 100, 2),
        "Why It Matters": "Invalid dates affect trend, seasonality, and time-series analysis."
    })

if "InvoiceNo" in df.columns:
    cancelled_invoice_count = df["InvoiceNo"].astype(str).str.startswith("C").sum()
    validation_results.append({
        "Check": "Cancelled Invoice",
        "Issue Count": cancelled_invoice_count,
        "Issue %": round((cancelled_invoice_count / len(df)) * 100, 2),
        "Why It Matters": "Cancelled invoices should be treated separately from completed sales."
    })

if {"Quantity", "UnitPrice", "Revenue"}.issubset(df.columns):
    expected_revenue = df["Quantity"] * df["UnitPrice"]
    revenue_mismatch_count = (abs(df["Revenue"] - expected_revenue) > 0.01).sum()

    validation_results.append({
        "Check": "Revenue Calculation Mismatch",
        "Issue Count": revenue_mismatch_count,
        "Issue %": round((revenue_mismatch_count / len(df)) * 100, 2),
        "Why It Matters": "Revenue should match Quantity × UnitPrice for reliable financial reporting."
    })

validation_df = pd.DataFrame(validation_results)

if validation_df.empty:
    st.info("No retail-specific validation checks were available for this dataset.")
else:
    st.dataframe(validation_df, use_container_width=True)
    # --------------------------------------------------
# Governance flags
# --------------------------------------------------
st.header("8. Governance Flags")

governance_flags = []

# Missingness flags
for column in df.columns:
    missing_percent = df[column].isna().mean() * 100

    if missing_percent >= 40:
        governance_flags.append({
            "Flag": f"Critical missingness in {column}",
            "Severity": "Critical",
            "Reason": f"{missing_percent:.2f}% of values are missing. This column may not be reliable for reporting."
        })
    elif missing_percent >= 20:
        governance_flags.append({
            "Flag": f"High missingness in {column}",
            "Severity": "High",
            "Reason": f"{missing_percent:.2f}% of values are missing. Results using this column may be incomplete."
        })
    elif missing_percent >= 5:
        governance_flags.append({
            "Flag": f"Moderate missingness in {column}",
            "Severity": "Medium",
            "Reason": f"{missing_percent:.2f}% of values are missing. Monitor before using this field in KPIs."
        })

# Duplicate rows flag
if duplicate_count > 0:
    governance_flags.append({
        "Flag": "Duplicate rows detected",
        "Severity": "High",
        "Reason": f"{duplicate_count:,} duplicate rows found. Duplicates may inflate revenue, transaction, and product demand metrics."
    })

# Validation-based flags
if not validation_df.empty:
    for _, row in validation_df.iterrows():
        if row["Issue Count"] > 0:
            severity = "Medium"

            if row["Issue %"] >= 10:
                severity = "High"
            elif row["Issue %"] >= 25:
                severity = "Critical"

            governance_flags.append({
                "Flag": row["Check"],
                "Severity": severity,
                "Reason": row["Why It Matters"]
            })

# Constant column flags
for column in df.columns:
    if df[column].nunique(dropna=True) == 1:
        governance_flags.append({
            "Flag": f"Constant column: {column}",
            "Severity": "Low",
            "Reason": "This column has only one unique value and may add limited analytical value."
        })

governance_flags_df = pd.DataFrame(governance_flags)

if governance_flags_df.empty:
    st.success("No governance flags raised. Dataset appears ready for reporting.")
else:
    st.dataframe(governance_flags_df, use_container_width=True)
    # --------------------------------------------------
# Overall data quality score
# --------------------------------------------------
st.header("9. Overall Data Quality Score")

# Completeness: based on missing values
total_cells = total_rows * total_columns
missing_ratio = total_missing / total_cells if total_cells > 0 else 0
completeness_score = 35 * (1 - missing_ratio)

# Uniqueness: based on duplicate rows
duplicate_ratio = duplicate_count / total_rows if total_rows > 0 else 0
uniqueness_score = 20 * (1 - duplicate_ratio)

# Validity: based on retail validation checks
if validation_df.empty:
    validity_issue_ratio = 0
else:
    total_validation_issues = validation_df["Issue Count"].sum()
    validity_issue_ratio = total_validation_issues / (len(validation_df) * total_rows)

validity_score = 25 * (1 - validity_issue_ratio)

# Consistency: based on governance flags
high_risk_flags = 0

if not governance_flags_df.empty:
    high_risk_flags = governance_flags_df[
        governance_flags_df["Severity"].isin(["High", "Critical"])
    ].shape[0]

consistency_penalty = min(high_risk_flags * 3, 20)
consistency_score = 20 - consistency_penalty

# Final score
overall_quality_score = round(
    completeness_score + uniqueness_score + validity_score + consistency_score,
    2
)

# Rating
if overall_quality_score >= 85:
    quality_rating = "Good — dataset is largely reporting-ready"
elif overall_quality_score >= 70:
    quality_rating = "Fair — dataset needs some review before reporting"
elif overall_quality_score >= 50:
    quality_rating = "Poor — dataset has significant quality issues"
else:
    quality_rating = "Critical — dataset needs major remediation"

score_col1, score_col2, score_col3, score_col4, score_col5 = st.columns(5)

score_col1.metric("Overall Score", f"{overall_quality_score} / 100")
score_col2.metric("Completeness", f"{completeness_score:.1f} / 35")
score_col3.metric("Uniqueness", f"{uniqueness_score:.1f} / 20")
score_col4.metric("Validity", f"{validity_score:.1f} / 25")
score_col5.metric("Consistency", f"{consistency_score:.1f} / 20")

st.info(quality_rating)

score_breakdown = pd.DataFrame({
    "Dimension": ["Completeness", "Uniqueness", "Validity", "Consistency"],
    "Score": [
        round(completeness_score, 2),
        round(uniqueness_score, 2),
        round(validity_score, 2),
        round(consistency_score, 2)
    ],
    "Maximum Score": [35, 20, 25, 20]
})

st.subheader("Score Breakdown")
st.dataframe(score_breakdown, use_container_width=True)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(score_breakdown["Dimension"], score_breakdown["Score"])
ax.set_ylim(0, 35)
ax.set_ylabel("Score")
ax.set_title("Data Quality Score Breakdown")

st.pyplot(fig, use_container_width=True)
# --------------------------------------------------
# Business glossary
# --------------------------------------------------
st.header("10. Business Glossary")

glossary_data = [
    {
        "Field": "InvoiceNo",
        "Business Definition": "Unique invoice or transaction identifier. Cancelled invoices may start with 'C'."
    },
    {
        "Field": "StockCode",
        "Business Definition": "Product stock keeping unit used to identify each item."
    },
    {
        "Field": "Description",
        "Business Definition": "Product name or product description."
    },
    {
        "Field": "Quantity",
        "Business Definition": "Number of units purchased. Negative values may indicate returns or cancellations."
    },
    {
        "Field": "InvoiceDate",
        "Business Definition": "Date and time when the transaction was recorded."
    },
    {
        "Field": "UnitPrice",
        "Business Definition": "Price per unit of product."
    },
    {
        "Field": "CustomerID",
        "Business Definition": "Unique customer identifier used for customer-level analysis."
    },
    {
        "Field": "Country",
        "Business Definition": "Country associated with the customer transaction."
    },
    {
        "Field": "Revenue",
        "Business Definition": "Transaction revenue calculated as Quantity multiplied by UnitPrice."
    }
]

glossary_df = pd.DataFrame(glossary_data)

# Only show glossary rows for columns that exist in the dataset
glossary_df = glossary_df[glossary_df["Field"].isin(df.columns)]

st.markdown(
    """
    The business glossary explains the meaning of each field in plain English.
    This helps improve consistency across analysis, dashboarding, and stakeholder reporting.
    """
)

st.dataframe(glossary_df, use_container_width=True)


# --------------------------------------------------
# Data lineage
# --------------------------------------------------
st.header("11. Data Lineage")

st.markdown(
    """
    Data lineage shows how the dataset moves from raw source data to final business insights.
    This improves transparency and makes dashboard outputs easier to trust.
    """
)

st.code(
    """
Raw UK Retail Dataset
        ↓
Data Cleaning Notebook
        ↓
Cleaned Dataset
        ↓
Auto-EDA & Data Quality Layer
        ↓
Business Analysis Notebook
        ↓
Streamlit Dashboard / Power BI Dashboard
        ↓
Business Recommendations
    """,
    language="text"
)

# --------------------------------------------------
# Export reports
# --------------------------------------------------
st.header("12. Export Reports")

st.markdown(
    """
    Download the automated profiling and quality outputs.
    These files can be used for documentation, stakeholder review, or Power BI reporting.
    """
)

# Create quality summary table
quality_summary_df = pd.DataFrame({
    "Metric": [
        "Total Rows",
        "Total Columns",
        "Duplicate Rows",
        "Missing Values",
        "Overall Quality Score",
        "Completeness Score",
        "Uniqueness Score",
        "Validity Score",
        "Consistency Score"
    ],
    "Value": [
        total_rows,
        total_columns,
        duplicate_count,
        total_missing,
        overall_quality_score,
        round(completeness_score, 2),
        round(uniqueness_score, 2),
        round(validity_score, 2),
        round(consistency_score, 2)
    ]
})

export_col1, export_col2, export_col3, export_col4 = st.columns(4)

with export_col1:
    st.download_button(
        label="Download Data Catalog",
        data=catalog_df.to_csv(index=False),
        file_name="data_catalog_report.csv",
        mime="text/csv"
    )

with export_col2:
    st.download_button(
        label="Download Validation Checks",
        data=validation_df.to_csv(index=False),
        file_name="validation_checks_report.csv",
        mime="text/csv"
    )

with export_col3:
    st.download_button(
        label="Download Governance Flags",
        data=governance_flags_df.to_csv(index=False),
        file_name="governance_flags_report.csv",
        mime="text/csv"
    )

with export_col4:
    st.download_button(
        label="Download Quality Summary",
        data=quality_summary_df.to_csv(index=False),
        file_name="quality_summary_report.csv",
        mime="text/csv"
    )