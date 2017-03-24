# RUN: compare.py data20_a.json data20_b.json --full -m time_a | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: time_a

CHECK: Test                           data20_a  data20_b diff

CHECK: test-suite :: echandob.test    1.32     27.62    1986.2%
CHECK: test-suite :: ich.test        17.42     81.84    369.8%
CHECK: test-suite :: or.test         -9.43     19.29    -304.6%
CHECK: test-suite :: imim.test       12.62     42.05    233.1%
CHECK: test-suite :: ardons.test      4.87     -5.91    -221.3%
CHECK: test-suite :: ach.test        27.66    -18.46    -166.7%
CHECK: test-suite :: ib.test          8.16     21.63    165.0%
CHECK: test-suite :: ins.test         5.93     -2.55    -142.9%
CHECK: test-suite :: atrap.test      22.44     -7.24    -132.3%
CHECK: test-suite :: em.test        -14.95    -33.63    125.0%
CHECK: test-suite :: ithaboth.test   38.68     -6.25    -116.2%
CHECK: test-suite :: ochan.test     -30.51     -1.61    -94.7%
CHECK: test-suite :: aterap.test     22.50     42.91     90.7%
CHECK: test-suite :: iterd.test     -44.43    -17.45    -60.7%
CHECK: test-suite :: onteshach.test   9.19     14.34     56.0%
CHECK: test-suite :: it.test         20.91     11.94    -42.9%
CHECK: test-suite :: imardish.test  -23.04    -13.69    -40.6%
CHECK: test-suite :: ol.test        -19.08    -26.16     37.1%
CHECK: test-suite :: as.test        -22.10    -14.44    -34.7%
CHECK: test-suite :: atretr.test     22.56     19.21    -14.9%

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
