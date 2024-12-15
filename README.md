# FDToolDF
This is fork of https://github.com/kristian10007/FDTool which is fork of https://github.com/USEPA/FDTool

This fork introduces:
- Functionality of using pandas and polars dataframes as inputs.
- Better logging.
- (Experiments planned) Multithreaded search optimization.

## Usage

```python
# in cli
!pip install fdtooldf

# in jupyter notebook
from fdtooldf.runner import run_fdtool
import seaborn as sns

df = sns.load_dataset("tips")  # just to demonstrate
result = run_fdtool(df)  # result have two elements - [str to print, real_containers]

print(result[0])
# >>> FD (functional dependancies):
# total_bill tip -> sex
# total_bill day -> size
# total_bill day -> time
# total_bill tip -> size
# total_bill tip -> time
# total_bill size -> time
# total_bill tip day -> smoker
# total_bill tip smoker -> day
# total_bill smoker size -> day
# total_bill sex smoker day -> tip

# >>> EQ (equivalences):
# size smoker total_bill <-> smoker total_bill day
# tip total_bill day <-> tip smoker total_bill

# >>> CK (candidate keys):
# day tip total_bill
# smoker tip total_bill
# day sex smoker total_bill
# sex size smoker total_bill



result[1]
# {'FD': frozenset({(frozenset({'day', 'total_bill'}), 'size'),
#             (frozenset({'tip', 'total_bill'}), 'size'),
#             (frozenset({'size', 'total_bill'}), 'time'),
#             (frozenset({'tip', 'total_bill'}), 'sex'),
#             (frozenset({'tip', 'total_bill'}), 'time'),
#             (frozenset({'smoker', 'tip', 'total_bill'}), 'day'),
#             (frozenset({'day', 'total_bill'}), 'time'),
#             (frozenset({'size', 'smoker', 'total_bill'}), 'day'),
#             (frozenset({'day', 'sex', 'smoker', 'total_bill'}), 'tip'),
#             (frozenset({'day', 'tip', 'total_bill'}), 'smoker')}),
#  'EQ': frozenset({(frozenset({'size', 'smoker', 'total_bill'}),
#              frozenset({'day', 'smoker', 'total_bill'})),
#             (frozenset({'day', 'tip', 'total_bill'}),
#              frozenset({'smoker', 'tip', 'total_bill'}))}),
#  'CK': frozenset({frozenset({'day', 'tip', 'total_bill'}),
#             frozenset({'day', 'sex', 'smoker', 'total_bill'}),
#             frozenset({'sex', 'size', 'smoker', 'total_bill'}),
#             frozenset({'smoker', 'tip', 'total_bill'})})}

```

## License
Notes:
Module REPO/fdtooldf/modules/dbschema released under C-FSL license and copyright held by Elmar Stellnberger.
