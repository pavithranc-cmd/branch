# Employee Data Analysis Part 1: Data Cleaning & Exploratory Analysis
**Python & Data Engineering · Week 1 · Day 5 · Weekly Project**

## 1. Objective
* **Task 1, Data Cleaning:** make the employee dataset reliable. Handle missing values, fix data types,
  standardise text, remove duplicates and check for outliers. Document a reason for every decision and
  save `clean_data.csv` with a before/after summary.
* **Task 2, Exploratory Data Analysis:** describe the cleaned data. This covers summary statistics, group comparisons,
  correlation, five business questions, a merge with a lookup table and a pivot table.

## 2. Dataset
| Item | Value |
|---|---|
| Source | `week1/day4/task2_data_analysis/data/employees.csv`, the training dataset used on Day 4 (identical to the Day 4 Task 1 file) |
| Size | **8 rows × 5 columns** |
| Columns | `id` (unique key), `name`, `department` (Sales, HR, IT, Finance), `salary` (whole number; currency and period not stated), `city` |
| Not available | dates, age, experience, performance, attrition |

No rows were invented. Every number below is calculated from these 8 real rows.

### Copied files (and why)
| Copy | Copied from | Reason |
|---|---|---|
| `task1_data_cleaning/data/employees.csv` | Day 4 Task 2 `data/employees.csv` | Keeps Task 1 self-contained. It is byte-for-byte identical, and the Day 4 file is not touched. |
| `task2_exploratory_analysis/data/clean_data.csv` | `task1_data_cleaning/data/clean_data.csv` | A snapshot written automatically by `analysis.py`, so the Task 2 folder shows the exact input it analysed. **Task 1's file is the source of truth.** |

`task2_exploratory_analysis/data/department_budget.csv` is a **hand-made lookup table with ILLUSTRATIVE values**.
It is not real company data, and each row says so in its `value_type` column.

## 3. Folder structure
```text
week1/day5/
├── README.md                          # this file (full project report)
├── requirements.txt
├── task1_data_cleaning/
│   ├── data/
│   │   ├── employees.csv              # original data (copy of Day 4)
│   │   └── clean_data.csv             # output of cleaning
│   ├── notebooks/data_cleaning.ipynb  # step-by-step cleaning, executed with outputs
│   ├── src/cleaning.py                # reusable cleaning pipeline
│   ├── reports/cleaning_summary.csv   # before/after table
│   └── README.md
└── task2_exploratory_analysis/
    ├── data/
    │   ├── clean_data.csv             # snapshot of Task 1 output
    │   └── department_budget.csv      # ILLUSTRATIVE lookup table for the merge
    ├── notebooks/exploratory_analysis.ipynb
    ├── src/analysis.py
    ├── reports/
    │   ├── summary_statistics.csv
    │   ├── correlation_matrix.csv
    │   └── pivot_table.csv
    └── README.md
```

## 4. Data-cleaning decisions
**Order matters:** text is standardised before checking duplicates, so `chennai` and `Chennai` are recognised as the same value.

| Step | Column | What we found | Decision and reason |
|---|---|---|---|
| Text | `city` | 6 spellings for 4 cities: `Chennai`, `chennai`, `CHENNAI` | Trim + title case → **Chennai, Bangalore, Mumbai, Hyderabad**. Without this, Chennai would be split into 3 groups. |
| Text | `name` | Already clean | Trim + title case, applied for safety on future data. |
| Text | `department` | Already clean | Trim. Acronyms stay upper case (`HR`, `IT`). Plain `.title()` would wrongly produce `It`. |
| Text | `id` | Unique key | **Not changed.** Only validated as a whole number. |
| Types | `salary` | int64 | `pd.to_numeric`, which also converts text like `"65,000"` if it ever appears. |
| Types | `department`, `city` | text | → `category`: few repeated labels used for grouping. |
| Types | dates | none in dataset | Nothing to convert. |

