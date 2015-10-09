# coding=UTF-8

import numpy as np
import pandas as pd

dff = pd.DataFrame(np.random.randn(10,3),columns=list('ABC'))
dff.iloc[3:5,0] = np.nan
dff.iloc[4:6,1] = np.nan
dff.iloc[5:8,2] = np.nan

print(dff)
print(dff[dff.isnull().any(axis=1)<1])
print(dff.reindex(dff.dropna().index))
print('********************************************')

d1 = pd.DataFrame(np.random.randn(10, 3))
d1.iloc[3:5,0] = np.nan
d2 = pd.DataFrame(np.random.randn(10, 3))
d2.iloc[4:6,1] = np.nan
pdata = pd.Panel({'Item1':d1,'Item2':d2})
print(pdata['Item1'])
print(pdata['Item2'])
print('#############################################')

pdata = pdata.dropna(axis=1)
print(pdata['Item1'])
print(pdata['Item2'])
print(pdata.major_axis)

print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')