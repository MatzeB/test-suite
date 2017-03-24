#!/usr/bin/env python
import random
import json

metric_generators = [
    ('size', lambda: random.randint(1, 1000)),
    ('count_a', lambda: random.randint(1,1000)),
    ('count_b', lambda: random.randint(1,1000)),
    ('time_a', lambda: random.gauss(0,20.)),
    ('time_b', lambda: random.gauss(0,20.)),
]

wordrand = random.Random()
wordrand.seed(1234)
seen = set()
def mkword():
    while True:
        word = ''
        for i in range(0, wordrand.randint(1,3)):
            for vowel in wordrand.choice(['a', 'e', 'i', 'o', 'a']):
                word += vowel
                for cons in wordrand.choice(['m', 'n', 'ch', 's', 'l', 'r', 't',
                                             'b', 'p', 'tr', 'nt', 'sh', 'nd',
                                             'th', 'ng', 'rd', 'ns']):
                    word += cons
        if word not in seen:
            seen.add(word)
            break
    return word

tests = []
for i in range(0,20):
    metrics = dict()
    for name,func in metric_generators:
        metrics[name] = func()

    tests.append({
        'metrics': metrics,
        'name': 'test-suite :: %s.test' % mkword(),
    })

data = {'tests': tests}
print json.dumps(data, indent=2)
