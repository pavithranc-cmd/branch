"""Week 1 - Day 5 - Task 1: Data Cleaning.

What this script does
---------------------
1. Loads data/employees.csv (the original Day 4 dataset, unchanged).
2. Records "before" metrics: rows, missing values, duplicates.
3. Standardises text (trim spaces, consistent letter case).
4. Fixes data types (numbers, categories). The id column is validated, never changed.
5. Handles missing values with a documented rule for every column.
6. Removes duplicate records (exact rows, then repeated ids).
7. Detects salary outliers with the IQR rule and FLAGS them (never deletes valid salaries).
8. Saves data/clean_data.csv and reports/cleaning_summary.csv.

How to run (from the repository root, this folder, or VS Code "Run Python File"):
    python week1/day5/task1_data_cleaning/src/cleaning.py

Optional: pass a different input CSV as the first argument.
"""
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths - all relative to this file, so the script works from any folder.
# ---------------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parent            # .../task1_data_cleaning/src
PROJECT_DIR = SRC_DIR.parent                          # .../task1_data_cleaning
RAW_FILE = PROJECT_DIR / "data" / "employees.csv"
CLEAN_FILE = PROJECT_DIR / "data" / "clean_data.csv"
SUMMARY_FILE = PROJECT_DIR / "reports" / "cleaning_summary.csv"

ID_COLUMN = "id"
TEXT_COLUMNS = ["name", "department", "city"]
NUMERIC_COLUMNS = ["salary"]          # measures we analyse (id is an identifier, not a measure)
CATEGORY_COLUMNS = ["department", "city"]
ACRONYMS = {"HR", "IT"}               # keep these upper case ("IT" must not become "It")

# Missing-value rule for every column, with the reason. These rules are applied
# by handle_missing_values(). Strategies: drop | median | mode | flag.
MISSING_VALUE_RULES = {
    "id": ("drop",
           "The unique key. A row without an id cannot be identified or de-duplicated, "
           "and an id must never be invented."),
    "name": ("flag",
             "A personal name cannot be guessed; leave it empty and add a name_was_missing flag."),
    "department": ("flag",
                   "Filling with the mode would put an employee in the wrong department and "
                   "distort every department average; leave empty and flag."),
    "city": ("flag",
             "Filling with the mode would move an employee to the wrong city and distort "
             "city averages; leave empty and flag."),
    "salary": ("median",
               "Numeric and the main measure. A gap is filled with the median of the same "
               "department (the median is not pulled by outliers), and a salary_was_imputed "
               "flag is added so imputed values stay visible."),
}


def load_data(csv_path: Path = RAW_FILE) -> pd.DataFrame:
    """Load a CSV file and fail with a clear message if it is missing or invalid."""
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}\n"
            f"Expected the original file at: {RAW_FILE}"
        )
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"{csv_path} is empty - there is no data to clean.")
    except pd.errors.ParserError as err:
        raise ValueError(f"{csv_path} is not a valid CSV file: {err}")
    if df.empty:
        raise ValueError(f"{csv_path} has a header row but no data rows.")
    return df


def quality_metrics(df: pd.DataFrame) -> dict:
    """Count rows, missing cells and duplicates - used for the before/after table."""
    return {
        "rows": len(df),
        "columns": df.shape[1],
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_ids": int(df[ID_COLUMN].duplicated().sum()),
        "distinct_city_values": int(df["city"].nunique()),
    }


def standardise_department(value):
    """Trim spaces; acronyms upper case (HR, IT), other names title case (Sales)."""
    if pd.isna(value):
        return value
    value = " ".join(str(value).split())          # trim + collapse inner spaces
    return value.upper() if value.upper() in ACRONYMS else value.title()


