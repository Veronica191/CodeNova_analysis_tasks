
from pathlib import Path
import pandas as pd

# ==========================================
# 1. DEFINE FILE PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_FILE = PROJECT_DIR / "data" / "sales.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Original dataset not found: {INPUT_FILE}"
    )

# ==========================================
# 2. LOAD ORIGINAL DATA
# ==========================================

df_before = pd.read_csv(INPUT_FILE)

# Preserve a separate working copy.
df_clean = df_before.copy()

print("Original dataset loaded successfully.")
print("Original shape:", df_before.shape)

# ==========================================
# 3. RECORD INITIAL QUALITY METRICS
# ==========================================

def quality_metrics(data):
    numeric = data.select_dtypes(include="number")

    metrics = {
        "Rows": len(data),
        "Columns": len(data.columns),
        "Missing_Cells": int(data.isna().sum().sum()),
        "Exact_Duplicate_Rows": int(data.duplicated().sum()),
        "Duplicate_Row_IDs": (
            int(data["Row ID"].duplicated().sum())
            if "Row ID" in data.columns else None
        ),
    }

    for col in numeric.columns:
        metrics[f"{col}_Mean"] = data[col].mean()
        metrics[f"{col}_Median"] = data[col].median()
        metrics[f"{col}_Min"] = data[col].min()
        metrics[f"{col}_Max"] = data[col].max()
        metrics[f"{col}_Std"] = data[col].std()

    for col in data.columns:
        metrics[f"{col}_Missing"] = int(data[col].isna().sum())

    return metrics


before_metrics = quality_metrics(df_before)

# ==========================================
# 4. STANDARDIZE COLUMN DATA TYPES
# ==========================================

date_columns = ["Order Date", "Ship Date"]

for col in date_columns:
    df_clean[col] = pd.to_datetime(
        df_clean[col], errors="coerce"
    )

identifier_columns = [
    "Order ID", "Customer ID", "Product ID", "Postal Code"
]

for col in identifier_columns:
    df_clean[col] = df_clean[col].astype("string")

categorical_columns = [
    "Ship Mode",
    "Segment",
    "Country/Region",
    "City",
    "State/Province",
    "Region",
    "Category",
    "Sub-Category",
]

for col in categorical_columns:
    df_clean[col] = df_clean[col].astype("category")

# ==========================================
# 5. CHECK FOR INVALID VALUES
# ==========================================

invalid_date_count = sum(
    df_clean[col].isna().sum()
    for col in date_columns
)

if invalid_date_count > 0:
    raise ValueError(
        "Date conversion created missing dates. "
        "Investigate these records before proceeding."
    )

if (df_clean["Sales"] <= 0).any():
    raise ValueError(
        "Non-positive sales values found. "
        "Investigate before deciding how to handle them."
    )

if (df_clean["Quantity"] <= 0).any():
    raise ValueError(
        "Non-positive quantities found. "
        "Investigate before deciding how to handle them."
    )

if (
    (df_clean["Discount"] < 0)
    | (df_clean["Discount"] > 1)
).any():
    raise ValueError(
        "Discount values outside the 0-1 range found."
    )

if (
    df_clean["Ship Date"] < df_clean["Order Date"]
).any():
    raise ValueError(
        "Shipping dates before order dates found."
    )

# ==========================================
# 6. REMOVE CONFIRMED EXACT DUPLICATES
# ==========================================

duplicates_removed = int(df_clean.duplicated().sum())

df_clean = df_clean.drop_duplicates().copy()

# ==========================================
# 7. RECORD FINAL QUALITY METRICS
# ==========================================

after_metrics = quality_metrics(df_clean)

comparison = pd.DataFrame([
    {"Stage": "Before Cleaning", **before_metrics},
    {"Stage": "After Cleaning", **after_metrics},
])

# ==========================================
# 8. SAVE OUTPUT FILES
# ==========================================

cleaned_file = OUTPUT_DIR / "cleaned_data.csv"
comparison_file = OUTPUT_DIR / "before_after_comparison.csv"

df_clean.to_csv(cleaned_file, index=False)
comparison.to_csv(comparison_file, index=False)

print("\n--- CLEANING SUMMARY ---")
print("Original rows:", len(df_before))
print("Cleaned rows:", len(df_clean))
print("Duplicates removed:", duplicates_removed)
print("Missing cells before:", before_metrics["Missing_Cells"])
print("Missing cells after:", after_metrics["Missing_Cells"])
print("Output dataset:", cleaned_file)
print("Comparison table:", comparison_file)

print("\nCleaning completed successfully.")
