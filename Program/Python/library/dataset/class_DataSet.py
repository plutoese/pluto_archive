# coding=UTF-8

from library.region.class_Layout import *
from library.dataanalysis.class_DataVisualization import *

# 类DataSet代表数据集
class DataSet:
    '''
    类DataSet代表数据集。
    
    属性：
    self._data: 数据，类型是pandas对象。
    
    方法：
    __init__(self, data:pandas=None)：构造函数，初始化self._data。参数data是Pandas对象。
    noNA(self)：删除任何包含缺失值的行。
    '''
    # 构造函数
    def __init__(self, data=None):
        # load data
        self._data = data

    # to delete any row with NA
    # 删除任何包含缺失值的行
    def noNA(self):
        self.data = self.data.dropna()

if __name__ == '__main__':
    pass