def standardise_text(df: pd.DataFrame) -> pd.DataFrame:
    """Trim spaces and fix letter case in text columns. The id is not touched."""
    df = df.copy()
    for col in ["name", "city"]:
        # split/join removes leading, trailing and repeated inner spaces
        df[col] = df[col].map(lambda v: v if pd.isna(v) else " ".join(str(v).split()).title())
    df["department"] = df["department"].map(standardise_department)
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to the correct types.

    - id: must be a whole number. It is validated, never modified.
    - salary: numbers stored as text (e.g. "65,000") are converted to numbers.
    - department, city: low-cardinality labels -> 'category' type.
    """
    df = df.copy()
    ids = pd.to_numeric(df[ID_COLUMN], errors="coerce")
    bad_ids = df.loc[ids.isna() & df[ID_COLUMN].notna(), ID_COLUMN]
    if not bad_ids.empty:
        raise ValueError(f"Non-numeric ids found, fix the source file: {bad_ids.tolist()}")
    df[ID_COLUMN] = ids.astype("Int64")             # nullable integer keeps a missing id visible

    for col in NUMERIC_COLUMNS:
        as_text = df[col].astype("string").str.replace(",", "", regex=False).str.strip()
        df[col] = pd.to_numeric(as_text, errors="coerce")
    for col in CATEGORY_COLUMNS:
        df[col] = df[col].astype("category")
    df["name"] = df["name"].astype("string")
    return df


def handle_missing_values(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Apply MISSING_VALUE_RULES column by column and report what was done."""
    df = df.copy()
    actions = []
    for col, (strategy, reason) in MISSING_VALUE_RULES.items():
        n_missing = int(df[col].isna().sum())
        if strategy == "drop" and n_missing:
            df = df[df[col].notna()]
        elif strategy == "median" and n_missing:
            df[f"{col}_was_imputed"] = df[col].isna()
            dept_median = df.groupby("department", observed=True)[col].transform("median")
            df[col] = df[col].fillna(dept_median).fillna(df[col].median())
        elif strategy == "mode" and n_missing:
            df[col] = df[col].fillna(df[col].mode().iloc[0])
        elif strategy == "flag" and n_missing:
            df[f"{col}_was_missing"] = df[col].isna()
        actions.append({"column": col, "missing_before": n_missing, "strategy": strategy,
                        "reason": reason})
    return df, actions


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows, then any repeated id (keep the first record).

    Text is standardised BEFORE this step, so ' chennai' and 'Chennai' count as the same.
    """
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=[ID_COLUMN], keep="first")
    return df.reset_index(drop=True)


def iqr_outliers(series: pd.Series) -> dict:
    """IQR rule: values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are outliers."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = (series < lower) | (series > upper)
    return {"q1": q1, "q3": q3, "iqr": iqr, "lower_bound": lower, "upper_bound": upper,
            "outlier_count": int(mask.sum()), "mask": mask}


def flag_outliers(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Detect outliers in each numeric measure and add an <col>_outlier flag.

    Decision: outliers are FLAGGED, not deleted. A very high or low salary can be a
    real senior or junior salary; only an impossible value (e.g. negative) would be
    removed, and that requires checking with the data owner first.
    """
    df = df.copy()
    results = []
    for col in NUMERIC_COLUMNS:
        stats = iqr_outliers(df[col])
        df[f"{col}_outlier"] = stats.pop("mask")
        stats["column"] = col
        stats["treatment"] = ("No outliers found - nothing changed." if stats["outlier_count"] == 0
                              else "Kept and flagged in salary_outlier; valid salaries are not deleted.")
        results.append(stats)
    return df, results


def build_summary(before: dict, after: dict, outliers: list[dict]) -> pd.DataFrame:
    """Before/after table saved as reports/cleaning_summary.csv."""
    rows = [
        ("Rows", before["rows"], after["rows"], "Rows removed only for duplicates or a missing id."),
        ("Missing values (all cells)", before["missing_values"], after["missing_values"],
         "Each column follows its documented missing-value rule."),
        ("Exact duplicate rows", before["duplicate_rows"], after["duplicate_rows"],
         "Checked again after text standardisation."),
        ("Duplicate ids", before["duplicate_ids"], after["duplicate_ids"], "id is the unique key."),
        ("Distinct city values", before["distinct_city_values"], after["distinct_city_values"],
         "Chennai / chennai / CHENNAI were one city written three ways."),
    ]
    for o in outliers:
        rows.append((
            f"{o['column']} IQR outliers", o["outlier_count"], o["outlier_count"],
            f"Q1={o['q1']:,.0f}, Q3={o['q3']:,.0f}, IQR={o['iqr']:,.0f}, "
            f"bounds [{o['lower_bound']:,.0f}, {o['upper_bound']:,.0f}]. {o['treatment']}",
        ))
    return pd.DataFrame(rows, columns=["metric", "before", "after", "decision_or_note"])


def clean(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Run the full cleaning pipeline in the right order and return details for reporting."""
    before = quality_metrics(df_raw)
    df = standardise_text(df_raw)              # 1. text first, so duplicates are detected correctly
    df = fix_data_types(df)                    # 2. correct types
    df, missing_actions = handle_missing_values(df)   # 3. missing values
    df = remove_duplicates(df)                 # 4. duplicates
    df, outliers = flag_outliers(df)           # 5. outliers (flag, do not delete)
    after = quality_metrics(df)
    summary = build_summary(before, after, outliers)
    return df, {"before": before, "after": after, "missing_actions": missing_actions,
                "outliers": outliers, "summary": summary}


def main(argv: list[str]) -> int:
    input_path = Path(argv[1]) if len(argv) > 1 else RAW_FILE
    try:
        df_raw = load_data(input_path)
    except (FileNotFoundError, ValueError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    df_clean, details = clean(df_raw)

    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(CLEAN_FILE, index=False)
    details["summary"].to_csv(SUMMARY_FILE, index=False)

    b, a = details["before"], details["after"]
    print(f"Rows {b['rows']} -> {a['rows']} | Missing values {b['missing_values']} -> "
          f"{a['missing_values']} | Duplicates {b['duplicate_rows']} -> {a['duplicate_rows']}")
    print("\nMissing-value rules:")
    print(pd.DataFrame(details["missing_actions"]).to_string(index=False))
    print("\nBefore / after summary:")
    print(details["summary"].to_string(index=False))
    print(f"\nSaved: {CLEAN_FILE}\nSaved: {SUMMARY_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
