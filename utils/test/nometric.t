# RUN: not compare.py data20_a.json data20_b.json 2>&1 | FileCheck --strict-whitespace %s

CHECK: No default metric found and none specified
CHECK: Available metrics:
CHECK: count_a
CHECK: size
CHECK: time_a
CHECK: time_b
CHECK: count_b
CHECK: Tests: 20
