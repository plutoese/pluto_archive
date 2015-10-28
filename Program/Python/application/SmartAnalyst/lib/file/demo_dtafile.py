# coding=UTF-8

import pandas as pd
import numpy as np

# 读入stata文件
df = pd.read_stata('e:/Data/micro/CGSS2010.dta',encoding='GBK',convert_categoricals =False, iterator=True)

# 变量
variables = df.variable_labels()
print(len(df.lbllist),df.lbllist)
print(len(df.varlist),df.varlist)
print(len(df.vlblist),df.vlblist)

# 数据的label
labels = df.value_labels()
new_labels = dict()
for var in labels:
    var_label = list(labels[var].items())
    label_tuple = [(np.uint(item[0]).astype(int),item[1]) for item in var_label]
    new_labels[var] = dict(label_tuple)
print(new_labels)

# 数据
data = df.read()

'''
# 组合数据
result_data = []
picec_data = {}
for i in range(data.shape[0]):
#for i in range(2):
    series_data = data.iloc[i]
    for var in series_data.index:
        var_label = variables.get(var)
        var_value = series_data[var]
        value_label = new_labels.get(var)
        if var in new_labels:
            print(var)


        #print(var_value,type(var_value),isinstance(var_value,(np.int,np.float)),np.isnan(var_value))
        if isinstance(var_value,(np.int,np.float)):
            if np.isnan(var_value):
                picec_data[var] = {'label':var_label,'value':{'value':None,'label':None}}
            else:
                if var_value- int(var_value) == 0:
                    if value_label is not None:
                        picec_data[var] = {'label':var_label,'value':{'value':var_value,'label':value_label[int(var_label)]}}
                    else:
                        picec_data[var] = {'label':var_label,'value':{'value':var_value,'label':None}}
                else:
                    picec_data[var] = {'label':var_label,'value':{'value':var_value,'label':None}}
        else:
            picec_data[var] = {'label':var_label,'value':{'value':var_value,'label':None}}

    #print(picec_data)
    result_data.append(picec_data)
'''






















