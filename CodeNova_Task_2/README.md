# Data Cleaning and Quality Audit

**CodeNova Data Science Internship — Task 2**

## Project Overview

This project focuses on assessing and improving the quality of a sales dataset through systematic data cleaning, validation, and outlier detection.

The goal is to identify potential data quality issues, standardize data types, validate business rules, document cleaning decisions, and produce a clean dataset suitable for further analysis.

## Objectives

- Inspect the dataset for missing values and duplicate records.
- Identify and standardize inappropriate data types.
- Validate date fields and important business rules.
- Detect potential numerical outliers using the Interquartile Range (IQR) method.
- Document cleaning decisions and justify whether records should be retained, modified, or removed.
- Generate a before-and-after comparison of data quality metrics.
- Produce a reproducible Python cleaning script and a data quality audit report.

## Dataset Description

The project uses a sales dataset containing **10,194 rows and 21 columns**.

The dataset includes information about:
- Orders and shipping dates
- Customers and customer segments
- Product categories and subcategories
- Sales, quantity, discount, and profit
- Geographic regions and locations

The original dataset is stored in `data/sales.csv` and is preserved without modification.

## Tools and Technologies

- **Python** — data cleaning and validation
- **Pandas** — data manipulation and quality checks
- **Pathlib** — file and directory management
- **Visual Studio Code** — development environment

## Data Quality Checks

The following checks were performed:

### 1. Missing Values
All columns were checked for missing values. No missing values were found.

### 2. Duplicate Records
The dataset was checked for exact duplicate rows and duplicate Row IDs. No duplicates were identified.

### 3. Data Type Standardization
- Converted `Order Date` and `Ship Date` to datetime.
- Converted `Order ID`, `Customer ID`, `Product ID`, and `Postal Code` to string types.
- Converted selected descriptive columns, such as `Category`, `Region`, and `Segment`, to categorical types.

### 4. Date Validation
Checked for invalid dates and shipping dates occurring before order dates. No violations were detected.

### 5. Business Rule Validation
Checked that:
- Sales values were greater than zero.
- Quantities were greater than zero.
- Discounts were between 0 and 1.
- Shipping dates did not precede order dates.

No violations were detected by these checks.

### 6. Outlier Detection
The Interquartile Range (IQR) method was used to identify potential outliers in numerical columns.

| Column | Potential Outliers | Percentage |
|---|---:|---:|
| Sales | 1,183 | 11.60% |
| Quantity | 175 | 1.72% |
| Discount | 874 | 8.57% |
| Profit | 1,913 | 18.77% |

Potential outliers were retained because extreme values are not automatically errors. They may represent genuine business transactions, including high-value orders, large quantities, discounts, or losses.

## Cleaning Decisions

The audit found no missing values, exact duplicate records, or violations of the implemented validation rules. Therefore, no records needed to be removed or imputed.

The main cleaning actions were data type standardization and validation. The original dataset was preserved, and the cleaned dataset was exported separately.

## Project Structure

```text
CodeNova_Task_2/
├── data/
│   └── sales.csv
├── output/
│   ├── cleaned_data.csv
│   └── before_after_comparison.csv
├── data_cleaning.py
├── DATA_QUALITY_AUDIT_REPORT.md
└── README.md
```

## How to Run the Project

### Prerequisites

Install Python and Pandas if they are not already installed.

```bash
pip install pandas
```

### Run the Cleaning Script

Open the terminal in the project directory and run:

```bash
python data_cleaning.py
```

The script reads the original dataset, performs the cleaning and validation steps, and saves the output files in the `output/` directory.

## Output Files

| File | Description |
|---|---|
| `output/cleaned_data.csv` | Dataset with standardized data types and completed validation checks |
| `output/before_after_comparison.csv` | Exported before-and-after quality metrics |
| `DATA_QUALITY_AUDIT_REPORT.md` | Detailed report of findings, outliers, and cleaning decisions |
| `data_cleaning.py` | Reproducible cleaning and validation script |

## Key Findings

- The original dataset contains 10,194 rows and 21 columns.
- No missing values were found.
- No exact duplicate rows or duplicate Row IDs were identified.
- Date and business-rule validation checks passed.
- Potential outliers were identified using the IQR method and retained for further investigation.
- No records were removed during the cleaning process.
- The cleaned dataset was saved separately from the original data.

## Conclusion

This project demonstrates a systematic approach to data quality assessment, cleaning, validation, and documentation. The process improves consistency by standardizing data types and checking important business rules while preserving potentially meaningful observations.

The resulting dataset is ready for further exploratory data analysis, subject to additional checks appropriate to the intended analysis.

## Author

**Veronica A.**

Data Science Intern — CodeNova
