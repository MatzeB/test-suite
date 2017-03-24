# RUN: compare.py data20_a.json | FileCheck --strict-whitespace %s

CHECK: Tests: 20

CHECK: Test                                            count_a  size  time_a  time_b  count_b

CHECK: imardish                                       937      336  -23.04   23.60   533
CHECK: ach                                            925      546   27.66  -15.91   510
CHECK: atretr                                         923      205   22.56   -1.59   175
CHECK: aterap                                         919      606   22.50   43.38   259
CHECK: atrap                                          908      515   22.44  -23.48   146
CHECK: ithaboth                                       873      978   38.68   -5.03   909
CHECK: onteshach                                      865      290    9.19   12.89   16
CHECK: it                                             827      673   20.91   12.69   866
CHECK: ins                                            674      117    5.93  -23.83   136
CHECK: iterd                                          671      339  -44.43  -12.94   461
CHECK: or                                             593      461   -9.43    7.87   147
CHECK: ich                                            523      150   17.42  -19.33   282
CHECK: ardons                                         432      485    4.87   12.17   112
CHECK: as                                             347      44   -22.10  -10.95   644
CHECK: imim                                           241      299   12.62   -1.92   559

CHECK: metric      count_a         size       time_a       time_b      count_b
CHECK: count         20.00        20.00        20.00        20.00        20.00
CHECK: sum        11317.00      8222.00        50.76        16.19      9508.00
CHECK: mean         565.85       411.10         2.54         0.81       475.40
CHECK: std          329.09       256.51        22.20        19.65       313.84
CHECK: min            8.00        44.00       -44.43       -23.83        16.00
CHECK: 25%          237.75       205.00       -15.98       -13.68       168.00
CHECK: 50%          632.00       346.00         7.05        -2.18       485.50
CHECK: 75%          881.75       556.75        21.29        12.74       747.50
CHECK: max          937.00       978.00        38.68        43.38       953.00
