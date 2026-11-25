#!/usr/bin/env bash
# Terminal practice (Git Bash / Linux / Mac).
# Run from the folder that CONTAINS "project":  bash project/terminal_practice.sh
set -e
echo "== mkdir =="; mkdir -p project/data project/notebooks project/reports; ls project
echo; echo "== cd / pwd / ls =="; cd project/data; pwd; ls -l
echo; echo "== cp =="; cp employees.csv employees_backup.csv; ls
echo; echo "== mv =="; mv employees_backup.csv ../reports/employees_copy.csv; ls ../reports
echo; echo "== rm =="; rm ../reports/employees_copy.csv; ls ../reports
echo; echo "== grep -i \"chennai\" employees.csv =="; grep -i "chennai" employees.csv
echo; echo "== grep \"chennai\" (no -i, case-sensitive) =="; grep "chennai" employees.csv
echo; echo "== grep -ic (count) =="; grep -ic "chennai" employees.csv
grep -i "chennai" employees.csv > ../reports/chennai_employees.txt
cd ../..; echo; echo "== structure =="; find project -not -path "*/.ipynb_checkpoints*" | sort
