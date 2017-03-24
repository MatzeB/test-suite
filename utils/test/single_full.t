# RUN: compare.py data20_a.json --full -m size | FileCheck --strict-whitespace %s

CHECK: Tests: 20
CHECK: Metric: size

CHECK: Test                           size

CHECK: test-suite :: ithaboth.test   978
CHECK: test-suite :: em.test         913
CHECK: test-suite :: it.test         673
CHECK: test-suite :: aterap.test     606
CHECK: test-suite :: ib.test         589
CHECK: test-suite :: ach.test        546
CHECK: test-suite :: atrap.test      515
CHECK: test-suite :: ardons.test     485
CHECK: test-suite :: or.test         461
CHECK: test-suite :: echandob.test   353
CHECK: test-suite :: iterd.test      339
CHECK: test-suite :: imardish.test   336
CHECK: test-suite :: imim.test       299
CHECK: test-suite :: onteshach.test  290
CHECK: test-suite :: ol.test         205
CHECK: test-suite :: atretr.test     205
CHECK: test-suite :: ich.test        150
CHECK: test-suite :: ochan.test      118
CHECK: test-suite :: ins.test        117
CHECK: test-suite :: as.test         44

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
