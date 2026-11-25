# Task 2: Report and Presentation
**Week 1 · Day 5 · Weekly Project (Part 2)**

## Submission
| Item | File |
|---|---|
| One-page summary (problem, data, 3 insights, 2 recommendations, limitations) | [reports/summary_report.md](reports/summary_report.md) |
| Notebook exported as HTML (nbconvert) | [reports/analysis_report.html](reports/analysis_report.html) |
| 5-minute presentation with speaker notes | [reports/presentation.md](reports/presentation.md) |
| README with how to run | [root README](../../../../README.md) |
| Merged Pull Request link | *add the link here after the PR is merged* |

## Re-create the HTML report (from the repository root)
Run the Task 1 notebook first, then export it into this folder:
```powershell
python -m nbconvert --to html week1/day5/afternoon/task1_visualisations/notebooks/week1_day5_employee_customer_analysis.ipynb --output analysis_report --output-dir week1/day5/afternoon/task2_report_presentation/reports
```
