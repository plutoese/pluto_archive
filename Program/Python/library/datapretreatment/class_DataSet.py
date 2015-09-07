# coding=UTF-8

import json
import pickle
import pandas as pd
import numpy as np
from library.region.class_AdminCode import *
from library.datapretreatment.class_DataSheet import *

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
        if year is None:
            year = slice(None)
        else:
            if isinstance(year,(range,list)):
                year = [str(y) for y in year]
        if region is None:
            region = slice(None)
        else:
            regions = []
            for item in region:
                if len(item) == 1:
                    regions.append(self.AD[item[0]]['acode'])
                else:
                    regions.append(self.AD[tuple(item)]['acode'])
            region = regions
        if variable is None:
            variable = slice(None)

        self.data = self._data

        if self.data.ndim == 1:
            self.data = self.data.loc[year]

        elif self.data.ndim == 2:
            if year in mindex and region in mindex:
                self.data = self.data.loc[region,year]
            if year in mindex and variable in mindex:
                self.data = self.data.loc[year,variable]
            if region in mindex and variable in mindex:
                self.data = self.data.loc[region,variable]

        else:
            self.data = self.data.loc[year,region,variable]

        # transform
        shape = self.data.shape
        if len(shape) == 3:
            if shape[0] == 1:
                self.data = self.data.xs(key=year,axis=0)
            if len(self.data.shape) < 3:
                if shape[1] == 1:
                    self.data = self.data.xs(key=region[0],axis=0)
                if len(self.data.shape) < 2:
                    if shape[2] == 1:
                        self.data = self.data.xs(key=variable[0],axis=0)
                else:
                    if shape[2] == 1:
                        self.data = self.data.xs(key=variable[0],axis=1)
            else:
                if shape[1] == 1:
                    self.data = self.data.xs(key=region[0],axis=1)
                if len(self.data.shape) < 3:
                    if shape[2] == 1:
                        pass
                else:
                    if shape[2] == 1:
                        self.data = self.data.xs(key=variable[0],axis=2)

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

# 类ToDataSet用来转换数据表到数据集
class PandasDataStruct:
    # 构造函数
    def __init__(self,data=None):
        # load data
        self._data = data
        self.vars = self._data[0][3:]
        self.rdata = self._data[1:]
        self.rows = len(self.rdata)
        self.period = list(sorted(set([int(item[2]) for item in self.rdata])))
        self.numberofdataframe = int(self.rows / len(self.period))

    # to Pandas DataStruct
    def toPDataStruct(self):
        nvar = len(self.vars)
        nyear = len(self.period)
        nunit = self.numberofdataframe

        if nvar > 1 & nyear > 1 & nunit > 1:
            return self._toPanel


    # 转换为Panel数据
    def _toPanel(self):
        regions = [self.rdata[n][0] for n in range(self.numberofdataframe)]
        variables = self.vars
        ndata = dict()
        for i in range(len(self.period)):
            mdata = [self.rdata[j][3:] for j in range(i * self.numberofdataframe, (i + 1) * self.numberofdataframe)]
            dframe = pd.DataFrame(mdata,columns=variables,index=regions)
            ndata[str(self.period[i])] = dframe
        paneldata = pd.Panel(ndata)

        return paneldata

if __name__ == '__main__':
    #mdatasheet = DataSheet(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICData.xlsx')
    #json.dump(mdatasheet.data, fp=open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICData.txt','w'))
    '''
    P = json.load(open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICData.txt'))
    topanel = PandasDataStruct(P)
    pdata = topanel._toPanel()
    F = open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICPdata.pkl','wb')
    pickle.dump(pdata,F)
    F.close()
    '''
    F = open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICPdata.pkl','rb')
    pdata = pickle.load(F)
    dset = DataSet(pdata)
    dset.setSubset(year=range(2000,2013),region=[[u'上海']],variable=[u'国内生产总值_人均'])
    #dset.setSubset(year='2012',region=[[u'北京'],[u'上海'],[u'浙江',u'嘉兴']],variable=[u'财政支出',u'国内生产总值',u'国内生产总值_人均'])
    #dset.setSubset(year=range(2010,2013),region=[[u'北京'],[u'上海'],[u'浙江',u'嘉兴']],variable=[u'财政支出',u'国内生产总值',u'国内生产总值_人均'])
    #dset.setSubset(year=range(2000,2013),region=[[u'北京']],variable=[u'财政支出',u'国内生产总值',u'国内生产总值_人均'])
    #dset.setSubset(year=range(2000,2014),region=[[u'北京'],[u'上海'],[u'浙江',u'杭州']],variable=[u'国内生产总值_人均'])
    dset.noNA()
    mdata = dset.data

    print(mdata)
    print(dset.data.ndim)

    