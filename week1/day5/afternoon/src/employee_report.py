"""Week 1 - Day 5 - Part 2: shared data + chart helpers.

Used by BOTH:
  * week1/day5/afternoon/notebooks/week1_day5_employee_customer_analysis.ipynb
  * week1/day5/afternoon/streamlit_app/app.py
so the notebook, the saved PNG files and the dashboard always show the same numbers.

Data source (no copies are made):
  week1/day5/task1_data_cleaning/data/clean_data.csv   <- output of Part 1 cleaning.py
If that file is missing, the Part 1 cleaning pipeline is re-run in memory on the raw file.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, PercentFormatter

# ---------------------------------------------------------------------------
# Paths - all relative to this file, so the project works on any computer.
# ---------------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parents[1]     # .../week1/day5/afternoon
DAY5_DIR = PROJECT_DIR.parent                          # .../week1/day5
PART1_DIR = DAY5_DIR / "task1_data_cleaning"
CLEAN_FILE = PART1_DIR / "data" / "clean_data.csv"
FIGURES_DIR = PROJECT_DIR / "reports" / "figures"

# Salary currency and pay period are NOT stated in the dataset, so we never guess them.
SALARY_LABEL = "Salary (currency not stated)"

# ---------------------------------------------------------------------------
# One consistent palette (validated default palette, light mode).
# Every chart uses ONE series colour; departments/cities are named on the axis
# or by direct labels, so nothing depends on telling colours apart.
# ---------------------------------------------------------------------------
PRIMARY = "#257de0"      # blue - the data
ACCENT = "#f47230"       # orange - one highlighted reference (company average)
NEUTRAL = "#8c8c8c"      # grey - reference lines, equality line
TEXT = "#191919"
TEXT_MUTED = "#666666"
GRID = "#e6e6e6"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def load_clean_data() -> pd.DataFrame:
    """Return the cleaned employee data produced by Part 1."""
    if CLEAN_FILE.is_file():
        df = pd.read_csv(CLEAN_FILE)
    else:
        # Re-use the Part 1 cleaning logic instead of writing it again.
        sys.path.insert(0, str(PART1_DIR / "src"))
        import cleaning  # noqa: E402  (Part 1 module)
        df, _ = cleaning.clean(cleaning.load_data())
    df["department"] = df["department"].astype(str)
    df["city"] = df["city"].astype(str)
    df["salary"] = pd.to_numeric(df["salary"])
    return df


def group_summary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Headcount and salary statistics per group, highest average first."""
    return (
        df.groupby(column)["salary"]
        .agg(employees="count", avg_salary="mean", median_salary="median",
             min_salary="min", max_salary="max")
        .sort_values("avg_salary", ascending=False)
    )


def iqr_bounds(series: pd.Series) -> dict:
    """Q1, Q3 and the 1.5 x IQR outlier fences for a numeric column."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return {"q1": q1, "q3": q3, "iqr": iqr,
            "lower": q1 - 1.5 * iqr, "upper": q3 + 1.5 * iqr}


def payroll_curve(df: pd.DataFrame) -> pd.DataFrame:
    """Employees sorted from lowest to highest salary, with cumulative shares (%).

    Starts with a (0 %, 0 %) point so the line begins at the origin.
    """
    salaries = np.sort(df["salary"].to_numpy())
    n = len(salaries)
    return pd.DataFrame({
        "employee_share": np.arange(n + 1) / n * 100,
        "payroll_share": np.concatenate([[0], np.cumsum(salaries)]) / salaries.sum() * 100,
    })


def gini(df: pd.DataFrame) -> float:
    """Gini coefficient of salaries: 0 = everyone paid the same, 1 = one person gets everything."""
    x = np.sort(df["salary"].to_numpy(dtype=float))
    n = len(x)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))


# ---------------------------------------------------------------------------
# Chart style
# ---------------------------------------------------------------------------
def apply_style() -> None:
    """Readable fonts, light gridlines, no chart junk. Call once at the start."""
    plt.rcParams.update({
        "figure.figsize": (9, 5.5),
        "figure.dpi": 100,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlepad": 12,
        "axes.labelsize": 11,
        "axes.labelcolor": TEXT,
        "axes.edgecolor": "#bdbdbd",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": TEXT_MUTED,
        "ytick.color": TEXT_MUTED,
        "text.color": TEXT,
        "legend.frameon": False,
    })


def _thousands(value, _pos=None) -> str:
    return f"{value:,.0f}"


THOUSANDS = FuncFormatter(_thousands)


def save_figure(fig, filename: str) -> Path:
    """Save a figure as a high-resolution PNG in reports/figures/."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.savefig(path, facecolor="white")
    return path


