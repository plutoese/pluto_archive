# coding=UTF-8

import pandas as pd
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 类RSeriesData用来处理时间序列数据
class SeriesData(pd.Series):
    '''
    类RSeriesData用来处理时间序列数据。

    属性：
    self._data: pandas.Series类型的时间序列数据

    方法：
    __init__(self,data=None,tags=None)：构造函数，参数tags记录时间序列数据的基本信息。
    '''
    # 构造函数
    def __init__(self,data=None,tags=None):
        self._data = data
        self.tags = tags
        # 设置时间序列的基本信息
        self._setup()

    # 设置Series的基本信息
    # 此处待以后补充
    def _setup(self):
        if self.tags is not None:
            pass

    # 时间序列图
    def tsline(self):
        self._data.plot()
        plt.show()

if __name__ == '__main__':
    pass