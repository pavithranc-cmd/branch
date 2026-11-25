# Employee Salary Analysis – One-Page Summary
**Week 1 · Day 5 · Weekly Project (Part 2)** · Source notebook: `notebooks/week1_day5_employee_customer_analysis.ipynb`

## 1. Problem Statement
How are salaries distributed across departments and cities? Is pay concentrated in a few people, and are there outliers?
What should management look at next?

## 2. Dataset Description
| Item | Detail |
|---|---|
| File | `week1/day5/task1_data_cleaning/data/clean_data.csv` (Part 1 cleaned output, re-verified against the cleaning pipeline) |
| Size | 8 employees × 6 columns: `id`, `name`, `department` (Finance, IT, Sales, HR), `salary`, `city` (Chennai, Hyderabad, Mumbai, Bangalore), `salary_outlier` |
| Quality | 0 missing values, 0 duplicates, city spelling standardised in Part 1 |
| Not available | experience, joining date, job level, salary currency/period |

Salary summary: mean **61,500**, median **61,500**, minimum **45,000**, maximum **81,000**, standard deviation **12,950**.

## 3. Three Key Insights
1. **Department is the clearest driver of pay.** Average salary: Finance 81,000 (n=1), IT 67,000 (n=3), Sales 58,500 (n=2), HR 46,500 (n=2).
   HR is **15,000 (24 %) below** the company average, and both HR employees are among the three lowest salaries (45,000 and 48,000).
2. **Pay is evenly spread, with no outliers.** Mean equals median. The lowest-paid 50 % of staff receive **41.3 %** of payroll and the top 25 % receive **31.7 %**.
   The Gini coefficient is **0.11** (0 = equal). **0** salaries fall outside the IQR fences of 22,875–97,875.
3. **The city gap is probably department mix, not location.** Chennai and Hyderabad average **68,000** and Bangalore **48,500** (a 19,500 gap).
   But Bangalore's two employees work in HR and Sales, the two lowest-paid departments, so city and department effects cannot be separated.

## 4. Two Data-Driven Recommendations
1. **Benchmark HR salaries against the market.** HR is 24 % below the company average, and its salaries (45,000–48,000) are below every other department's.
   Review whether this reflects the role or under-payment before it becomes a retention risk.
2. **Collect experience, joining date, job level and currency, and grow the dataset.** With 8 rows and one numeric column, the department and city gaps
   can only be described, not explained. These fields would let the team test whether seniority explains the gaps, and build the hiring-trend and
   experience charts the brief requested.

## 5. Limitations
* Only **8 employees**. Finance's "highest average" is a single person, so averages are fragile and nothing here is statistically significant.
* No experience or date columns. The scatter plot uses **salary by city** and the line chart uses a **payroll concentration curve** instead.
* Salary currency and pay period are unknown. Correlation analysis is not possible with a single numeric measure.

## 6. Conclusion
The data is clean and the pay structure is simple: salaries follow department lines, HR is clearly the lowest-paid group, and there are no outliers.
The next step is better data, not more charts. Adding experience and joining dates would turn these descriptive findings into explanations
that can support pay decisions.
