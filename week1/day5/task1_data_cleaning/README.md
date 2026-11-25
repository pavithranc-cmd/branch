# Task 1: Data Cleaning (Week 1 · Day 5)
Cleans `data/employees.csv` (the unchanged Day 4 dataset) and saves `data/clean_data.csv` and `reports/cleaning_summary.csv`.

**Result:** Rows 8 → 8 | Missing values 0 → 0 | Duplicates 0 → 0 | City spellings 6 → 4 | Salary IQR outliers 0

| File | Purpose |
|---|---|
| `src/cleaning.py` | Reusable pipeline: text → types → missing values → duplicates → outliers (flag only) |
| `notebooks/data_cleaning.ipynb` | Step-by-step walkthrough with outputs and a salary box plot |
| `reports/cleaning_summary.csv` | Before/after table with outlier bounds and decisions |

Run (from anywhere): `python week1/day5/task1_data_cleaning/src/cleaning.py`

All decisions and reasons are listed in the [Day 5 README](../README.md#4-data-cleaning-decisions).
