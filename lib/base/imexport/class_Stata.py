# coding = UTF-8

"""
=========================================
Stata类
=========================================

:Author: glen
:Date: 2018.6.4
:Tags: Stata
:abstract: Stata类用来读写.dta（stata格式）的数据文件。

**类**
==================
Stata
    读写Stata数据文件

**使用方法**
==================


**示范代码**
==================
::

"""


import pandas as pd


class Stata:
    """类Stata用来读写.dta文件。

    :param str filename: 想要读写的文件名
    :param str encoding: 编码方式，默认是'GBK'
    :return: 无返回值
    :var list variables: 变量列表
    :var list variables_labels: 变量标签列表
    :var list variables_values_labels: 变量的值标签
    :var list values_labels: 值标签的内容
    """
    def __init__(self, filename, **kwargs):
        # 读入stata文件
        self.stata_file = pd.read_stata(filename, iterator=True, **kwargs)

    def read(self):
        """读入Stata数据文件数据

        :return: 返回stata数据
        :rtype: pandas.core.frame.DataFrame
        """
        return self.stata_file.read()

    @property
    def data_label(self):
        return self.stata_file.data_label()

    @property
    def value_labels(self):
        return self.stata_file.value_labels()

    @property
    def variable_labels(self):
        return self.stata_file.variable_labels()


if __name__ == '__main__':
    file_name = r'E:\datahouse\rawdata\microdata\cgss\dta\cgss2015_14.dta'
    stata_file = Stata(file_name, convert_categoricals=False)
    print(stata_file.data_label)
    #stata_data = stata_file.read()
    #print(stata_data.shape)
    #records = stata_data.to_dict("records")
    #for record in records:
    #    print(record)
    #print(stata_file.variable_labels)
