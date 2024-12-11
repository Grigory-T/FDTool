this is fork of https://github.com/kristian10007/FDTool which is fork of https://github.com/USEPA/FDTool

for licence and additional info - see thouse repositories

my changes are clear from my two commits

how to use:
```python
!git clone https://github.com/Grigory-T/FDTool.git

import sys; sys.path.insert(0, r'cloned_repo_folder_here')
from FDTool.runner import run_fdtool
import seaborn as sns

df = sns.load_dataset("tips")
run_fdtool(df) # should return results below (str dtype)

# Functional Dependencies: 
# {size, total_bill} -> {time}
# {day, total_bill} -> {size}
# {day, total_bill} -> {time}
# {total_bill, tip} -> {size}
# {total_bill, tip} -> {sex}
# {total_bill, tip} -> {time}
# {day, total_bill, tip} -> {smoker}
# {size, total_bill, smoker} -> {day}
# {total_bill, tip, smoker} -> {day}
# {day, total_bill, sex, smoker} -> {tip}

# Equivalences: 
# {day, total_bill, tip} <-> {total_bill, tip, smoker}
# {day, total_bill, smoker} <-> {size, total_bill, smoker}

# Keys: 
# {total_bill, sex, smoker, size}
# {total_bill, sex, smoker, day}
# {total_bill, tip, smoker}
# {total_bill, tip, day}

# Number of FDs checked: 127
```
