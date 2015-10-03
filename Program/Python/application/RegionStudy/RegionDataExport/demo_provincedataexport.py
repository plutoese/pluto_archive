# coding=UTF-8

from application.RegionStudy.RegionDataInterface.class_regionaldatainterface import *


dinterface = RegionDataInterface(collection='ProvinceStatistics')
print(dinterface.variable)
ad = AdminCode()

querydict = {'variable':[u'地区生产总值',u'地区生产总值指数',u'人均地区生产总值',u'个体全社会固定资产投资']}
result = dinterface.query(querydict)
mdata = result['data']
mdata = mdata.swapaxes(0,2)
mdata = mdata.to_frame()
file = 'c:/down/mproresult.xls'
mdata.to_excel(file)