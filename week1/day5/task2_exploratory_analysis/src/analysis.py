"""Week 1 - Day 5 - Task 2: Exploratory Data Analysis.

What this script does
---------------------
1. Loads the cleaned dataset produced by Task 1
   (../task1_data_cleaning/data/clean_data.csv) and saves a snapshot copy in
   data/clean_data.csv so this folder shows exactly which input was analysed.
2. Summary statistics (mean, median, min, max, std) -> reports/summary_statistics.csv
3. Group analysis with groupby().agg() by city and by department.
4. Correlation matrix with df.corr(numeric_only=True) -> reports/correlation_matrix.csv
5. Answers the five business questions from Day 4 Task 2.
6. Merges data/department_budget.csv (ILLUSTRATIVE values) on 'department'.
7. Pivot table city x department, mean salary -> reports/pivot_table.csv

How to run (from the repository root, this folder, or VS Code "Run Python File"):
    python week1/day5/task2_exploratory_analysis/src/analysis.py
Run Task 1 (cleaning.py) first so clean_data.csv exists.
"""
import shutil
import sys
from itertools import combinations
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths - relative to this file, so the script works from any folder.
# ---------------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parent                 # .../task2_exploratory_analysis/src
PROJECT_DIR = SRC_DIR.parent                               # .../task2_exploratory_analysis
DAY5_DIR = PROJECT_DIR.parent                              # .../week1/day5
TASK1_CLEAN_FILE = DAY5_DIR / "task1_data_cleaning" / "data" / "clean_data.csv"
CLEAN_COPY = PROJECT_DIR / "data" / "clean_data.csv"
BUDGET_FILE = PROJECT_DIR / "data" / "department_budget.csv"
REPORTS_DIR = PROJECT_DIR / "reports"

ID_COLUMN = "id"
FLAG_SUFFIXES = ("_outlier", "_was_missing", "_was_imputed")   # helper flags from Task 1


def read_csv_checked(path: Path, hint: str) -> pd.DataFrame:
    """Read a CSV, raising a clear error if the file does not exist or is empty."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}\n{hint}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"{path} has no data rows.")
    return df


def load_clean_data(path: Path = TASK1_CLEAN_FILE, save_copy: bool = True) -> pd.DataFrame:
    """Load Task 1's clean_data.csv and restore the column types CSV cannot store."""
    df = read_csv_checked(path, "Run Task 1 first: python week1/day5/task1_data_cleaning/src/cleaning.py")
    for col in ["department", "city"]:
        df[col] = df[col].astype("category")
    if save_copy:
        CLEAN_COPY.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, CLEAN_COPY)          # snapshot of the analysed input
    return df


def measure_columns(df: pd.DataFrame) -> list[str]:
    """Numeric columns that are real measures: not the id and not True/False flag columns."""
    numeric = df.select_dtypes(include="number").columns
    return [c for c in numeric if c != ID_COLUMN and not c.endswith(FLAG_SUFFIXES)]


# ---------------------------------------------------------------------------
# A. Summary statistics
# ---------------------------------------------------------------------------
def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Mean, median, min, max and standard deviation for every measure column."""
    stats = df[measure_columns(df)].agg(["count", "mean", "median", "min", "max", "std"]).T
    stats.index.name = "column"
    return stats.round(2)


# ---------------------------------------------------------------------------
# B. Group analysis
# ---------------------------------------------------------------------------
def group_summary(df: pd.DataFrame, by: str) -> pd.DataFrame:
    """Employee count and salary statistics per category, highest average first."""
    out = df.groupby(by, observed=True).agg(
        employees=(ID_COLUMN, "count"),
        avg_salary=("salary", "mean"),
        median_salary=("salary", "median"),
        min_salary=("salary", "min"),
        max_salary=("salary", "max"),
        total_salary=("salary", "sum"),
    )
    return out.sort_values("avg_salary", ascending=False).round(2)


# ---------------------------------------------------------------------------
# C. Correlation
# ---------------------------------------------------------------------------
def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation of the numeric columns (helper True/False flags removed)."""
    flags = [c for c in df.columns if c.endswith(FLAG_SUFFIXES)]
    return df.drop(columns=flags).corr(numeric_only=True)


