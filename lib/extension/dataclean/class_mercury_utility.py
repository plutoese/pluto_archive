# coding=UTF-8

"""
=========================================
MercuryUtility类
=========================================

:Author: glen
:Date: 2018.05.21
:Tags: utility data_cleaning
:abstract:

**类**
==================
MercuryUtility
    金星工具类

**使用方法**
==================
"""

import math
import numpy as np
import pandas as pd
import pickle


class DummyUtility:
    def __init__(self, dataframe=None):
        self._dataframe = dataframe
        self._labels = dict()

    def to_dummy_of_variable(self, col_names=None, col_indexes=None):
        if col_indexes is not None:
            if isinstance(col_indexes,int):
                col_names = self._dataframe.columns[[col_indexes]].values
            elif isinstance(col_indexes,(tuple,list)):
                col_names = self._dataframe.columns[col_indexes].values

        if col_names is not None:
            if isinstance(col_names, str):
                col_names = [col_names]

            for col_name in col_names:
                print(col_name)
                print(self.to_dummy(col_name))

    def to_compose_dummy(self):
        pass

    def to_dummy(self, col_name=None, dummy_start_name=None):

        series_data = self._dataframe[col_name]
        values = series_data.drop_duplicates().values
        dummy_start_name = ''.join([col_name,'_d'])

        # 根据值的个数，确定变量名称后的数字
        # 例如变量值有99个，那么数字就是2，意味着虚拟变量的个数是两位数，如果单个数字1，就需要补足0，为起始名+01
        # 意味着虚拟变量名为：起始名+01-起始名+99
        if values is not None:
            digit = math.floor(np.log10(len(values))) + 1
        else:
            raise Exception

        pdata = pd.DataFrame(series_data)

        # 定义label储存虚拟变量与值的对应字典
        labels = dict()
        for i in range(1, len(values) + 1):
            dummy_var = "".join([dummy_start_name, "{0:0{1}d}".format(i, digit)])
            labels[dummy_var] = values[i - 1]
            pdata.loc[:, dummy_var] = 0
            pdata.loc[series_data == values[i - 1], dummy_var] = 1

        del pdata[col_name]

        return pdata, labels


if __name__ == '__main__':
    # 导入数据
    #raw_cgss_data_2015 = pd.read_stata(r"E:\datahouse\rawdata\microdata\cgss\2015\cgss2015_14.dta")

    #with open(r'E:\datahouse\rawdata\microdata\cgss\2015\cgss2015.pkl', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
    #    pickle.dump(raw_cgss_data_2015, f, pickle.HIGHEST_PROTOCOL)

    with open(r'E:\datahouse\rawdata\microdata\cgss\2015\cgss2015.pkl', 'rb') as f:
        data = pickle.load(f)

    mdata = DummyUtility(dataframe=data)
    mdata.to_dummy_of_variable(col_indexes=[1,2,3])

    #pdata, label = to_dummy(data, dummy_start_name="s41d", col_index=2)
    #dummy_vars = ["s41"]
    #dummy_vars.extend(label.keys())
    #print(pdata.loc[:,dummy_vars])
    # pdata.loc[:,dummy_vars].to_excel(r"E:\datahouse\rawdata\microdata\cgss\2015\cgss2015_14.xlsx")