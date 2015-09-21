# coding=UTF-8

from library.datastruct.class_SeriesData import *
from library.datalayout.class_Layout import *
from application.RegionStudy.RegionDataInterface.class_regionaldatainterface import *

dinterface = RegionDataInterface(collection='cCity')

ad = AdminCode()
for var in dinterface.variable:
    for year in range(2000,2013):
        print(var)
        querydict = {'variable':var,'scale':'全市','year':year}
        result = dinterface.query(querydict)
        if result is not None:
            file = 'C:/Data/database/' + var + '_全市_' + str(year) + '.xls'
            result['data'].to_excel(file)

        querydict = {'variable':var,'scale':'市辖区','year':year}
        result = dinterface.query(querydict)
        if result is not None:
            file = 'C:/Data/database/' + var + '_市辖区_' + str(year) + '.xls'
            result['data'].to_excel(file)