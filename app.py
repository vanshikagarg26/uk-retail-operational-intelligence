import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="UK Retail Operational Intelligence",
    layout="wide"
)

# Title
st.title("UK Retail Operational Intelligence")
st.write(
    "A business intelligence dashboard analysing revenue, geography, products, customers, seasonality, and operational inefficiencies."
)

# Load data
df = pd.read_csv("data/clean_data.csv")

# -----------------------
# Executive Summary
# -----------------------
st.header("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"£{df['Revenue'].sum():,.0f}")
col2.metric("Transactions", f"{len(df):,}")
col3.metric("Customers", f"{df['CustomerID'].nunique():,}")
col4.metric("Countries", f"{df['Country'].nunique()}")

# -----------------------
# Revenue by Geography
# -----------------------
st.header("Revenue by Geography")

country_revenue = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
country_revenue.plot(kind="bar", ax=ax1)
ax1.set_title("Top 10 Countries by Revenue")
ax1.set_xlabel("Country")
ax1.set_ylabel("Revenue (£)")
plt.xticks(rotation=45)

st.pyplot(fig1)

# -----------------------
# Product Performance
# -----------------------
st.header("Product Performance")

top_products = df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(12, 6))
top_products.plot(kind="bar", ax=ax2)
ax2.set_title("Top 10 Products by Revenue")
ax2.set_xlabel("Product")
ax2.set_ylabel("Revenue (£)")
plt.xticks(rotation=75)

st.pyplot(fig2)

# -----------------------
# Customer Insights
# -----------------------
st.header("Customer Insights")

top_customers = df.groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(10, 5))
top_customers.plot(kind="bar", ax=ax3)
ax3.set_title("Top 10 Customers by Revenue")
ax3.set_xlabel("Customer ID")
ax3.set_ylabel("Revenue (£)")
plt.xticks(rotation=45)

st.pyplot(fig3)

# -----------------------
# Seasonality Analysis
# -----------------------
st.header("Seasonality Analysis")

monthly_revenue = df.groupby("Month")["Revenue"].sum().sort_index()

fig4, ax4 = plt.subplots(figsize=(10, 5))
monthly_revenue.plot(kind="line", marker="o", ax=ax4)
ax4.set_title("Monthly Revenue Trend")
ax4.set_xlabel("Month")
ax4.set_ylabel("Revenue (£)")
ax4.set_xticks(range(1, 13))

st.pyplot(fig4)

# -----------------------
# Final Insight
# -----------------------
st.header("Strategic Insights")

st.markdown("""
### Key Business Issues:
- Heavy UK revenue concentration
- Holiday/seasonal dependency
- Product return-driven operational inefficiencies

### Strategic Recommendations:
1. Expand stronger international markets
2. Diversify year-round gifting strategy
3. Reduce return leakage in top-selling products
""")