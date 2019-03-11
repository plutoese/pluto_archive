import random
from itertools import permutations
import numpy as np
import time
import copy

x = ['c1','c2','c3','c4','c5']
period1 = time.time()
preferences = [random.choice(list(permutations(x, len(x)))) for i in range(1000)]
print(np.mean([item.index('c1') for item in preferences]))
print(np.mean([item.index('c2') for item in preferences]))
print(np.mean([item.index('c3') for item in preferences]))
print(np.mean([item.index('c4') for item in preferences]))
print(np.mean([item.index('c5') for item in preferences]))
print('period1: ', time.time() - period1)

period2 = time.time()
p2 = []
for i in range(1000):
    x = copy.copy(x)
    random.shuffle(x)
    p2.append(x)
print(np.mean([item.index('c1') for item in p2]))
print(np.mean([item.index('c2') for item in p2]))
print(np.mean([item.index('c3') for item in p2]))
print(np.mean([item.index('c4') for item in p2]))
print(np.mean([item.index('c5') for item in p2]))
print('period2: ', time.time() - period2)


x = {2:'tom', 1:'jerry'}
for k in sorted(x):
    print(x[k])