### Missing values: one rule per column
**The dataset has 0 missing values**, so no value was filled or dropped. The rules below are coded in
`cleaning.MISSING_VALUE_RULES` and tested, so the script is safe to use on future data:

| Column | Rule | Reason |
|---|---|---|
| `id` | **Drop row** | A row without its unique key cannot be identified or de-duplicated, and an id must never be invented. |
| `name` | **Leave + flag** | A person's name cannot be guessed. |
| `department` | **Leave + flag** | Mode would assign people to the wrong department and distort department averages. |
| `city` | **Leave + flag** | Mode would move people to the wrong city and distort city averages. |
| `salary` | **Median of the same department + flag** | Numeric. The median is not pulled by extreme values, and the `salary_was_imputed` flag keeps imputed values visible. |

### Duplicates
Exact duplicate rows are removed first, then any repeated `id` (keeping the first record). Result: **0 found, 0 removed**.

## 5. Before / after summary (`task1_data_cleaning/reports/cleaning_summary.csv`)
**Rows 8 → 8 | Missing values 0 → 0 | Duplicates 0 → 0**

| Metric | Before | After | Note |
|---|---|---|---|
| Rows | 8 | 8 | Rows are removed only for duplicates or a missing id. |
| Missing values (all cells) | 0 | 0 | Each column has a documented rule. |
| Exact duplicate rows | 0 | 0 | Checked again after text standardisation. |
| Duplicate ids | 0 | 0 | `id` is the unique key. |
| Distinct city values | 6 | **4** | The one real fix: city letter case. |
| Salary IQR outliers | 0 | 0 | Bounds [22,875, 97,875]. Nothing changed. |

The original dataset was already in good shape. The only real problem was the inconsistent city case.

## 6. Outlier detection (IQR rule)
Only `salary` is a measurement (`id` is an identifier).

| Q1 | Q3 | IQR | Lower bound (Q1 − 1.5·IQR) | Upper bound (Q3 + 1.5·IQR) | Outliers |
|---|---|---|---|---|---|
| 51,000 | 69,750 | 18,750 | 22,875 | 97,875 | **0** |

All salaries (45,000 to 81,000) are inside the bounds, so **nothing was removed or changed**. The pipeline never deletes
a valid high or low salary. It adds a `salary_outlier` True/False flag instead, because an unusual salary can be real
(a senior or junior role). The notebook includes a box plot showing the bounds.

## 7. Summary statistics (`reports/summary_statistics.csv`)
| Column | Count | Mean | Median | Min | Max | Std |
|---|---|---|---|---|---|---|
| salary | 8 | 61,500 | 61,500 | 45,000 | 81,000 | 12,950.46 |

`salary` is the only numeric measure. `id` and the `salary_outlier` flag are excluded on purpose.

## 8. Group analysis (`groupby().agg()`)
| City | Employees | Avg salary | Min | Max |
|---|---|---|---|---|
| Chennai | 3 | 68,000 | 58,000 | 81,000 |
| Hyderabad | 1 | 68,000 | 68,000 | 68,000 |
| Mumbai | 2 | 61,500 | 48,000 | 75,000 |
| Bangalore | 2 | 48,500 | 45,000 | 52,000 |

| Department | Employees | Avg salary | Min | Max |
|---|---|---|---|---|
| Finance | 1 | 81,000 | 81,000 | 81,000 |
| IT | 3 | 67,000 | 58,000 | 75,000 |
| Sales | 2 | 58,500 | 52,000 | 65,000 |
| HR | 2 | 46,500 | 45,000 | 48,000 |

## 9. Correlation (`df.corr(numeric_only=True)`, `reports/correlation_matrix.csv`)
|  | id | salary |
|---|---|---|
| id | 1.000 | −0.036 |
| salary | −0.036 | 1.000 |

**A top-three list is not possible.** There are only two numeric columns, so only one pair exists, and that pair is not meaningful
because `id` is a row number, not a measurement. No relationship is claimed. Real measures such as age, experience or rating
would be needed. Also, **correlation does not prove causation**: even a strong correlation only shows that two values move together.

