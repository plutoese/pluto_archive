# coding=UTF-8

import re
import os
from library.datapretreatment.class_DataSheet import *

# 类AdminCodeDataSheet用来处理行政区域代码的Excel文件
class AdminCodeDataSheet(DataSheet):
    '''
    类AdminCodeDataSheet用来处理行政区域代码
    
    属性：
    self.rawdata: 原始数据
    '''
    # 构造函数
    def __init__(self, filename=None,sheetnum=0):
        DataSheet.__init__(self,filename=filename,sheetnum=sheetnum,type='dataframe')
        # 设置文件名为版本号，年份为文件名第一部分
        self.version = re.split('\.',os.path.basename(filename))[0]
        self.year = re.split('\_',self.version)[0]

        self.rawdata = self.rawdata.set_index(u'代码')

        # 删除缺失值所在的行
        self._data = self.rawdata.dropna(axis=0)

        # 剔除*号或者（）号
        self._data = self._data.applymap(lambda x:re.split('\(|\*',x)[0])

        # 删除index不是数字的行
        #self._data = self._data.drop([code for code in list(self._data.index) if not isinstance(code,int)])
        self._data = self._data.drop([code for code in list(self._data.index) if re.match('^\d{6}$',str(int(code))) is None])

        # 行索引
        self.index = self._data.index

    # 把数据分类为省地县三级
    def classification(self):
        index_province =  [code % 10000 == 0 for code in list(self.index)]
        index_prefecture = [code % 10000 != 0 and code % 100 == 0 for code in list(self.index)]
        index_county = [code % 100 != 0 for code in list(self.index)]

        # 创建省地县三级行政区域列表
        self.provinces = self._data[index_province]
        self.prefectures = self._data[index_prefecture]
        self.counties = self._data[index_county]

        # 创建字典形式的三级行政区域，用来插入MongoDB数据库
        self.provinces_dict = [{'acode':str(int(i)),'region':self.provinces.loc[i][0],'adminlevel':2,'version':self.version,'year':self.year} for i in self.provinces.index]
        self.prefectures_dict = [{'acode':str(int(i)),'region':self.prefectures.loc[i][0],'adminlevel':3,'version':self.version,'year':self.year} for i in self.prefectures.index]
        self.counties_dict = [{'acode':str(int(i)),'region':self.counties.loc[i][0],'adminlevel':4,'version':self.version,'year':self.year} for i in self.counties.index]


if __name__ == '__main__':
    mdatasheet = AdminCodeDataSheet(r'C:\Data\acode\2006_12_31.xlsx')
    mdatasheet.classification()
    mdata = mdatasheet.data
    print(mdata)
    print(mdatasheet.provinces_dict)

