# Python & Data Engineering: Week 1 Assignments

## Structure
```text
branch/
├── week1/
│   └── day4/
│       ├── task1_terminal_jupyter/      # Task 1: terminal, VS Code, Jupyter + Matplotlib charts
│       │   ├── project/
│       │   │   ├── data/employees.csv
│       │   │   ├── notebooks/           # performance_check.ipynb, debug_loop.py
│       │   │   └── reports/             # chennai_employees.txt (grep output)
│       │   ├── notebooks/task1.ipynb    # runs task1.py and shows the charts
│       │   └── task1.py                 # draws the charts into chart_output/
│       │
│       └── task2_data_analysis/         # Task 2: employee data kickoff analysis
│           ├── data/employees.csv
│           ├── notebooks/data_kickoff.ipynb
│           ├── reports/data_summary.txt
│           ├── src/analysis.py
│           ├── README.md
│           └── requirements.txt
│
├── chart_output/                        # PNG charts created by Task 1
├── .gitignore
└── README.md
```

## Setup
```bash
python -m pip install pandas matplotlib jupyter
```

## Quick start (run from the repository root)
| Task | Command |
|---|---|
| Task 1 charts | `python week1/day4/task1_terminal_jupyter/task1.py` |
| Task 2 analysis | `python week1/day4/task2_data_analysis/src/analysis.py` |
| Notebooks | Open the `.ipynb` file in VS Code and click **Run All** |

See [Task 1 README](week1/day4/task1_terminal_jupyter/project/README.md) and
[Task 2 README](week1/day4/task2_data_analysis/README.md) for details.
