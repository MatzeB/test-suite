# RUN: compare.py data20_a.json -m time_b | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: time_b

CHECK: Test                                            time_b

CHECK: aterap                                         43.38
CHECK: ochan                                          36.13
CHECK: ins                                           -23.83
CHECK: imardish                                       23.60
CHECK: atrap                                         -23.48
CHECK: ib                                            -22.01
CHECK: ich                                           -19.33
CHECK: ol                                             19.16
CHECK: ach                                           -15.91
CHECK: iterd                                         -12.94
CHECK: onteshach                                      12.89
CHECK: it                                             12.69
CHECK: echandob                                      -12.26
CHECK: ardons                                         12.17
CHECK: as                                            -10.95

CHECK: metric       time_b
CHECK: count         20.00
CHECK: sum           16.19
CHECK: mean           0.81
CHECK: std           19.65
CHECK: min          -23.83
CHECK: 25%          -13.68
CHECK: 50%           -2.18
CHECK: 75%           12.74
CHECK: max           43.38
