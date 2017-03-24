# RUN: not compare.py data20_a.json -m foo 2>&1 | FileCheck --strict-whitespace %s

CHECK: Unknown metric 'foo'
CHECK: Available metrics:
CHECK: count_a
CHECK: size
CHECK: time_a
CHECK: time_b
CHECK: count_b
CHECK: Tests: 20
