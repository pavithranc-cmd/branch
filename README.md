# Employee Data Analysis: Visualisations, Report and Presentation
**Python & Data Engineering · Week 1 · Weekly Project (Day 5, Part 2)**

## Project overview
This repository holds my Week 1 training work. The weekly project analyses a small employee dataset in two parts:
* **Part 1** (`week1/day5/`) cleans the data and explores it with tables. See the [Part 1 README](week1/day5/README.md).
* **Part 2** (`week1/day5/afternoon/`, documented in this README) turns the cleaned data into **five charts**, an executed **Jupyter notebook**, an **HTML report**,
  a **one-page summary**, a **Streamlit dashboard** and a **five-minute presentation**.

## Objectives
1. Build five clear, labelled, high-resolution visualisations from the cleaned data.
2. Write findings and recommendations that come from real calculations, not assumptions.
3. Share the results as a notebook, an HTML report, a one-page summary, a dashboard and a presentation.

## Datasets
| File | Rows × columns | Description |
|---|---|---|
| `week1/day5/task1_data_cleaning/data/employees.csv` | 8 × 5 | Original employee data: `id`, `name`, `department`, `salary`, `city` |
| `week1/day5/task1_data_cleaning/data/clean_data.csv` | 8 × 6 | **Used by Part 2.** Part 1 output: standardised city names plus a `salary_outlier` flag |
| `week1/day5/task2_exploratory_analysis/data/department_budget.csv` | 4 × 4 | Illustrative lookup table from Part 1 (not used in Part 2) |

Part 2 reads the Part 1 file directly. **No dataset was copied.** There is no customer or order data in the repository.
The dataset has **no experience or joining-date column**, so two requested charts were replaced (see below). No values were invented.

## Repository structure
```text
branch/
├── week1/
│   ├── day4/
│   │   ├── task1_terminal_jupyter/                    # terminal, VS Code, Jupyter + Matplotlib basics
│   │   └── task2_data_analysis/                       # employee data kickoff analysis
│   └── day5/
│       ├── task1_data_cleaning/                       # Part 1: cleaning (clean_data.csv lives here)
│       ├── task2_exploratory_analysis/                # Part 1: exploratory analysis
│       └── afternoon/                                 # Part 2
│           ├── task1_visualisations/                  # TASK 1: five visualisations
│           │   ├── notebooks/week1_day5_employee_customer_analysis.ipynb
│           │   ├── reports/figures/                   # five 200-dpi PNG charts
│           │   ├── src/employee_report.py             # shared data loading + chart functions
│           │   └── README.md
│           ├── task2_report_presentation/             # TASK 2: report and presentation
│           │   ├── reports/summary_report.md          # one-page summary
│           │   ├── reports/analysis_report.html       # HTML export of the Task 1 notebook
│           │   ├── reports/presentation.md            # 5-minute talk with speaker notes
│           │   └── README.md
│           ├── bonus_streamlit_app/app.py             # BONUS: Streamlit dashboard
│           └── requirements.txt
├── chart_output/                                      # Day 4 Task 1 charts
├── .gitignore
└── README.md
```

## Technologies
Python 3 · pandas · NumPy · Matplotlib · Jupyter Notebook / nbconvert · Streamlit · Git and GitHub

## The five visualisations
| # | File (`week1/day5/afternoon/task1_visualisations/reports/figures/`) | Chart | Notes |
|---|---|---|---|
| 1 | `01_department_salary_bar.png` | Bar: average salary by department | Includes a company-average reference line |
| 2 | `02_salary_distribution_histogram.png` | Histogram: salary distribution | Bands of 10,000 |
| 3 | `03_city_salary_scatter.png` | Scatter: salary by city | **Replaces "experience vs salary"** (no experience column) |
| 4 | `04_payroll_concentration_line.png` | Line: payroll concentration curve | **Replaces "hiring trend"** (no joining-date column) |
| 5 | `05_salary_boxplot.png` | Box plot: salary by department | Shows every employee and the IQR outlier fences |

All charts use one colour palette and say "currency not stated" on the salary axis, because the source data does not give the currency.

## Key findings
1. **Department drives pay.** Finance 81,000 (1 person), IT 67,000, Sales 58,500, HR 46,500. HR is **24 % below** the 61,500 company average.
2. **Pay is evenly spread and there are no outliers.** Mean = median = 61,500, the lowest-paid 50 % get 41.3 % of payroll, Gini = 0.11, 0 IQR outliers.
3. **The city gap (Chennai/Hyderabad 68,000 vs Bangalore 48,500) probably reflects department mix.** Bangalore's staff are in HR and Sales.

**Recommendations:** benchmark HR pay against the market, and collect experience, joining date, job level and currency for a larger sample.
See [summary_report.md](week1/day5/afternoon/task2_report_presentation/reports/summary_report.md) for details.

## Install dependencies (Windows PowerShell)
```powershell
cd path\to\branch
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # if blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
python -m pip install --upgrade pip
python -m pip install -r week1/day5/afternoon/requirements.txt
```

## Task 1: run the notebook
Open `week1/day5/afternoon/task1_visualisations/notebooks/week1_day5_employee_customer_analysis.ipynb` in VS Code or Jupyter and click **Run All**. You can also run it from the terminal:
```powershell
python -m nbconvert --to notebook --execute --inplace week1/day5/afternoon/task1_visualisations/notebooks/week1_day5_employee_customer_analysis.ipynb
```
To regenerate only the five PNG files:
```powershell
python week1/day5/afternoon/task1_visualisations/src/employee_report.py
```

## Task 2: export the HTML report
```powershell
python -m nbconvert --to html week1/day5/afternoon/task1_visualisations/notebooks/week1_day5_employee_customer_analysis.ipynb --output analysis_report --output-dir week1/day5/afternoon/task2_report_presentation/reports
```
(`jupyter nbconvert --to html ...` works the same way if the `jupyter` command is on your PATH.)

## Bonus: launch the Streamlit dashboard
```powershell
streamlit run week1/day5/afternoon/bonus_streamlit_app/app.py
# or: python -m streamlit run week1/day5/afternoon/bonus_streamlit_app/app.py
```
It opens at http://localhost:8501. Use the department filter at the top. The KPIs and charts update automatically.

## Earlier work (Day 4 and Day 5 Part 1)
| Task | Command (from the repository root) |
|---|---|
| Day 4 Task 1 charts | `python week1/day4/task1_terminal_jupyter/task1.py` |
| Day 4 Task 2 analysis | `python week1/day4/task2_data_analysis/src/analysis.py` |
| Day 5 Part 1 cleaning | `python week1/day5/task1_data_cleaning/src/cleaning.py` |
| Day 5 Part 1 EDA | `python week1/day5/task2_exploratory_analysis/src/analysis.py` |

## GitHub contribution workflow
```powershell
git checkout main
git pull origin main
git checkout -b feature/<short-description>      # one branch per task
# ...make changes, run the notebook, check the outputs...
git status                                       # review what changed
git add <files>                                  # add only the files you intend to commit
git commit -m "Describe the change"
git push -u origin feature/<short-description>
# On GitHub: open a Pull Request into main, ask for a review, and merge only after approval
```
