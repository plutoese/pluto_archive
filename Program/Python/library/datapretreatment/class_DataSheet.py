# coding=UTF-8

from library.imexport.class_Excel import *
import pandas as pd

# 处理DataSheet的主类，用来被继承。
# 可以导出DataSet类，有序字典格式
class DataSheet:
    '''
    类DataSheet是数据表单的主类，用以被继承。
    
    属性：
    rawdata: 原始数据
    '''

    def __init__(self, filename=None,sheetnum=0,type=None):
        if type is None:
            self.rawdata = Excel(filename).read(sheetnum=sheetnum)
        else:
            self.rawdata = pd.read_excel(filename,sheetnum)


    @property
    def data(self):
        return self._data

if __name__ == '__main__':
    mdatasheet = DataSheet(r'C:\Down\student.xls')
    print(mdatasheet.rawdata)