## 10. Business questions (reused from Day 4 Task 2)
| # | Question | Calculated answer | Interpretation |
|---|---|---|---|
| 1 | What is the average salary across all employees? | Mean **61,500**, median 61,500, range 45,000–81,000 | The top salary is 1.8 × the lowest. |
| 2 | Which department has the highest average salary? | **Finance, 81,000** (1 employee), then IT 67,000 (3) | Among departments with more than one employee, IT pays the most. HR pays the least (46,500). |
| 3 | Which city has the highest average salary? | **Chennai and Hyderabad, 68,000**. Lowest is Bangalore, 48,500 | A 19,500 gap. Without cleaning, Chennai would show 3 different averages (65,000 / 58,000 / 81,000). |
| 4 | Which employee has the highest salary? | **Rohan** (id 5, Finance, Chennai), 81,000 | 19,500 above the average. |
| 5 | How are employees distributed? | IT is the largest department (3). Chennai is the largest city (3) | Most city/department pairs have 0 or 1 employees. |

Each answer is calculated with pandas in the notebook. Nothing is typed in by hand.

## 11. Merge (`pd.merge`)
* **Lookup:** `department_budget.csv` (department → `annual_budget`, `budget_owner`). The values are **ILLUSTRATIVE**.
* **Key:** `department`, which exists in both tables and is unique in the lookup (checked with `validate="many_to_one"`).
* **Join type:** **left**, so every employee is kept even if their department were missing from the lookup.
  `indicator=True` shows the result: all **8 of 8** employees matched (`_merge = both`).
* **Example use:** total salary as a % of the illustrative budget. Finance 20.2%, HR 31.0%, IT 22.3%, Sales 19.5%.
  These show how a merge enables new analysis. They are not real findings.

## 12. Pivot table (`pd.pivot_table`, `reports/pivot_table.csv`)
Mean salary, rows = `city`, columns = `department`:

| city | Finance | HR | IT | Sales |
|---|---|---|---|---|
| Bangalore | | 45,000 | | 52,000 |
| Chennai | 81,000 | | 58,000 | 65,000 |
| Hyderabad | | | 68,000 | |
| Mumbai | | 48,000 | 75,000 | |

Empty cells mean **no employee** has that combination. They are left empty on purpose, not filled with 0.

## 13. Installation
```bash
# from week1/day5
python -m venv .venv                  # optional
.venv\Scripts\activate                # Windows (Mac/Linux: source .venv/bin/activate)
python -m pip install -r requirements.txt
```

## 14. How to run
```bash
# from the repository root (or any folder: the paths are relative to each script)
python week1/day5/task1_data_cleaning/src/cleaning.py          # run first, writes clean_data.csv
python week1/day5/task2_exploratory_analysis/src/analysis.py   # reads Task 1 output
```
If a file is missing, the scripts print a clear `ERROR:` message and exit with code 1.

**Notebooks:** open them in VS Code, pick your Python interpreter as the kernel and click **Run All**. Or run from the terminal:
```bash
python -m nbconvert --to notebook --execute --inplace week1/day5/task1_data_cleaning/notebooks/data_cleaning.ipynb
python -m nbconvert --to notebook --execute --inplace week1/day5/task2_exploratory_analysis/notebooks/exploratory_analysis.ipynb
```
The notebooks import the functions from `src/`, so notebooks and scripts produce identical files (verified).

## 15. Limitations and conclusions
* **8 employees is too small for business decisions.** Most groups have 1 to 3 people, so one salary changes a group average a lot.
* Only one numeric measure, so no meaningful correlation analysis is possible.
* The salary currency and period are unknown. The budget values are illustrative.
* The missing-value, duplicate and outlier rules were not triggered by this data. They were tested in code and are ready for larger files with the same columns.

**Conclusion:** the data was mostly clean. Fixing the city letter case was the step that changed results, because without it the
city analysis would be wrong. After cleaning, the average salary is 61,500. Finance and IT pay the most and HR the least.
Chennai and Hyderabad have the highest average salaries.