# ---------------------------------------------------------------------------
# The five charts. Each takes the (possibly filtered) DataFrame, returns a Figure.
# ---------------------------------------------------------------------------
def plot_department_salary_bar(df: pd.DataFrame):
    """1. Bar chart - average salary by department."""
    summary = group_summary(df, "department")
    company_avg = df["salary"].mean()
    fig, ax = plt.subplots()
    labels = [f"{d}\n(n={n})" for d, n in zip(summary.index, summary["employees"])]
    bars = ax.bar(labels, summary["avg_salary"], color=PRIMARY, width=0.6,
                  edgecolor="white", linewidth=2, label="Department average")
    # Value labels sit in the middle of each bar, well away from the average line.
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in summary["avg_salary"]],
                 label_type="center", color="white", fontsize=11, fontweight="bold")
    ax.axhline(company_avg, color=ACCENT, linestyle="--", linewidth=2,
               label=f"Company average ({company_avg:,.0f})")
    ax.set_title("Average Salary by Department")
    ax.set_xlabel("Department (number of employees)")
    ax.set_ylabel(f"Average {SALARY_LABEL.lower()}")
    ax.yaxis.set_major_formatter(THOUSANDS)
    ax.set_ylim(0, summary["avg_salary"].max() * 1.15)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    return fig


def plot_salary_histogram(df: pd.DataFrame):
    """2. Histogram - salary distribution with fixed 10,000-wide bins."""
    low = np.floor(df["salary"].min() / 10_000) * 10_000
    high = np.ceil(df["salary"].max() / 10_000) * 10_000
    if high == low:
        high = low + 10_000
    bins = np.arange(low, high + 10_000, 10_000)
    mean, median = df["salary"].mean(), df["salary"].median()

    fig, ax = plt.subplots()
    ax.hist(df["salary"], bins=bins, color=PRIMARY, edgecolor="white", linewidth=2,
            label="Employees per salary band")
    if np.isclose(mean, median):
        ax.axvline(mean, color=ACCENT, linestyle="--", linewidth=2,
                   label=f"Mean = median ({mean:,.0f})")
    else:
        ax.axvline(mean, color=ACCENT, linestyle="--", linewidth=2, label=f"Mean ({mean:,.0f})")
        ax.axvline(median, color=NEUTRAL, linestyle=":", linewidth=2,
                   label=f"Median ({median:,.0f})")
    ax.set_title("Employee Salary Distribution")
    ax.set_xlabel(f"{SALARY_LABEL} - bands of 10,000")
    ax.set_ylabel("Number of employees (frequency)")
    ax.set_xticks(bins)
    ax.xaxis.set_major_formatter(THOUSANDS)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    return fig


def plot_city_salary_scatter(df: pd.DataFrame):
    """3. Scatter plot - each employee's salary by city (experience is not in the dataset)."""
    city_order = group_summary(df, "city").index.tolist()
    x_pos = {city: i for i, city in enumerate(city_order)}
    company_avg = df["salary"].mean()

    fig, ax = plt.subplots()
    ax.scatter(df["city"].map(x_pos), df["salary"], s=90, color=PRIMARY,
               edgecolor="white", linewidth=2, zorder=3, label="Employee")
    for _, row in df.iterrows():   # direct labels: name and department
        ax.annotate(f"{row['name']} ({row['department']})",
                    (x_pos[row["city"]], row["salary"]), xytext=(9, -4),
                    textcoords="offset points", fontsize=9, color=TEXT_MUTED)
    # City average tick - only for cities with 2+ employees (one person IS the average).
    city_stats = df.groupby("city")["salary"].agg(["mean", "count"])
    drawn = False
    for i, city in enumerate(city_order):
        if city_stats.loc[city, "count"] > 1:
            ax.hlines(city_stats.loc[city, "mean"], i - 0.25, i + 0.25, color=NEUTRAL,
                      linewidth=2.5, zorder=2, label=None if drawn else "City average (2+ employees)")
            drawn = True
    ax.axhline(company_avg, color=ACCENT, linestyle="--", linewidth=1.5,
               label=f"Company average ({company_avg:,.0f})")
    ax.set_title("Employee Salary by City")
    ax.set_xlabel("City (ordered by average salary, highest first)")
    ax.set_ylabel(SALARY_LABEL)
    ax.set_xticks(range(len(city_order)), city_order)
    ax.set_xlim(-0.5, len(city_order) - 0.1)
    ax.yaxis.set_major_formatter(THOUSANDS)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower left")
    return fig


