

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

def summarize_by_dimension(data, dimension):
    summary_data = data[[dimension, "Sales", "Profit"]].copy()
    summary_data[dimension] = summary_data[dimension].fillna("(Unknown)")

    summary = (
        summary_data.groupby(dimension, as_index=False, dropna=False)[
            ["Sales", "Profit"]
        ]
        .sum(min_count=1)
        .rename(columns={"Sales": "Revenue", "Profit": "Profit"})
    )
    summary["Profit Margin (%)"] = (
        summary["Profit"] / summary["Revenue"] * 100
    ).where(summary["Revenue"].notna() & summary["Revenue"].ne(0))
    return summary

# Sidebar filters
st.sidebar.header("Dashboard Filters")

valid_dates = df["Order Date"].dropna()

if valid_dates.empty:
    st.info(
        "The dataset has no valid order dates. Check the Order Date values "
        "in the sales dataset."
    )
    st.stop()

future_records = df[df["Order Date"] > pd.Timestamp.now().normalize()]
if not future_records.empty:
    last_future_date = future_records["Order Date"].max().date()
    st.warning(
        f"The dataset contains {len(future_records):,} records dated after "
        f"today, through {last_future_date:%b %d, %Y}. These records remain "
        "available in the date filter and are not excluded from the analysis."
    )

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

    st.divider()
    st.subheader("Business Analysis")
    (
        profitability_tab,
        growth_tab,
        regional_tab,
        discount_tab,
        ranking_tab,
        insights_tab
    ) = st.tabs([
        "Profitability",
        "Sales growth",
        "Regional performance",
        "Discount impact",
        "Product ranking",
        "Business insights"
    ])

    if "Sub-Category" in filtered_df.columns:
        subcategory_summary = summarize_by_dimension(
            filtered_df, "Sub-Category"
        )
        subcategory_summary["Performance"] = subcategory_summary["Profit"].map(
            lambda value: (
                "Loss-making" if value < 0
                else "Profitable" if value > 0
                else "Break-even"
            ) if pd.notna(value) else "Unavailable"
        )
        subcategory_summary = subcategory_summary.sort_values(
            "Profit", na_position="last"
        )
    else:
        subcategory_summary = pd.DataFrame()

    with profitability_tab:
        st.markdown(
            "Profit and revenue are totals for the selected records. "
            "Profit margin is total profit divided by total revenue."
        )
        if subcategory_summary.empty:
            st.info("Subcategory profitability is unavailable in this dataset.")
        else:
            profit_column, margin_column = st.columns(2, gap="large")
            with profit_column:
                fig_subcategory_profit = px.bar(
                    subcategory_summary,
                    x="Profit",
                    y="Sub-Category",
                    orientation="h",
                    color="Performance",
                    color_discrete_map={
                        "Profitable": "#0F766E",
                        "Loss-making": "#DC2626",
                        "Break-even": "#64748B",
                        "Unavailable": "#94A3B8"
                    },
                    hover_data={
                        "Revenue": ":$,.2f",
                        "Profit Margin (%)": ":.2f",
                        "Profit": ":$,.2f"
                    },
                    title="Total Profit by Subcategory",
                    labels={
                        "Profit": "Total Profit ($)",
                        "Sub-Category": "Product Subcategory",
                        "Performance": "Profitability"
                    },
                    template="plotly_white"
                )
                fig_subcategory_profit.update_layout(
                    title_x=0.02,
                    height=max(420, 30 * len(subcategory_summary)),
                    margin=dict(l=15, r=15, t=55, b=20),
                    legend_title_text="Profitability"
                )
                fig_subcategory_profit.update_xaxes(tickformat="$,.0f")
                st.plotly_chart(
                    fig_subcategory_profit,
                    width="stretch",
                    alt="Total profit by subcategory, colored by profitability"
                )

            with margin_column:
                st.markdown("**Totals and margin by subcategory**")
                st.dataframe(
                    subcategory_summary[
                        [
                            "Sub-Category", "Revenue", "Profit",
                            "Profit Margin (%)", "Performance"
                        ]
                    ],
                    hide_index=True,
                    width="stretch",
                    height=420,
                    column_config={
                        "Revenue": st.column_config.NumberColumn(
                            "Revenue (total)", format="$%.2f"
                        ),
                        "Profit": st.column_config.NumberColumn(
                            "Profit (total)", format="$%.2f"
                        ),
                        "Profit Margin (%)": st.column_config.NumberColumn(
                            "Profit margin", format="%.2f%%"
                        )
                    }
                )

    with growth_tab:
        st.markdown(
            "Month-over-month growth compares each month's filtered revenue "
            "with the previous calendar month's filtered revenue. Growth is "
            "shown as unavailable when the previous month's revenue is zero "
            "or outside the selected date range."
        )
        monthly_growth = filtered_df[["Order Date", "Sales"]].copy()
        monthly_growth["Month"] = (
            monthly_growth["Order Date"].dt.to_period("M")
        )
        monthly_revenue = (
            monthly_growth.groupby("Month")["Sales"].sum(min_count=1)
        )
        month_range = pd.period_range(
            monthly_growth["Month"].min(),
            monthly_growth["Month"].max(),
            freq="M"
        )
        monthly_revenue = monthly_revenue.reindex(month_range)
        observed_months = monthly_growth["Month"].drop_duplicates()
        empty_months = month_range.difference(observed_months)
        monthly_revenue.loc[empty_months] = 0

        growth_table = pd.DataFrame({
            "Month": month_range.astype(str),
            "Revenue": monthly_revenue.to_numpy()
        })
        previous_revenue = monthly_revenue.shift(1)
        growth_table["Revenue Growth (%)"] = (
            (monthly_revenue - previous_revenue) / previous_revenue * 100
        ).where(previous_revenue.notna() & previous_revenue.ne(0)).to_numpy()

        fig_growth = px.line(
            growth_table,
            x="Month",
            y="Revenue Growth (%)",
            markers=True,
            color_discrete_sequence=["#2563EB"],
            title="Month-over-Month Revenue Growth",
            labels={
                "Month": "Month",
                "Revenue Growth (%)": "Revenue Growth (%)"
            },
            custom_data=["Revenue"],
            template="plotly_white"
        )
        fig_growth.update_layout(
            title_x=0.02,
            height=400,
            margin=dict(l=20, r=20, t=55, b=45)
        )
        fig_growth.update_xaxes(title_text="Month", tickangle=-45)
        fig_growth.update_yaxes(ticksuffix="%", title_text="Revenue Growth (%)")
        fig_growth.update_traces(
            connectgaps=False,
            hovertemplate=(
                "<b>%{x}</b><br>Revenue growth: %{y:.2f}%"
                "<br>Revenue: $%{customdata[0]:,.2f}<extra></extra>"
            )
        )
        st.plotly_chart(
            fig_growth,
            width="stretch",
            alt="Month-over-month revenue growth percentage"
        )
        st.dataframe(
            growth_table,
            hide_index=True,
            width="stretch",
            column_config={
                "Revenue": st.column_config.NumberColumn(
                    "Revenue (total)", format="$%.2f"
                ),
                "Revenue Growth (%)": st.column_config.NumberColumn(
                    "Revenue growth", format="%.2f%%"
                )
            }
        )

    with regional_tab:
        st.markdown(
            "Revenue and profit are totals; profit margin is calculated from "
            "each region's total profit and total revenue."
        )
        region_summary = summarize_by_dimension(filtered_df, "Region")
        region_summary = region_summary.sort_values(
            "Revenue", ascending=False, na_position="last"
        )
        region_summary_long = region_summary.melt(
            id_vars="Region",
            value_vars=["Revenue", "Profit"],
            var_name="Measure",
            value_name="Amount"
        )
        fig_regions = px.bar(
            region_summary_long,
            x="Region",
            y="Amount",
            color="Measure",
            barmode="group",
            color_discrete_map={
                "Revenue": "#0F766E",
                "Profit": "#2563EB"
            },
            title="Total Revenue and Profit by Region",
            labels={"Amount": "Total amount ($)", "Region": "Region"},
            template="plotly_white"
        )
        fig_regions.update_layout(
            title_x=0.02,
            height=380,
            margin=dict(l=20, r=20, t=55, b=20),
            legend_title_text=""
        )
        fig_regions.update_yaxes(tickformat="$,.0f")
        st.plotly_chart(
            fig_regions,
            width="stretch",
            alt="Total revenue and profit by region"
        )
        st.dataframe(
            region_summary,
            hide_index=True,
            width="stretch",
            column_config={
                "Revenue": st.column_config.NumberColumn(
                    "Revenue (total)", format="$%.2f"
                ),
                "Profit": st.column_config.NumberColumn(
                    "Profit (total)", format="$%.2f"
                ),
                "Profit Margin (%)": st.column_config.NumberColumn(
                    "Profit margin", format="%.2f%%"
                )
            }
        )

    with discount_tab:
        if "Discount" not in filtered_df.columns:
            st.info(
                "Discount analysis is unavailable because this dataset has "
                "no Discount column."
            )
        else:
            discount_data = filtered_df[
                ["Discount", "Profit", "Sales", "Category", "Order ID"]
            ].dropna(subset=["Discount", "Profit"])
            if discount_data.empty:
                st.info(
                    "No filtered records have both discount and profit values "
                    "to compare."
                )
            else:
                fig_discount = px.scatter(
                    discount_data,
                    x="Discount",
                    y="Profit",
                    color="Category",
                    hover_data={
                        "Sales": ":$,.2f",
                        "Profit": ":$,.2f",
                        "Discount": ":.0%",
                        "Order ID": True
                    },
                    title="Discount and Profit by Order",
                    labels={
                        "Discount": "Discount rate",
                        "Profit": "Profit ($)"
                    },
                    opacity=0.65,
                    color_discrete_sequence=[
                        "#0F766E", "#2563EB", "#F59E0B"
                    ],
                    template="plotly_white"
                )
                fig_discount.update_layout(
                    title_x=0.02,
                    height=450,
                    margin=dict(l=20, r=20, t=55, b=20),
                    legend_title_text="Category"
                )
                fig_discount.update_xaxes(tickformat=".0%")
                fig_discount.update_yaxes(tickformat="$,.0f")
                fig_discount.add_hline(
                    y=0,
                    line_dash="dash",
                    line_color="#64748B"
                )
                st.plotly_chart(
                    fig_discount,
                    width="stretch",
                    alt="Order-level relationship between discount and profit"
                )
                st.caption(
                    "This chart shows association, not proof that discounts "
                    "cause a change in profit."
                )

    with ranking_tab:
        ranking_dimension = next(
            (
                column for column in ("Product Name", "Sub-Category")
                if column in filtered_df.columns
            ),
            None
        )
        if ranking_dimension is None:
            st.info(
                "Product ranking is unavailable because the dataset has "
                "neither Product Name nor Sub-Category."
            )
        else:
            ranking = summarize_by_dimension(
                filtered_df, ranking_dimension
            ).sort_values("Revenue", ascending=False, na_position="last")
            st.caption(
                f"Ranked by total revenue. Profit margin is total profit "
                f"divided by total revenue for each {ranking_dimension.lower()}."
            )
            st.dataframe(
                ranking,
                hide_index=True,
                width="stretch",
                height=520,
                column_config={
                    ranking_dimension: st.column_config.TextColumn(
                        ranking_dimension
                    ),
                    "Revenue": st.column_config.NumberColumn(
                        "Revenue (total)", format="$%.2f"
                    ),
                    "Profit": st.column_config.NumberColumn(
                        "Profit (total)", format="$%.2f"
                    ),
                    "Profit Margin (%)": st.column_config.NumberColumn(
                        "Profit margin", format="%.2f%%"
                    )
                }
            )

    with insights_tab:
        st.markdown(
            "These highlights are recalculated from the currently filtered "
            "records. Revenue and profit are totals; margin is a ratio of totals."
        )
        insight_columns = st.columns(2, gap="medium")

        category_summary = summarize_by_dimension(filtered_df, "Category")
        category_summary = category_summary.dropna(subset=["Revenue"])
        if category_summary.empty:
            best_category_text = "Unavailable"
        else:
            best_category = category_summary.loc[
                category_summary["Revenue"].idxmax()
            ]
            best_category_text = (
                f"{best_category['Category']} "
                f"(${best_category['Revenue']:,.2f} revenue)"
            )
        insight_columns[0].metric(
            "Best-performing category by revenue",
            best_category_text
        )

        if subcategory_summary.empty or subcategory_summary["Profit"].notna().sum() == 0:
            weakest_subcategory_text = "Unavailable"
        else:
            weakest_subcategory = subcategory_summary.loc[
                subcategory_summary["Profit"].idxmin()
            ]
            weakest_subcategory_text = (
                f"{weakest_subcategory['Sub-Category']} "
                f"(${weakest_subcategory['Profit']:,.2f} total profit)"
            )
        insight_columns[1].metric(
            "Weakest-profitability subcategory",
            weakest_subcategory_text,
            help="Identified by the lowest total profit in the filtered records."
        )

        region_insights = summarize_by_dimension(filtered_df, "Region")
        region_insights = region_insights.dropna(subset=["Revenue"])
        if region_insights.empty:
            highest_region_text = "Unavailable"
        else:
            highest_region = region_insights.loc[
                region_insights["Revenue"].idxmax()
            ]
            highest_region_text = (
                f"{highest_region['Region']} "
                f"(${highest_region['Revenue']:,.2f} revenue)"
            )
        insight_columns[0].metric("Highest-revenue region", highest_region_text)

        insight_monthly = filtered_df[["Order Date", "Sales"]].copy()
        insight_monthly["Month"] = (
            insight_monthly["Order Date"].dt.to_period("M")
        )
        insight_monthly = (
            insight_monthly.groupby("Month")["Sales"]
            .sum(min_count=1)
            .dropna()
        )
        if insight_monthly.empty:
            strongest_month_text = "Unavailable"
        else:
            strongest_month = insight_monthly.idxmax()
            strongest_month_text = (
                f"{strongest_month.strftime('%b %Y')} "
                f"(${insight_monthly.loc[strongest_month]:,.2f} revenue)"
            )
        insight_columns[1].metric("Strongest sales month", strongest_month_text)
