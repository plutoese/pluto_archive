# coding=UTF-8

from library.datapretreatment.class_DataSet import *

# 类DataExplore用来进行数据探索性分析
class DataExplore:
    # 构造函数
    def __init__(self,data):
        self._data = data

    # 均值
    def describe(self):
        return self._data.describe()

if __name__ == '__main__':
    F = open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICPdata.pkl','rb')
    pdata = pickle.load(F)
    dset = DataSet(pdata)
    dset.setSubset(year='2002',variable=[u'财政支出',u'国内生产总值',u'国内生产总值_人均'],)
    dset.noNA()

    dexplore = DataExplore(dset.data)
    print(dexplore.describe())