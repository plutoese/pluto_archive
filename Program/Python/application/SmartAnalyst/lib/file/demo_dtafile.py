# coding=UTF-8

import pandas as pd


df = pd.read_stata('e:/Data/micro/CGSS2010.dta',convert_categoricals=False,iterator=True)
print(df.variable_labels())













