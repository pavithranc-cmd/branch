#!/usr/bin/env python
# coding: utf-8

# # Python & Data Engineering
# ## Week 1 · Day 4 · Task 1 — Terminal, VS Code and Jupyter

# ## 1. Folder structure
# ```bash
# mkdir -p project/data project/notebooks project/reports
# ```
# PowerShell: `New-Item -ItemType Directory -Force project/data, project/notebooks, project/reports`

# ## 2. `grep -i "chennai" employees.csv`

# In[1]:


get_ipython().system('grep -i "chennai" ../data/employees.csv')


# **Explanation**
# - `grep` prints every line of the file that contains the pattern.
# - `-i` makes the match **case-insensitive**, so it finds `Chennai`, `chennai` and `CHENNAI`.
# - Result: **3 employees** (Arun, Karthik, Rohan). Without `-i`, only Karthik's row (lowercase `chennai`) would match.
# - The header is not printed because it does not contain the word.
# - PowerShell equivalent: `Select-String -Path employees.csv -Pattern "chennai"`, which is case-insensitive by default.

# In[2]:


get_ipython().system('grep "chennai" ../data/employees.csv   # without -i: only the exact lowercase match')


# ## 3. List Comprehension vs For Loop Benchmark
# Comparing execution speed in Python using `%timeit`.

# In[3]:


def using_for_loop(n=10000):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result


def using_list_comp(n=10000):
    return [i * 2 for i in range(n)]


assert using_for_loop() == using_list_comp()  # same result


# ### 3.1 For loop

# In[4]:


get_ipython().run_line_magic('timeit', 'using_for_loop(10000)')


# ### 3.2 List comprehension

# In[5]:


get_ipython().run_line_magic('timeit', 'using_list_comp(10000)')


# ### 3.3 Result
# The list comprehension is faster because it avoids looking up and calling `result.append` on every iteration; it uses a dedicated `LIST_APPEND` bytecode instead.

# ## 4. Export to a script
# ```bash
# jupyter nbconvert --to script performance_check.ipynb
# ```
# This creates `performance_check.py`. `%timeit` becomes `get_ipython().run_line_magic(...)`.

# ## 5. When to Use a Notebook vs. a `.py` File
# 1. Use a Jupyter notebook when exploring data, testing ideas step by step, and viewing charts or outputs inline with notes.
# 2. Use a `.py` file when writing clean, reusable production code, data pipelines, or functions that run automatically.
# 3. Notebooks are great for experiments and presentations, while `.py` files work better with Git diffs, testing, and scheduling.
# 4. A common workflow is prototyping in a `.ipynb` notebook first and then moving stable logic into `.py` scripts.
