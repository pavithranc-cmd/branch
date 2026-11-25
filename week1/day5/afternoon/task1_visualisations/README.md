# Task 1: Five Visualisations
**Week 1 · Day 5 · Weekly Project (Part 2)**

## Submission
* **Notebook:** [notebooks/week1_day5_employee_customer_analysis.ipynb](notebooks/week1_day5_employee_customer_analysis.ipynb), executed, with Markdown headings and no unused cells
* **Figures folder:** [reports/figures/](reports/figures/)

## The five charts
| # | File | Chart | Insight (calculated in the notebook) |
|---|---|---|---|
| 1 | `01_department_salary_bar.png` | Bar: average salary by department | Finance is highest (81,000, 1 person); HR is lowest (46,500), 24 % below the 61,500 company average |
| 2 | `02_salary_distribution_histogram.png` | Histogram: salary distribution | Salaries range from 45,000 to 81,000; mean = median = 61,500, so the distribution is balanced |
| 3 | `03_city_salary_scatter.png` | Scatter: salary by city | Bangalore is lowest (48,500), but its staff are in HR and Sales, so the gap may come from department mix |
| 4 | `04_payroll_concentration_line.png` | Line (sorted values): payroll concentration curve | The lowest-paid 50 % receive 41.3 % of payroll; Gini 0.11, so pay is evenly spread |
| 5 | `05_salary_boxplot.png` | Box plot: salary by department | 0 outliers; IT has the widest range (17,000) and HR the narrowest (3,000) |

The dataset has no experience or date columns, so the scatter uses **city** and the line uses **sorted salaries**. No values were invented.

## Data
Reads `week1/day5/task1_data_cleaning/data/clean_data.csv` (the Part 1 output). The file is not copied.

## How to run (from the repository root)
```powershell
python -m pip install -r week1/day5/afternoon/requirements.txt
python -m nbconvert --to notebook --execute --inplace week1/day5/afternoon/task1_visualisations/notebooks/week1_day5_employee_customer_analysis.ipynb
# or only regenerate the five PNG files:
python week1/day5/afternoon/task1_visualisations/src/employee_report.py
```
