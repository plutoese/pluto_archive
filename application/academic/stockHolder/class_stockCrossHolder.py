# coding=UTF-8

"""
=========================================
上市公司交叉持股类
=========================================

:Author: glen
:Date: 2018.03.20
:Tags: stock cross_holder
:abstract: 整理交叉持股信息

**类**
==================
StockCrossHolder
    交叉持股类

**使用方法**
==================

"""

import re
import pickle
import pandas as pd
from pathlib import Path


class StockCrossHolder:
    def __init__(self):
        # 导入交叉持股主文件
        self._data = None

    def toStockerHolderDf(self):
        """ 删除没有上市公司股东的条目

        :return: self
        """
        self._data = self._data.loc[(self._data['股东上市公司代码_SHComCd']).notnull(),]
        return self

    def load(self, file_name):
        """ 导入交叉持股主文件

        :param str file_name: 交叉持股主文件名
        :return: 返回交叉持股数据
        :rtype: pands.Dataframe
        """
        if re.match('^\.xls(x)?$',Path(file_name).suffix) is not None:
            self._data =  pd.read_excel(file_name)
        elif re.match('^\.pkl$',Path(file_name).suffix) is not None:
            with open(file_name, 'rb') as f:
                self._data = pickle.load(f)
        return self

    @property
    def data(self):
        return self._data


if __name__ == '__main__':
    stock_holder_file_name = r'D:\data\yang\forproj\main_stock_holder.pkl'
    stock_holder = StockCrossHolder().load(stock_holder_file_name)
    stock_holder.toStockerHolderDf().data.to_excel(r'D:\data\yang\forproj\stock_holder_df2.xlsx')

    #print(stock_holder.toStockerHolderDf().data)