def top_correlations(corr: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Strongest pairs of DIFFERENT columns, each pair once (no self or mirror pairs)."""
    pairs = [(a, b, corr.loc[a, b]) for a, b in combinations(corr.columns, 2)]
    out = pd.DataFrame(pairs, columns=["column_1", "column_2", "correlation"])
    out["abs_correlation"] = out["correlation"].abs()
    return out.sort_values("abs_correlation", ascending=False).head(n).reset_index(drop=True)


# ---------------------------------------------------------------------------
# D. Business questions (the five questions from Day 4 Task 2)
# ---------------------------------------------------------------------------
def business_questions(df: pd.DataFrame) -> list[dict]:
    """Answer each Day 4 question with a calculated result."""
    by_dept = df.groupby("department", observed=True)["salary"].agg(["mean", "count"])
    by_city = df.groupby("city", observed=True)["salary"].mean()
    top = df.loc[df["salary"].idxmax()]
    top_cities = by_city[by_city == by_city.max()].index.tolist()
    return [
        {"question": "Q1. What is the average salary across all employees?",
         "answer": f"Mean {df['salary'].mean():,.0f}; median {df['salary'].median():,.0f}; "
                   f"range {df['salary'].min():,.0f}-{df['salary'].max():,.0f}."},
        {"question": "Q2. Which department has the highest average salary?",
         "answer": f"{by_dept['mean'].idxmax()} ({by_dept['mean'].max():,.0f}, "
                   f"{int(by_dept.loc[by_dept['mean'].idxmax(), 'count'])} employee(s))."},
        {"question": "Q3. Which city has the highest average salary?",
         "answer": f"{' and '.join(top_cities)} ({by_city.max():,.0f}); lowest is "
                   f"{by_city.idxmin()} ({by_city.min():,.0f})."},
        {"question": "Q4. Which employee has the highest salary?",
         "answer": f"{top['name']} (id {top[ID_COLUMN]}, {top['department']}, {top['city']}): "
                   f"{top['salary']:,.0f}."},
        {"question": "Q5. How are employees distributed across departments and cities?",
         "answer": f"Largest department: {df['department'].value_counts().idxmax()} "
                   f"({df['department'].value_counts().max()}); largest city: "
                   f"{df['city'].value_counts().idxmax()} ({df['city'].value_counts().max()})."},
    ]


# ---------------------------------------------------------------------------
# E. Merge
# ---------------------------------------------------------------------------
def merge_budget(df: pd.DataFrame, budget: pd.DataFrame) -> pd.DataFrame:
    """LEFT join employees to the department budget lookup on 'department'.

    validate="many_to_one": many employees share one department row; pandas raises an
    error if the lookup accidentally has the same department twice.
    indicator=True adds a _merge column so unmatched employees are visible.
    """
    emp = df.copy()
    emp["department"] = emp["department"].astype(str)   # same key type on both sides
    return pd.merge(emp, budget, on="department", how="left",
                    validate="many_to_one", indicator=True)


def budget_by_department(merged: pd.DataFrame) -> pd.DataFrame:
    """Salary total vs the illustrative budget, per department."""
    out = merged.groupby("department").agg(employees=(ID_COLUMN, "count"),
                                           total_salary=("salary", "sum"),
                                           annual_budget=("annual_budget", "first"))
    out["salary_pct_of_budget"] = (100 * out["total_salary"] / out["annual_budget"]).round(1)
    return out


# ---------------------------------------------------------------------------
# F. Pivot table
# ---------------------------------------------------------------------------
def salary_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean salary with city as rows and department as columns.

    Empty cells mean no employee exists for that city/department pair - they are left
    empty on purpose (filling them with 0 would wrongly suggest a salary of 0).
    """
    return pd.pivot_table(df, index="city", columns="department", values="salary",
                          aggfunc="mean", observed=True)


def main() -> int:
    try:
        df = load_clean_data()
        budget = read_csv_checked(BUDGET_FILE, "department_budget.csv should be in the data folder.")
    except (FileNotFoundError, ValueError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 120)

    print(f"Loaded {len(df)} rows x {df.shape[1]} columns from {TASK1_CLEAN_FILE.name}")

    stats = summary_statistics(df)
    stats.to_csv(REPORTS_DIR / "summary_statistics.csv")
    print("\nA. Summary statistics\n", stats)

    print("\nB. Group analysis by city\n", group_summary(df, "city"))
    print("\nB. Group analysis by department\n", group_summary(df, "department"))

    corr = correlation_matrix(df)
    corr.round(4).to_csv(REPORTS_DIR / "correlation_matrix.csv")
    print("\nC. Correlation matrix\n", corr.round(4))
    print("Numeric measures available:", measure_columns(df))
    print("Strongest pairs:\n", top_correlations(corr))
    print("NOTE: only 'salary' is a real numeric measure; 'id' is an identifier, so the "
          "id-salary value is not a meaningful relationship. Correlation does not prove causation.")

    print("\nD. Business questions")
    for qa in business_questions(df):
        print(f"  {qa['question']}\n     -> {qa['answer']}")

    merged = merge_budget(df, budget)
    print("\nE. Merge (left join on department) - budget values are ILLUSTRATIVE")
    print(merged[[ID_COLUMN, "name", "department", "salary", "annual_budget", "_merge"]])
    print(budget_by_department(merged))

    pivot = salary_pivot(df)
    pivot.to_csv(REPORTS_DIR / "pivot_table.csv")
    print("\nF. Pivot table: mean salary, city x department\n", pivot)

    print(f"\nReports saved in {REPORTS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
