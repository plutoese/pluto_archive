# coding=UTF-8

from library.region.class_AdminCode import *

# 类DataSet代表数据集
# 用来生成和转换数据
class DataSet:
    '''
    类DataSet代表数据集。

    属性：
    data: 数据，类型是pandas对象
    '''

    # 构造函数
    def __init__(self, data=None):
        # load data
        self._data = data
        self.data = self._data
        self.AD = AdminCode()

    # subset of the dataset
    def setSubset(self,year=None,region=None,variable=None,mindex=None):
        shape = self.data.shape
        if len(shape) == 1:
            self.data = self.data.apply(self._setMissingData)
        if len(shape) == 2:
            self.data = self.data.applymap(self._setMissingData)
        if len(shape) == 3:
            self.data = self.data.apply(self._setMissingData,0)
            self.data = self.data.apply(self._setMissingData,1)
            self.data = self.data.apply(self._setMissingData,2)

    # to delete any row with NA
    # 删除任何保护缺失值的行
    def noNA(self):
        self.data = self.data.dropna()

    # 辅助函数，用来生成缺失值
    def _setMissingData(self,x):
        if len(str(x)) < 1:
            return None
        else:
            return x

if __name__ == '__main__':
    pass
    