# RUN: compare.py data.csv | FileCheck --strict-whitespace %s

CHECK: Tests: 2

CHECK: Program                                         time   size

CHECK: foobar                                          5.00  20
CHECK: baz                                             2.40  13

CHECK: metric         time         size
CHECK: count          2.00         2.00
CHECK: sum            7.40        33.00
CHECK: mean           3.70        16.50
CHECK: std            1.84         4.95
CHECK: min            2.40        13.00
CHECK: 25%            3.05        14.75
CHECK: 50%            3.70        16.50
CHECK: 75%            4.35        18.25
CHECK: max            5.00        20.00
