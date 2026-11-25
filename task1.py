"""Week 1 - Day 4 - Task 1: Charts with Matplotlib.

Draws 4 charts from employees.csv and saves each as a PNG:
  1. bar chart   - average salary per department (values shown on bars)
  2. histogram   - salaries, 5 bins
  3. scatter     - id vs salary, coloured by department, with legend
  4. line chart  - monthly sales Jan-Jun with markers
Bonus: all four on one figure with plt.subplots(2, 2).

How to run (in the normal terminal, NOT at the >>> Python prompt):
    python charts.py
It also works with the VS Code Run button or pasted into a Jupyter cell.
"""
import os

import matplotlib.pyplot as plt
import pandas as pd

# ---------- 1. load the data ----------
# Put the full path to your Day 3 file here if you want, e.g.
# CSV_FILE = r"E:\GEN AI PYTHON\GenAi_Training\day3\employees.csv"
CSV_FILE = None

# Folder this script is in (falls back to the current folder in Jupyter)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

csv_path = CSV_FILE
if not csv_path:
    # Search: next to the script, then the whole project folder (one level up)
    search_roots = [script_dir, os.getcwd(), os.path.dirname(script_dir)]
    for root in search_roots:
        for folder, _subdirs, files in os.walk(root):
            if "employees.csv" in files:
                csv_path = os.path.join(folder, "employees.csv")
                break
        if csv_path:
            break

def load_employees(path):
    """Read the CSV robustly: auto-detect the separator (, ; or tab),
    skip broken lines, and tidy column names and salary values."""
    # find the real header row (first line mentioning "salary"), skipping any title lines
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    header_row = next((i for i, line in enumerate(lines) if "salary" in line.lower()), 0)
    df = pd.read_csv(path, sep=None, engine="python", on_bad_lines="warn",
                     encoding_errors="replace", skipinitialspace=True,
                     skiprows=header_row, skip_blank_lines=True)
    # tidy column names: " Salary " -> "salary", "Emp ID" -> "emp_id"
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    # accept common alternative column names
    aliases = {
        "id": ["emp_id", "employee_id", "empid", "employee_number", "sno", "s.no"],
        "department": ["dept", "department_name", "dept_name"],
        "salary": ["monthly_salary", "annual_salary", "salary_inr", "pay", "income"],
    }
    for target, options in aliases.items():
        if target not in df.columns:
            for opt in options:
                if opt in df.columns:
                    df = df.rename(columns={opt: target})
                    break
    missing = [c for c in ["department", "salary"] if c not in df.columns]
    if missing:
        raise SystemExit(f"\n{path} has columns {list(df.columns)}\n"
                         f"but the charts need {missing}. Rename those columns in the CSV, "
                         f"or tell me the column names and I'll adapt the script.")
    # clean values: "85,000" / "Rs 85000" -> 85000 ; " sales " -> "Sales"
    df["salary"] = pd.to_numeric(
        df["salary"].astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
    df["department"] = df["department"].astype(str).str.strip().str.title()
    df = df.dropna(subset=["salary"])
    df = df[~df["department"].isin(["", "Nan", "None"])]
    if "id" not in df.columns:
        df["id"] = range(1, len(df) + 1)
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])
    return df


if csv_path:
    df = load_employees(csv_path)
    print(f"Loaded {csv_path}  ->  {len(df)} rows, columns: {list(df.columns)}")
else:
    print("employees.csv not found - using built-in sample data")
    df = pd.DataFrame({
        "id": list(range(1, 21)),
        "department": ["Engineering", "Marketing", "Engineering", "HR", "Sales",
                       "Engineering", "Sales", "Marketing", "HR", "Engineering",
                       "Sales", "Marketing", "Engineering", "HR", "Sales",
                       "Marketing", "Engineering", "HR", "Sales", "Marketing"],
        "salary": [85000, 62000, 92000, 54000, 58000, 98000, 61000, 67000, 50000, 88000,
                   64000, 71000, 105000, 57000, 55000, 69000, 95000, 52000, 66000, 73000],
    })

# Output folder for the PNG files (created next to this script)
out_dir = os.path.join(script_dir, "chart_output")
os.makedirs(out_dir, exist_ok=True)

avg_salary = df.groupby("department")["salary"].mean().sort_values(ascending=False)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 15, 14, 18, 22, 25]
departments = sorted(df["department"].unique())
colors = dict(zip(departments, plt.cm.tab10.colors))


# ---------- 2. one function per chart ----------
def bar_chart(ax):
    bars = ax.bar(avg_salary.index, avg_salary.values,
                  color=[colors[d] for d in avg_salary.index])
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in avg_salary.values], padding=3)
    ax.set_title("Average Salary per Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary (INR)")
    ax.set_ylim(0, avg_salary.max() * 1.15)


def histogram(ax):
    ax.hist(df["salary"], bins=5, color="steelblue", edgecolor="black")
    ax.set_title("Salary Distribution (5 bins)")
    ax.set_xlabel("Salary (INR)")
    ax.set_ylabel("Number of Employees")


def scatter(ax):
    for dept in departments:
        sub = df[df["department"] == dept]
        ax.scatter(sub["id"], sub["salary"], label=dept, color=colors[dept], s=60)
    ax.set_title("Employee ID vs Salary by Department")
    ax.set_xlabel("Employee ID")
    ax.set_ylabel("Salary (INR)")
    ax.set_ylim(df["salary"].min() * 0.9, df["salary"].max() * 1.2)
    ax.legend(title="Department", loc="upper center", ncol=len(departments), fontsize=8)


def line_chart(ax):
    ax.plot(months, sales, marker="o", linestyle="-", color="darkorange", label="Sales")
    ax.set_title("Monthly Sales (Jan - Jun)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales (units)")
    ax.legend()
    ax.grid(alpha=0.3)


charts = {
    "bar_avg_salary_by_department.png": bar_chart,
    "histogram_salary.png": histogram,
    "scatter_id_vs_salary.png": scatter,
    "line_monthly_sales.png": line_chart,
}

# ---------- 3. save every chart as its own PNG ----------
for filename, draw in charts.items():
    fig, ax = plt.subplots(figsize=(8, 5))
    draw(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, filename), dpi=150)
    plt.close(fig)
    print("saved", os.path.join(out_dir, filename))

# ---------- 4. bonus: all four charts on one figure ----------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, draw in zip(axes.flat, charts.values()):
    draw(ax)
fig.suptitle("Employee Dashboard", fontsize=16, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(out_dir, "dashboard_2x2.png"), dpi=150)
plt.show()
print("saved", os.path.join(out_dir, "dashboard_2x2.png"))
