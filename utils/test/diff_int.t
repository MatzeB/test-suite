# RUN: compare.py data20_a.json data20_b.json -m count_a | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: count_a

CHECK: Test                                            data20_a  data20_b diff

CHECK: ol                                             8         850      10525.0%
CHECK: echandob                                       80        941      1076.2%
CHECK: em                                             187       733      292.0%
CHECK: ochan                                          228       822      260.5%
CHECK: imim                                           241       838      247.7%
CHECK: ib                                             156       527      237.8%
CHECK: ithaboth                                       873       1        -99.9%
CHECK: ich                                            523       4        -99.2%
CHECK: atretr                                         923       173      -81.3%
CHECK: aterap                                         919       297      -67.7%
CHECK: atrap                                          908       352      -61.2%
CHECK: ardons                                         432       189      -56.2%
CHECK: iterd                                          671       338      -49.6%
CHECK: ins                                            674       398      -40.9%
CHECK: or                                             593       385      -35.1%

CHECK: data20_a     data20_b         diff
CHECK: count        20.00        20.00        20.00
CHECK: sum       11317.00     10209.00       119.76
CHECK: mean        565.85       510.45         5.99
CHECK: std         329.09       306.57        23.52
CHECK: min           8.00         1.00        -1.00
CHECK: 25%         237.75       289.25        -0.57
CHECK: 50%         632.00       462.50        -0.27
CHECK: 75%         881.75       824.25         2.40
CHECK: max         937.00       941.00       105.25
