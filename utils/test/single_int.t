# RUN: compare.py data20_a.json -m size | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: size

CHECK: Test                                            size

CHECK: ithaboth                                       978
CHECK: em                                             913
CHECK: it                                             673
CHECK: aterap                                         606
CHECK: ib                                             589
CHECK: ach                                            546
CHECK: atrap                                          515
CHECK: ardons                                         485
CHECK: or                                             461
CHECK: echandob                                       353
CHECK: iterd                                          339
CHECK: imardish                                       336
CHECK: imim                                           299
CHECK: onteshach                                      290
CHECK: ol                                             205

CHECK: metric         size
CHECK: count         20.00
CHECK: sum         8222.00
CHECK: mean         411.10
CHECK: std          256.51
CHECK: min           44.00
CHECK: 25%          205.00
CHECK: 50%          346.00
CHECK: 75%          556.75
CHECK: max          978.00
