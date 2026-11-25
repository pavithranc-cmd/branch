"""Week 1 - Day 5 - Streamlit dashboard for the employee salary analysis.

Run from the repository root:
    streamlit run streamlit_app/app.py

Uses the same cleaned data (Part 1 output) and the same chart functions
(src/employee_report.py) as the notebook, so the numbers always match.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

# Make src/ importable no matter which folder Streamlit is started from
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import employee_report as er  # noqa: E402

st.set_page_config(page_title="Employee Salary Dashboard", page_icon="📊", layout="wide")
er.apply_style()


@st.cache_data
def get_data():
    return er.load_clean_data()


df_all = get_data()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Employee Salary Dashboard")
st.caption("Week 1 · Day 5 · Weekly Project (Part 2). Data: Part 1 cleaned employee dataset "
           f"({len(df_all)} employees). Salary currency is not stated in the source data.")

# ---------------------------------------------------------------------------
# Filter (one row, above the charts)
# ---------------------------------------------------------------------------
departments = sorted(df_all["department"].unique())
selected = st.multiselect("Filter by department", departments, default=departments)
df = df_all[df_all["department"].isin(selected)]

if df.empty:
    st.warning("Select at least one department to see the dashboard.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI metrics
# ---------------------------------------------------------------------------
dept = er.group_summary(df, "department")
company_avg = df_all["salary"].mean()
avg = df["salary"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Employees", f"{len(df)}")
k2.metric("Average salary", f"{avg:,.0f}",
          delta=f"{avg - company_avg:+,.0f} vs all staff" if len(df) < len(df_all) else None)
k3.metric("Median salary", f"{df['salary'].median():,.0f}")
k4.metric("Salary range", f"{df['salary'].min():,.0f} – {df['salary'].max():,.0f}")
k5.metric("Top-paying department", dept.index[0],
          help=f"Average {dept['avg_salary'].iloc[0]:,.0f} from {dept['employees'].iloc[0]} employee(s)")

# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
left, right = st.columns(2)
with left:
    st.subheader("Average salary by department")
    fig = er.plot_department_salary_bar(df)
    st.pyplot(fig)
    plt.close(fig)
with right:
    st.subheader("Salary distribution")
    fig = er.plot_salary_histogram(df)
    st.pyplot(fig)
    plt.close(fig)

with st.expander("More charts: salary by city, payroll concentration, box plot"):
    for chart in (er.plot_city_salary_scatter, er.plot_payroll_curve_line, er.plot_salary_boxplot):
        fig = chart(df)
        st.pyplot(fig)
        plt.close(fig)

# ---------------------------------------------------------------------------
# Data overview
# ---------------------------------------------------------------------------
st.subheader("Department summary")
st.dataframe(dept.style.format("{:,.0f}"), width="stretch")

st.subheader("Employee data")
st.dataframe(df.drop(columns="salary_outlier"), hide_index=True, width="stretch")

st.caption("Limitations: only 8 employees, so one salary moves a group average a lot. The dataset has no "
           "experience or joining-date columns.")