def plot_payroll_curve_line(df: pd.DataFrame):
    """4. Line chart - cumulative share of payroll (dataset has no joining dates)."""
    curve = payroll_curve(df)
    fig, ax = plt.subplots()
    ax.plot([0, 100], [0, 100], color=NEUTRAL, linestyle="--", linewidth=1.5,
            label="Perfectly equal pay")
    ax.plot(curve["employee_share"], curve["payroll_share"], color=PRIMARY,
            linewidth=2, marker="o", markersize=7, markeredgecolor="white",
            label="Actual payroll")
    # Direct label at the half-way point
    half = curve.iloc[(curve["employee_share"] - 50).abs().argmin()]
    ax.annotate(f"Lowest-paid {half['employee_share']:.0f}% of staff\n"
                f"receive {half['payroll_share']:.1f}% of payroll",
                (half["employee_share"], half["payroll_share"]), xytext=(15, -45),
                textcoords="offset points", fontsize=10, color=TEXT,
                arrowprops={"arrowstyle": "-", "color": TEXT_MUTED})
    ax.set_title("Payroll Concentration Curve")
    ax.set_xlabel("Cumulative share of employees, lowest salary first (%)")
    ax.set_ylabel("Cumulative share of total payroll (%)")
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left")
    return fig


def plot_salary_boxplot(df: pd.DataFrame):
    """5. Box plot - salary distribution by department, with every employee shown."""
    order = group_summary(df, "department").index.tolist()
    groups = [df.loc[df["department"] == d, "salary"] for d in order]
    bounds = iqr_bounds(df["salary"])

    fig, ax = plt.subplots()
    ax.boxplot(groups, widths=0.5, patch_artist=True,
               boxprops={"facecolor": "#d6e6f9", "edgecolor": PRIMARY, "linewidth": 1.5},
               medianprops={"color": PRIMARY, "linewidth": 2.5},
               whiskerprops={"color": PRIMARY}, capprops={"color": PRIMARY},
               flierprops={"marker": "D", "markerfacecolor": ACCENT, "markeredgecolor": ACCENT})
    for i, values in enumerate(groups, start=1):   # show the real points (n is small)
        ax.scatter([i] * len(values), values, color=PRIMARY, s=45, zorder=3,
                   edgecolor="white", linewidth=1.5,
                   label="Individual employee" if i == 1 else None)
    ax.axhline(bounds["upper"], color=NEUTRAL, linestyle=":", linewidth=1.5,
               label=f"Company outlier fences (IQR rule: {bounds['lower']:,.0f} - {bounds['upper']:,.0f})")
    ax.axhline(bounds["lower"], color=NEUTRAL, linestyle=":", linewidth=1.5)
    ax.set_xticks(range(1, len(order) + 1),
                  [f"{d}\n(n={len(g)})" for d, g in zip(order, groups)])
    ax.set_title("Salary Distribution by Department")
    ax.set_xlabel("Department (number of employees)")
    ax.set_ylabel(SALARY_LABEL)
    ax.yaxis.set_major_formatter(THOUSANDS)
    ax.grid(axis="x", visible=False)
    ax.set_ylim(min(bounds["lower"], df["salary"].min()) - 5_000,
                max(bounds["upper"], df["salary"].max()) + 5_000)
    ax.legend(loc="lower right", bbox_to_anchor=(1, 0.08), fontsize=9)
    return fig


# Filename -> chart function, in presentation order.
CHARTS = {
    "01_department_salary_bar.png": plot_department_salary_bar,
    "02_salary_distribution_histogram.png": plot_salary_histogram,
    "03_city_salary_scatter.png": plot_city_salary_scatter,
    "04_payroll_concentration_line.png": plot_payroll_curve_line,
    "05_salary_boxplot.png": plot_salary_boxplot,
}


if __name__ == "__main__":
    # Quick way to regenerate all five PNG files: python week1/day5/afternoon/src/employee_report.py
    apply_style()
    data = load_clean_data()
    for name, chart in CHARTS.items():
        print("Saved:", save_figure(chart(data), name))
        plt.close("all")
