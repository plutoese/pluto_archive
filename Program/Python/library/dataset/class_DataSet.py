# coding=UTF-8

from library.region.class_Layout import *
from library.dataanalysis.class_DataVisualization import *

# 类DataSet代表数据集
# 用来生成和转换数据
class DataSet:
    '''
    类DataSet代表数据集。

    属性：
    data: 数据，类型是pandas对象
    '''
    # 构造函数
    def __init__(self, data):
        # load data
        self._data = data

    # to delete any row with NA
    # 删除任何包含缺失值的行
    def noNA(self):
        self.data = self.data.dropna()

if __name__ == '__main__':
    pass