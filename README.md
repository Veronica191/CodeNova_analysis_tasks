# Sales Data Analysis

## Project Objective

This project analyses sales transactions to show how the business is performing. It looks at revenue, profit, sales over time, product performance, and differences between regions. The findings can help guide decisions about products, pricing, inventory, marketing, and regional planning.

## Dataset Overview

The notebook reads the dataset from `data/sales.csv`.

- **Records:** 10,194 rows
- **Columns:** 21 original fields
- **Date range in the dataset:** 3 January 2023 to 30 December 2026
- **Data fields include:** order and shipping dates, shipping mode, customer and segment information, country/region, city, state/province, sales region, product category and sub-category, sales, quantity, discount, and profit.

The notebook checks for missing values and duplicate rows. Its saved results show none. It also converts the order and shipping dates into date format so they can be used in time-based analysis.

## Tools and Libraries

- **Python** — analysis workflow and calculations
- **Pandas** — loading, cleaning, grouping, and analysing tabular data
- **NumPy** — numerical operations
- **Matplotlib** — charts and plots
- **Seaborn** — statistical and categorical visualisations
- **Jupyter Notebook** — interactive analysis and documentation

## Key Business Metrics

The notebook reports these overall results:

| Metric | Result |
|---|---:|
| Total revenue (sales) | $2,326,534.35 |
| Total profit | $292,296.81 |
| Overall profit margin | 12.56% |
| Units sold | 38,654 |
| Unique orders | 5,111 |
| Average order value | $455.20 |

**What this means:** For every $100 in recorded sales, the business earned about $12.56 in profit. These totals include all records in the dataset, including dates that may have been in the future when the notebook ran. See **Data Limitations and Considerations**.

## Key Findings

### Product category performance

| Category | Revenue | Profit | Units sold | Profit margin |
|---|---:|---:|---:|---:|
| Technology | $839,893.28 | $146,543.38 | 7,017 | 17.45% |
| Furniture | $754,747.76 | $19,730.00 | 8,369 | 2.61% |
| Office Supplies | $731,893.31 | $126,023.44 | 23,268 | 17.22% |

- **Technology** generated the highest revenue and total profit among the three categories.
- **Office Supplies** had the highest unit volume.
- **Furniture** had a much lower profit margin (2.61%) than Technology and Office Supplies, so its costs, discounts, and product-level performance merit closer review.

### Sub-category performance

- **Chairs** recorded the highest sub-category revenue: **$335,768.25**.
- **Copiers** recorded the highest total sub-category profit: **$56,093.94**.
- **Labels** had the highest reported sub-category profit margin: **43.90%**.
- **Tables** recorded the largest sub-category loss: **-$17,753.21**.
- **Bookcases** recorded a loss of **-$3,632.07**, and **Supplies** recorded a loss of **-$1,171.39**.
- **Phones** generated **$331,842.64** in revenue and **$45,050.83** in profit.
- **Binders** had the highest unit volume among the listed sub-categories, with **6,071 units**, and a positive profit margin of **15.16%**.

These results suggest two useful next steps: investigate why some sub-categories are losing money, and find out what is contributing to the high margins for products such as Labels, Paper, and Copiers.

### Monthly and quarterly trends

The notebook calculates average revenue, profit, and units sold for each quarter across the years in the dataset:

| Quarter | Average revenue | Average profit | Average units sold |
|---|---:|---:|---:|
| Q1 | $91,623.21 | $12,284.23 | 1,316.75 |
| Q2 | $112,580.94 | $13,995.94 | 2,010.50 |
| Q3 | $154,926.82 | $18,547.63 | 2,670.50 |
| Q4 | $222,502.61 | $28,246.40 | 3,665.75 |

- Average revenue, profit, and units sold rise from Q1 to Q4 in this summary.
- Q1 has the lowest averages, while Q4 has the highest.
- Average Q4 revenue is approximately **2.43 times** average Q1 revenue.
- Across calendar months, **November** had the highest average revenue in the notebook's monthly seasonality table (**$88,166.50**), followed by December (**$82,554.54**) and September (**$77,220.92**).
- February had the lowest average revenue in that table (**$14,937.81**).

