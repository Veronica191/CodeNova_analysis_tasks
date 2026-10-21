

from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

DATA_PATH = Path(__file__).resolve().parent / "data" / "sales.csv"

# Page configuration
st.set_page_config(
    page_title="CodeNova Sales Dashboard",
    page_icon=":material/analytics:",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    # Convert dates to datetime
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    return df


if not DATA_PATH.is_file():
    st.error(
        "The sales dataset was not found. Make sure `data/sales.csv` is "
        "included next to `app.py`."
    )
    st.stop()

if DATA_PATH.stat().st_size == 0:
    st.info("The sales dataset is empty. Add sales records to view the dashboard.")
    st.stop()

df = load_data()

# Dashboard title
st.title("Sales Performance Dashboard")
st.markdown(
    "Explore sales, profitability, and business performance "
    "using interactive filters."
)

# Check required columns
required_columns = [
    "Order Date", "Sales", "Profit", "Category", "Region",
    "Quantity", "Order ID"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

if df.empty:
    st.info("The sales dataset is empty. Add sales records to view the dashboard.")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

valid_dates = df["Order Date"].dropna()

if valid_dates.empty:
    st.info(
        "The dataset has no valid order dates. Check the Order Date values "
        "in the sales dataset."
    )
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_range = st.sidebar.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select regions",
    regions,
    default=regions
)

# Apply filters
filtered_df = df[
    (df["Order Date"].dt.date >= date_range[0]) &
    (df["Order Date"].dt.date <= date_range[1]) &
    (df["Category"].isin(selected_categories)) &
    (df["Region"].isin(selected_regions))
].copy()

# Numerical threshold filter
if not filtered_df.empty:
    min_sales = float(filtered_df["Sales"].min())
    max_sales = float(filtered_df["Sales"].max())

    if min_sales < max_sales:
        sales_threshold = st.sidebar.slider(
            "Minimum sales value",
            min_value=min_sales,
            max_value=max_sales,
            value=min_sales
        )
    else:
        st.sidebar.caption(
            f"Minimum sales value is fixed at ${min_sales:,.2f} for this selection."
        )
        sales_threshold = min_sales

    filtered_df = filtered_df[
        filtered_df["Sales"] >= sales_threshold
    ]

# KPI metrics
st.subheader("Key Performance Indicators")

if filtered_df.empty:
    st.info(
        "No records match your selected filters. Adjust the filters in the "
        "sidebar to view sales performance."
    )
else:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_quantity = filtered_df["Quantity"].sum()
    total_orders = filtered_df["Order ID"].nunique()

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0 else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0 else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    col1.metric("Total Revenue", f"${total_sales:,.2f}", border=True)
    col2.metric("Total Profit", f"${total_profit:,.2f}", border=True)
    col3.metric("Profit Margin", f"{profit_margin:.2f}%", border=True)
    col4.metric("Units Sold", f"{total_quantity:,.0f}", border=True)
    col5.metric("Average Order Value", f"${average_order_value:,.2f}", border=True)

    st.caption(
        f"Displaying {len(filtered_df):,} records "
        f"from {total_orders:,} unique orders."
    )

    
# Stop chart creation if no records match the filters
if not filtered_df.empty:

    st.divider()
    st.subheader("Sales Analysis")

    category_column, trend_column = st.columns(2, gap="large")

    # 1. Bar chart: Revenue by category
    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    with category_column:
        with st.container(border=True):
            fig_bar = px.bar(
                category_sales,
                x="Category",
                y="Sales",
                title="Revenue by Category",
                labels={
                    "Category": "Product Category",
                    "Sales": "Revenue ($)"
                },
                color="Category",
                color_discrete_sequence=["#0F766E", "#2563EB", "#F59E0B"],
                text_auto="$,.0f",
                template="plotly_white"
            )

            fig_bar.update_layout(
                showlegend=False,
                title_x=0.02,
                height=380,
                margin=dict(l=20, r=20, t=55, b=20)
            )
            fig_bar.update_xaxes(title_text="")
            fig_bar.update_yaxes(tickformat="$,.0f", title_text="Revenue ($)")
            fig_bar.update_traces(
                hovertemplate=(
                    "<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
                )
            )

            st.plotly_chart(
                fig_bar,
                width="stretch",
                alt="Revenue by product category"
            )

    # 2. Line chart: Monthly revenue trend
    monthly_sales = filtered_df.copy()

    monthly_sales["Month"] = (
        monthly_sales["Order Date"].dt.to_period("M").astype(str)
    )

    monthly_sales = (
        monthly_sales.groupby("Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )

    with trend_column:
        with st.container(border=True):
            fig_line = px.line(
                monthly_sales,
                x="Month",
                y="Sales",
                title="Monthly Revenue Trend",
                labels={
                    "Month": "Month",
                    "Sales": "Revenue ($)"
                },
                markers=True,
                color_discrete_sequence=["#0F766E"],
                template="plotly_white"
            )

            fig_line.update_layout(
                title_x=0.02,
                height=380,
                margin=dict(l=20, r=20, t=55, b=45)
            )
            fig_line.update_xaxes(title_text="Month", tickangle=-45)
            fig_line.update_yaxes(tickformat="$,.0f", title_text="Revenue ($)")
            fig_line.update_traces(
                hovertemplate=(
                    "<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>"
                )
            )

            st.plotly_chart(
                fig_line,
                width="stretch",
                alt="Monthly revenue trend"
            )

    # 3. Scatter plot: Sales versus profit
    with st.container(border=True):
        fig_scatter = px.scatter(
            filtered_df,
            x="Sales",
            y="Profit",
            color="Category",
            hover_data={
                "Sales": ":$,.2f",
                "Profit": ":$,.2f",
                "Order ID": True,
                "Region": True
            },
            title="Sales vs. Profit by Order",
            labels={
                "Sales": "Sales ($)",
                "Profit": "Profit ($)"
            },
            opacity=0.7,
            color_discrete_sequence=["#0F766E", "#2563EB", "#F59E0B"],
            template="plotly_white"
        )

        fig_scatter.update_layout(
            title_x=0.02,
            height=480,
            margin=dict(l=20, r=20, t=55, b=20),
            legend_title_text="Category"
        )
        fig_scatter.update_xaxes(tickformat="$,.0f")
        fig_scatter.update_yaxes(tickformat="$,.0f")
        fig_scatter.add_hline(
            y=0,
            line_dash="dash",
            line_color="#64748B"
        )

        st.plotly_chart(
            fig_scatter,
            width="stretch",
            alt="Sales versus profit by order, colored by category"
        )
