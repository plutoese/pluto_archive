# coding=UTF-8

import pandas as pd
import numpy as np

wp = pd.Panel(np.random.randn(2, 5, 4), items=['Item1', 'Item2'],major_axis=pd.date_range('1/1/2000', periods=5),minor_axis=['A', 'B', 'C', 'D'])
print(wp)
print(wp['Item1'])

df = pd.DataFrame({'a': ['foo', 'bar', 'baz'],'b': np.random.randn(3)})
print(df)
data = {'item1': df, 'item2': df}
panel = pd.Panel.from_dict(data, orient='items')
print(panel['item1'])
print(panel['item2'])

