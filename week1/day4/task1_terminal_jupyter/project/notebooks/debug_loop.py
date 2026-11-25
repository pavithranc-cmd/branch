"""VS Code debugger practice.

1. Click left of the line marked BREAKPOINT to add a red dot.
2. Press F5 -> "Python Debugger: Current File".
3. Press F10 to step; watch row, chennai_count, total_salary in VARIABLES.
"""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "employees.csv"

chennai_count = 0
total_salary = 0

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["city"].lower() == "chennai":  # BREAKPOINT here
            chennai_count += 1
            total_salary += int(row["salary"])
            print(f"Found: {row['name']} ({row['city']})")

print(f"Employees in Chennai: {chennai_count}")
print(f"Average salary in Chennai: {total_salary / chennai_count:.0f}")
