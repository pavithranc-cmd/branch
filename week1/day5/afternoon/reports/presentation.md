# Employee Salary Analysis – 5-Minute Presentation
**Week 1 · Day 5 · Weekly Project (Part 2)**

Charts are in `week1/day5/afternoon/reports/figures/`. Open the dashboard with `streamlit run week1/day5/afternoon/streamlit_app/app.py` if you want to show it live.

---

## Slide 1 – Introduction and Problem (30 seconds)
**On screen**
* Employee Salary Analysis: Part 2
* Question: *How is pay distributed across departments and cities, and what should we do about it?*

**Speaker notes**
> "In Part 1, I cleaned our employee dataset. Today I will show what the clean data tells us about salaries.
> I want to answer three questions: which departments pay more, is pay fair across the team, and what should we check next."

---

## Slide 2 – Dataset and Method (45 seconds)
**On screen**
* 8 employees · 4 departments · 4 cities · salary is the only number
* Part 1 cleaning: fixed city spelling (6 versions → 4), 0 missing values, 0 duplicates
* Tools: pandas, NumPy, Matplotlib, Jupyter, Streamlit
* No experience or joining-date column, so two charts were replaced

**Speaker notes**
> "The dataset is small: 8 employees with name, department, salary and city. In Part 1, the only real problem was the city spelling,
> for example 'chennai' and 'CHENNAI'. I fixed that, so we now have 4 clean cities.
> The brief asked for an experience chart and a hiring-trend chart, but those columns do not exist. I did not invent data.
> I made a salary-by-city scatter and a payroll curve instead. All charts come from one shared Python file,
> so the notebook, the report and the dashboard always show the same numbers."

---

## Slide 3 – Three Charts and Insights (2 minutes)

### Chart A: Average Salary by Department (`01_department_salary_bar.png`), about 40 seconds
> "Finance has the highest average at 81,000, but that is just one person. IT is next at 67,000 with three people.
> HR is the lowest at 46,500. That is 15,000, or 24 percent, below the company average of 61,500."

### Chart B: Salary by Department Box Plot (`05_salary_boxplot.png`), about 40 seconds
> "This box plot shows every employee as a dot. IT has the widest spread, 17,000. HR is very tight, only 3,000.
> Every HR salary is below every other department's salary. The dotted lines are the outlier fences from Part 1.
> Nobody is outside them, so there are zero outliers."

### Chart C: Payroll Concentration Curve (`04_payroll_concentration_line.png`), about 40 seconds
> "This line answers the question: is pay concentrated in a few people? The grey diagonal is perfectly equal pay.
> Our blue line is close to it. The lowest-paid half of the team gets 41.3 percent of the payroll.
> The Gini score is 0.11, where zero means perfectly equal. So overall, pay is quite evenly spread."

*(If asked about cities: "Chennai and Hyderabad average 68,000 and Bangalore 48,500. But Bangalore's two people are in HR and Sales,
the lowest-paid departments, so the gap is probably about departments, not the city.")*

---

## Slide 4 – Two Recommendations (1 minute)
**On screen**
1. Benchmark HR salaries against the market (24 % below average)
2. Collect experience, joining date, job level and currency, and add more employees

**Speaker notes**
> "First, HR. Both HR employees are among the three lowest salaries. I recommend comparing HR pay with the market,
> to check whether it is fair or whether there is a retention risk.
> Second, better data. With 8 people, I can only describe the gaps, not explain them. If we add years of experience and joining date,
> we can check whether seniority explains the gaps, and we can build the experience and hiring-trend charts that were originally planned."

---

## Slide 5 – Limitations and Conclusion (45 seconds)
**On screen**
* Only 8 employees, and Finance is a single person
* No experience or dates; salary currency unknown
* Conclusion: pay follows department; HR is the lowest; no outliers; next step is better data

**Speaker notes**
> "The biggest limitation is size: with 8 people, one salary can change a group average a lot. We also do not know the currency.
> To sum up: salaries mainly follow department, HR is clearly the lowest-paid group, pay overall is evenly spread,
> and there are no outliers. My main recommendation is to collect richer data before making pay decisions. Thank you. Any questions?"
