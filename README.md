this is fork of https://github.com/kristian10007/FDTool which is fork of https://github.com/USEPA/FDTool

for licence and additional info - see those repositories

my changes are clear from my commits

how to use:
```python
# in cli
!git clone https://github.com/Grigory-T/FDTool.git

# in jupyter notebook
import sys; sys.path.insert(0, r'cloned_repo_folder_here')
from FDTool.runner import run_fdtool
import seaborn as sns

df = sns.load_dataset("tips")  # just to demonstrate
result = run_fdtool(df)  # result have two elements - [str, real_containers]

### print(result[0]) ###
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



### result[1] ###
# {'FD': frozenset({(frozenset({'tip', 'total_bill'}), 'size'),
#             (frozenset({'day', 'tip', 'total_bill'}), 'smoker'),
#             (frozenset({'smoker', 'tip', 'total_bill'}), 'day'),
#             (frozenset({'day', 'total_bill'}), 'size'),
#             (frozenset({'tip', 'total_bill'}), 'sex'),
#             (frozenset({'tip', 'total_bill'}), 'time'),
#             (frozenset({'day', 'total_bill'}), 'time'),
#             (frozenset({'size', 'total_bill'}), 'time'),
#             (frozenset({'day', 'sex', 'smoker', 'total_bill'}), 'tip'),
#             (frozenset({'size', 'smoker', 'total_bill'}), 'day')}),
#  'EQ': frozenset({frozenset({frozenset({'day', 'tip', 'total_bill'}),
#                        frozenset({'smoker', 'tip', 'total_bill'})}),
#             frozenset({frozenset({'size', 'smoker', 'total_bill'}),
#                        frozenset({'day', 'smoker', 'total_bill'})})}),
#  'CK': frozenset({frozenset({'day', 'tip', 'total_bill'}),
#             frozenset({'day', 'sex', 'smoker', 'total_bill'}),
#             frozenset({'smoker', 'tip', 'total_bill'}),
#             frozenset({'sex', 'size', 'smoker', 'total_bill'})})}

```
