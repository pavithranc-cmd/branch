# Week 1 · Day 4 · Task 1: Terminal, VS Code and Jupyter

```
Week 1 - Day 4/
└── project/
    ├── data/
    │   └── employees.csv              # sample data ("chennai" in mixed case)
    ├── notebooks/
    │   ├── performance_check.ipynb    # notebook: headings, grep, %timeit, notes
    │   ├── performance_check.py       # exported with nbconvert --to script
    │   └── debug_loop.py              # loop for the VS Code breakpoint exercise
    ├── reports/
    │   └── chennai_employees.txt      # grep output
    ├── .vscode/launch.json            # debugger configuration
    ├── terminal_practice.sh           # mkdir/ls/cd/cp/mv/rm/grep (Git Bash)
    └── terminal_practice.ps1          # same commands in PowerShell
```

## How to run
| Step | Command (run inside `Week 1 - Day 4`) |
|---|---|
| Terminal practice, Git Bash | `bash project/terminal_practice.sh` |
| Terminal practice, PowerShell | `powershell -ExecutionPolicy Bypass -File .\project\terminal_practice.ps1` |
| Notebook | open `project/notebooks/performance_check.ipynb` → **Run All** |
| Export | `cd project/notebooks` then `jupyter nbconvert --to script performance_check.ipynb` |
| Debugger | open `notebooks/debug_loop.py`, set a breakpoint on the `# BREAKPOINT` line, press **F5** |

## grep -i "chennai" employees.csv
```
1,Arun,Sales,65000,Chennai
3,Karthik,IT,58000,chennai
5,Rohan,Finance,81000,CHENNAI
```
`-i` ignores upper/lower case, so all 3 spellings match. Without `-i`, only Karthik's row matches.
The header is not printed because it does not contain the word.
In PowerShell, `Select-String` is case-insensitive by default; add `-CaseSensitive` to get the behaviour of `grep` without `-i`.

## When to use a notebook vs. a .py file
1. Use a Jupyter notebook when exploring data, testing ideas step by step, and viewing charts or outputs inline with notes.
2. Use a `.py` file when writing clean, reusable production code, data pipelines, or functions that run automatically.
3. Notebooks are great for experiments and presentations, while `.py` files work better with Git diffs, testing, and scheduling.
4. A common workflow is prototyping in a `.ipynb` notebook first and then moving stable logic into `.py` scripts.
