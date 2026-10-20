# Data Quality Audit Report
## CodeNova Data Science Internship — Task 2

### 1. Introduction
The purpose of this audit was to assess the quality of the sales dataset, identify potential data quality issues, standardize data types, validate important business rules, and produce a clean dataset suitable for further analysis.

### 2. Dataset Overview
- **Original dataset:** `sales.csv`
- **Original number of rows:** 10,194
- **Number of columns:** 21
- **Missing values:** 0
- **Exact duplicate rows:** 0
- **Duplicate Row IDs:** 0

The original dataset was preserved, and all cleaning operations were performed on a separate copy.

### 3. Data Quality Checks

#### Missing Values
All columns were checked for missing values. No missing values were found, so imputation was unnecessary.

#### Duplicate Records
The dataset was checked for exact duplicate rows and duplicate Row IDs. Neither was found. Therefore, no records were removed for duplication.

#### Data Types
The following standardizations were applied:
- `Order Date` and `Ship Date` were converted to datetime types.
- `Order ID`, `Customer ID`, `Product ID`, and `Postal Code` were converted to string types.
- Relevant descriptive columns, including `Category`, `Region`, and `Segment`, were converted to categorical types.

These changes improve data consistency and support appropriate analysis.

#### Date Validation
Both date columns were checked for invalid dates. Shipping dates were also checked to ensure they did not occur before order dates. No invalid dates or date-order violations were identified.

#### Business Rule Validation
The following checks were performed:
- Sales values must be greater than zero.
- Quantity values must be greater than zero.
- Discount values must fall between 0 and 1.
- Shipping dates must not precede order dates.

No violations were detected for these checks.

### 4. Outlier Detection
The Interquartile Range (IQR) method was used to identify potential outliers in numerical columns.

| Column | Potential outliers | Percentage |
|---|---:|---:|
| Sales | 1,183 | 11.60% |
| Quantity | 175 | 1.72% |
| Discount | 874 | 8.57% |
| Profit | 1,913 | 18.77% |

`Row ID` was excluded from meaningful outlier interpretation because it is an identifier rather than a business measurement.

Potential outliers were retained because extreme values are not necessarily errors. For example, high sales, large quantities, substantial discounts, and negative profits may reflect genuine business transactions. Further investigation would be required before removing or modifying these values.

### 5. Cleaning Actions and Justification

| Action | Reason |
|---|---|
| Preserved the original dataset | Maintains data traceability and allows reproducibility. |
| Converted date columns to datetime | Supports time-based analysis and date validation. |
| Standardized identifier columns as strings | Prevents identifiers from being treated as numerical measurements. |
| Converted selected descriptive columns to categorical types | Improves consistency when working with repeated categories. |
| Checked missing values and duplicates | Confirms whether imputation or duplicate removal is necessary. |
| Validated business rules | Helps identify invalid sales, quantities, discounts, and date relationships. |
| Retained potential outliers | Avoids removing legitimate business information without evidence. |

No records were removed, and no missing values were imputed because the audit did not identify a need for either action.

### 6. Before-and-After Summary

| Quality measure | Before cleaning | After cleaning |
|---|---:|---:|
| Rows | 10,194 | 10,194 |
| Columns | 21 | 21 |
| Missing cells | 0 | 0 |
| Exact duplicate rows | 0 | 0 |
| Duplicate Row IDs | 0 | 0 |
| Invalid dates | 0 | 0 |
| Business-rule violations detected | 0 | 0 |

The primary improvements were data-type standardization and validation. Since the dataset contained no missing values, duplicates, or identified business-rule violations, the row count remained unchanged.

### 7. Output Files
- `data/sales.csv` — original dataset, preserved without modification.
- `output/cleaned_data.csv` — cleaned dataset.
- `output/before_after_comparison.csv` — exported comparison of data quality metrics.
- `data_cleaning.py` — reproducible cleaning and validation script.

### 8. Conclusion
The audit found that the dataset was complete, contained no exact duplicate records, and passed the implemented date and business-rule checks. Data types were standardized, and potential outliers were documented rather than automatically removed.

The resulting dataset is saved separately and is ready for further exploratory data analysis, subject to any additional domain-specific checks required by future analyses.
