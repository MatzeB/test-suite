# RUN: compare.py data20_a.json data20_b.json --no-diff --delta -m count_a | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: count_a

CHECK: Test                                            data20_a  data20_b delta

CHECK: ithaboth                                       873       1           -872
CHECK: echandob                                       80        941          861
CHECK: ol                                             8         850          842
CHECK: atretr                                         923       173         -750
CHECK: aterap                                         919       297         -622
CHECK: imim                                           241       838          597
CHECK: ochan                                          228       822          594
CHECK: atrap                                          908       352         -556
CHECK: em                                             187       733          546
CHECK: ich                                            523       4           -519
CHECK: ib                                             156       527          371
CHECK: iterd                                          671       338         -333
CHECK: imardish                                       937       642         -295
CHECK: ins                                            674       398         -276
CHECK: ardons                                         432       189         -243

CHECK: data20_a     data20_b        delta
CHECK: count        20.00        20.00        20.00
CHECK: sum       11317.00     10209.00     -1108.00
CHECK: mean        565.85       510.45       -55.40
CHECK: std         329.09       306.57       525.02
CHECK: min           8.00         1.00      -872.00
CHECK: 25%         237.75       289.25      -379.50
CHECK: 50%         632.00       462.50      -193.50
CHECK: 75%         881.75       824.25       414.75
CHECK: max         937.00       941.00       861.00
