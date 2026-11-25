"""Week 1 - Day 4 - Task 2: Employee Data Analysis (data kickoff).

What this script does
---------------------
1. Loads data/employees.csv (path is relative to this file, so it works
   from any working directory and on any computer).
2. Prints the first five rows, shape, info(), describe(include="all"),
   missing values, duplicate rows, column names and data types.
3. Answers the five business questions from the README.
4. Saves everything it printed to reports/data_summary.txt.

How to run (from the repository root or from anywhere):
    python week1/day4/task2_data_analysis/src/analysis.py

Optional: pass a different CSV file as the first argument:
    python week1/day4/task2_data_analysis/src/analysis.py path/to/other.csv
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Paths (all relative to this file - no hard-coded Windows paths)
# ---------------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parent          # .../task2_data_analysis/src
PROJECT_DIR = SRC_DIR.parent                        # .../task2_data_analysis
DATA_FILE = PROJECT_DIR / "data" / "employees.csv"
REPORT_FILE = PROJECT_DIR / "reports" / "data_summary.txt"


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load the CSV file and give a clear message if something is wrong."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}\n"
            f"Expected the file at: {DATA_FILE}\n"
            "Check that employees.csv is inside the 'data' folder of the project."
        )
    if not csv_path.is_file():
        raise FileNotFoundError(f"{csv_path} is a folder, not a CSV file.")

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"{csv_path} is empty - there is no data to analyse.")
    except pd.errors.ParserError as err:
        raise ValueError(f"{csv_path} is not a valid CSV file: {err}")

    if df.empty:
        raise ValueError(f"{csv_path} has a header row but no data rows.")
    return df


def section(title: str) -> None:
    """Print a section heading so the output is easy to read."""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def explore(df: pd.DataFrame) -> None:
    """Basic data-kickoff checks."""
    section("1. First five rows - df.head()")
    print(df.head().to_string())

    section("2. Shape - df.shape")
    rows, cols = df.shape
    print(f"{rows} rows x {cols} columns")

    section("3. Info - df.info()")
    df.info()  # info() prints directly to the screen

    section('4. Summary statistics - df.describe(include="all")')
    print(df.describe(include="all").to_string())

    section("5. Missing values per column - df.isna().sum()")
    missing = df.isna().sum()
    print(missing.to_string())
    print(f"Total missing values: {missing.sum()}")

    section("6. Duplicate rows - df.duplicated().sum()")
    print(f"Fully duplicated rows: {df.duplicated().sum()}")
    if "id" in df.columns:
        print(f"Duplicated employee ids: {df['id'].duplicated().sum()}")

    section("7. Column names and data types - df.dtypes")
    print(f"Columns: {list(df.columns)}")
    print(df.dtypes.to_string())

    # Data-quality check: the same city written in different letter cases
    if "city" in df.columns:
        section("8. Data-quality check - city spellings")
        print("Raw city values:", sorted(df["city"].unique()))
        clean = df["city"].str.strip().str.title()
        print("After .str.strip().str.title():", sorted(clean.unique()))
        print(f"Unique cities raw: {df['city'].nunique()}  ->  cleaned: {clean.nunique()}")


def leaders(summary: pd.DataFrame, column: str) -> str:
    """Return every group that has the top value (there can be a tie)."""
    best = summary[column].max()
    names = summary.index[summary[column] == best].tolist()
    tie = " (tie)" if len(names) > 1 else ""
    return f"{', '.join(names)} - {best:,.2f}{tie}"


def business_questions(df: pd.DataFrame) -> None:
    """Answer the five business questions using the real columns."""
    required = {"id", "name", "department", "salary", "city"}
    missing_cols = required - set(df.columns)
    if missing_cols:
        print(f"\nSkipping business questions - missing columns: {sorted(missing_cols)}")
        return

    # Work on a copy so the raw data stays unchanged
    data = df.copy()
    data["city"] = data["city"].str.strip().str.title()  # Chennai/chennai/CHENNAI -> Chennai

    section("BUSINESS QUESTIONS")

    print("\nQ1. What is the average salary across all employees?")
    print(f"    Average salary: {data['salary'].mean():,.2f}  "
          f"(median {data['salary'].median():,.0f}, "
          f"min {data['salary'].min():,}, max {data['salary'].max():,})")

    print("\nQ2. Which department has the highest average salary?")
    by_dept = (data.groupby("department")["salary"]
               .agg(employees="count", avg_salary="mean")
               .sort_values("avg_salary", ascending=False))
    print(by_dept.round(2).to_string())
    print(f"    -> Highest: {leaders(by_dept, 'avg_salary')}")

    print("\nQ3. Which city has the highest average salary? (cities cleaned)")
    by_city = (data.groupby("city")["salary"]
               .agg(employees="count", avg_salary="mean",
                    min_salary="min", max_salary="max")
               .sort_values("avg_salary", ascending=False))
    print(by_city.round(2).to_string())
    print(f"    -> Highest: {leaders(by_city, 'avg_salary')}")

    print("\nQ4. Which employee has the highest salary?")
    top_rows = data[data["salary"] == data["salary"].max()]
    for _, top in top_rows.iterrows():
        print(f"    {top['name']} (id {top['id']}, {top['department']}, {top['city']}) "
              f"- salary {top['salary']:,}")

    print("\nQ5. How many employees work in each department and each city?")
    print(pd.crosstab(data["department"], data["city"],
                      margins=True, margins_name="Total").to_string())


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_FILE
    try:
        df = load_data(csv_path)
    except (FileNotFoundError, ValueError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    # Capture everything that is printed so it can also be saved to a report
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("Employee Data Analysis - Week 1 Day 4 Task 2")
        print(f"Dataset: {csv_path.name}")
        explore(df)
        business_questions(df)
    output = buffer.getvalue()

    print(output)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(output, encoding="utf-8")
    print(f"Report saved to: {REPORT_FILE.relative_to(PROJECT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
