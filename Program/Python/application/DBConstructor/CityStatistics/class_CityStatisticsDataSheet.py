# coding=UTF-8

import re
import os
from library.datapretreatment.class_DataSheet import *

# 类CityStatisticsDataSheet用来处理中国城市统计年鉴的数据
class CityStatisticsDataSheet(DataSheet):
    '''
    类CityStatisticsDataSheet用来处理中国城市统计年鉴的数据
    
    属性：
    self.rawdata: 原始数据
    '''
    # 构造函数
    def __init__(self, filename=None,sheetnum=0):
        DataSheet.__init__(self,filename=filename,sheetnum=sheetnum)


if __name__ == '__main__':
    mdatasheet = CityStatisticsDataSheet(r'C:\Data\city\m01.xlsx')
    print(mdatasheet.rawdata)

