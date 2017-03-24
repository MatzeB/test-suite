# RUN: compare.py data20_a.json data20_b.json -m time_a | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: time_a

CHECK: Test                                            data20_a  data20_b diff

CHECK: echandob                                        1.32     27.62    1986.2%
CHECK: ich                                            17.42     81.84    369.8%
CHECK: or                                             -9.43     19.29    -304.6%
CHECK: imim                                           12.62     42.05    233.1%
CHECK: ardons                                          4.87     -5.91    -221.3%
CHECK: ach                                            27.66    -18.46    -166.7%
CHECK: ib                                              8.16     21.63    165.0%
CHECK: ins                                             5.93     -2.55    -142.9%
CHECK: atrap                                          22.44     -7.24    -132.3%
CHECK: em                                            -14.95    -33.63    125.0%
CHECK: ithaboth                                       38.68     -6.25    -116.2%
CHECK: ochan                                         -30.51     -1.61    -94.7%
CHECK: aterap                                         22.50     42.91     90.7%
CHECK: iterd                                         -44.43    -17.45    -60.7%
CHECK: onteshach                                       9.19     14.34     56.0%

CHECK: data20_a     data20_b         diff
CHECK: count        20.00        20.00        20.00
CHECK: sum          50.76       133.44        16.90
CHECK: mean          2.54         6.67         0.85
CHECK: std          22.20        27.84         4.75
CHECK: min         -44.43       -33.63        -3.05
CHECK: 25%         -15.98       -13.88        -1.20
CHECK: 50%           7.05        -2.08        -0.38
CHECK: 75%          21.29        19.87         0.99
CHECK: max          38.68        81.84        19.86
