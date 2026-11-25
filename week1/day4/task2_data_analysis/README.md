# Employee Data Analysis: Data Kickoff
**Python & Data Engineering · Week 1 · Day 4 · Task 2**

## Objective
Load an employee dataset with pandas and check its structure and quality
(shape, data types, summary statistics, missing values, duplicates). Then answer
five business questions that the available columns can actually answer.

## Dataset
| Item | Value |
|---|---|
| File | [`data/employees.csv`](data/employees.csv) |
| Source | Training sample dataset, the same file used in Day 4 Task 1 (`../task1_terminal_jupyter/project/data/employees.csv`). It is copied here so Task 2 is self-contained. |
| Size | **8 rows × 5 columns** |
| Columns | `id`, `name`, `department`, `salary`, `city` |

## Folder structure
```text
task2_data_analysis/
├── data/
│   └── employees.csv          # input dataset
├── notebooks/
│   └── data_kickoff.ipynb     # step-by-step exploration (executed, outputs saved)
├── reports/
│   └── data_summary.txt       # created by src/analysis.py
├── src/
│   └── analysis.py            # reusable analysis script
├── README.md
└── requirements.txt
```

## Installation
```bash
# from this folder (week1/day4/task2_data_analysis)
python -m venv .venv                 # optional: create a virtual environment
.venv\Scripts\activate               # Windows   (Mac/Linux: source .venv/bin/activate)
python -m pip install -r requirements.txt
```

## How to run the Python script
```bash
python src/analysis.py
```
The script finds the CSV relative to its own location, so it also works from the repository root
(`python week1/day4/task2_data_analysis/src/analysis.py`) or from any other folder.
It prints every check and saves the same text to `reports/data_summary.txt`.

To analyse a different file: `python src/analysis.py path/to/file.csv`.
If the file is missing, empty or not a valid CSV, the script prints a clear `ERROR:` message and exits with code 1.

## How to open and run the notebook
- **VS Code:** open `notebooks/data_kickoff.ipynb`, choose your Python interpreter as the kernel (top right), then click **Run All**.
- **Browser:** run `jupyter notebook notebooks/data_kickoff.ipynb` and choose **Run → Run All Cells**.
- **Terminal (re-run and save outputs):** `python -m nbconvert --to notebook --execute --inplace notebooks/data_kickoff.ipynb`

## Summary of the initial analysis
| Check | Result |
|---|---|
| Shape | 8 rows × 5 columns |
| Missing values | 0 in every column |
| Duplicate rows / duplicate ids | 0 / 0 |
| Data types | `id`, `salary` → `int64`; `name`, `department`, `city` → `str` |
| Data-quality issue | `city` letter case is inconsistent: `Chennai`, `chennai`, `CHENNAI`. There are 6 raw values but only 4 real cities. Cleaned with `.str.strip().str.title()`. |

## Five business questions and answers
| # | Question | Answer (from this dataset) |
|---|---|---|
| 1 | What is the average salary across all employees? | **61,500** (median 61,500; range 45,000–81,000) |
| 2 | Which department has the highest average salary? | **Finance**, 81,000 (only 1 employee). Then IT 67,000, Sales 58,500, HR 46,500. |
| 3 | Which city has the highest average salary, and how does salary vary between cities? | **Chennai and Hyderabad tie** at 68,000. Then Mumbai 61,500, Bangalore 48,500. |
| 4 | Which employee has the highest salary? | **Rohan** (id 5, Finance, Chennai), 81,000 |
| 5 | How are employees distributed across departments and cities? | IT is the largest department (3). Chennai is the largest city (3). See the cross-tab in the notebook. |

We also checked for missing or duplicate employee records and found none.

## Data dictionary
| Column | Detected data type | Description | Example value |
|---|---|---|---|
| `id` | `int64` | Unique employee identifier (1–8, no duplicates) | `1` |
| `name` | `str` | Employee first name | `Arun` |
| `department` | `str` | Department: Sales, HR, IT or Finance | `Sales` |
| `salary` | `int64` | Employee salary as a whole number. The currency and period are not stated. | `65000` |
| `city` | `str` | City where the employee is based. Letter case is inconsistent. | `Chennai` |

*Types are as reported by pandas 3.x. Older pandas versions show text columns as `object`.*

## Dataset limitations
- **Very small sample (8 rows).** Most groups contain only 1–3 employees, so the averages are not
  statistically meaningful. The project demonstrates the method, not real business findings.
- The salary currency and period (monthly or annual) are not documented.
- There are no date, attrition, performance or experience columns, so the data cannot answer questions about trends, turnover or causes.
- `name` holds first names only. `id` is the reliable unique key.
- `city` must be cleaned before any grouping by city.