This pattern may be useful for planning, but it does not prove that seasonal changes caused the differences. Check the 2026 records before using these averages to make business decisions.

### Geographic performance

| Region | Revenue | Profit | Units sold | Unique orders |
|---|---:|---:|---:|---:|
| West | $739,813.61 | $110,798.82 | 12,466 | 1,635 |
| East | $691,828.17 | $94,883.26 | 11,159 | 1,475 |
| Central | $503,170.67 | $39,865.31 | 8,820 | 1,179 |
| South | $391,721.90 | $46,749.43 | 6,209 | 822 |

- **West** generated the highest revenue and profit among the four regions.
- **East** ranked second in revenue.
- **South** generated the lowest revenue and had the fewest unique orders.
- Results vary by region. Comparing customer demand, product mix, discounts, and marketing activity may help explain the differences.

## Strategic Business Recommendations

1. **Review Furniture's profitability.** Furniture had a 2.61% profit margin despite its high revenue. Review its costs, discounts, shipping costs (if available), and individual product margins.
2. **Investigate unprofitable sub-categories.** Check pricing, discounts, and costs for Tables, Bookcases, and Supplies before changing prices, promotions, or the product range.
3. **Understand high-margin products.** Find out what contributes to the margins for Labels, Paper, and Copiers. Consider whether the same approaches could work for similar products, and verify the results rather than assuming they will.
4. **Use monthly trends carefully when planning.** Average sales are higher in September, November, and December in this analysis. Confirm the pattern using complete, date-checked data before setting inventory or campaign budgets.
5. **Compare regions.** Explore why the West and East perform better than the Central and South regions. Compare product mix, order volume, discounts, and customer segments.
6. **Measure profit as well as revenue.** High revenue does not always mean a sale is profitable. Consider profit, profit margin, and sales volume together when comparing products, categories, and regions.
7. **Check dates before reporting.** Determine whether 2026 records after the analysis date are valid future records, data-entry errors, or synthetic data. Then recalculate the key metrics and trends.

## Data Limitations and Considerations

- **Records dated in the future:** In the saved notebook run, **1,121 records** had order dates after **12 October 2026**. The dataset runs through **30 December 2026**, and those records represented about **$251,632.87** in sales. These counts depend on when the notebook was run, so rerun the date check before using them. Confirm the records are valid and consider comparing results with and without them.
- **Comparing time periods:** The dataset covers 2023–2026. If 2026 is incomplete or contains future records, comparisons with earlier years may be misleading. The same issue can affect monthly and quarterly averages.
- **Data quality checks:** The notebook's initial checks found no missing values or duplicate rows. This does not confirm that all values are accurate or logically consistent.
- **Descriptive analysis only:** The results show patterns in the recorded data. They do not explain what caused changes in revenue or profit.
- **Limited business context:** The dataset supports analysis by product, customer segment, and region, but may not include all costs or external factors needed to explain performance.

## How to Run the Notebook

### 1. Requirements

Install Python and Jupyter Notebook, or use JupyterLab. The notebook requires:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`

### 2. Project structure

Place the project files in this structure:

```text
sales-analysis/
├── sales_analysis.ipynb
└── data/
    └── sales.csv
```

The notebook looks for the CSV at `data/sales.csv`, relative to the project folder. If the file is somewhere else, update the path in the notebook.

### 3. Install dependencies

In a terminal, run:

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter
```

### 4. Start Jupyter

From the project folder, start Jupyter:

```bash
jupyter notebook
```

Open `sales_analysis.ipynb` in the browser.

### 5. Run the analysis

Run the notebook cells in order, from top to bottom. It loads the CSV, checks data quality, converts date fields, calculates business metrics, and creates summaries and charts for categories, sub-categories, time periods, and regions.

Before relying on the results, review the future-dated records and rerun the relevant cells after deciding how those records should be handled.

## Project Status

This README describes the analysis and results currently in `sales_analysis.ipynb`. The category, sub-category, quarterly, monthly, and regional figures come from the notebook outputs. Where the data does not establish a cause, this README presents it as a question to investigate, not as a confirmed conclusion.
