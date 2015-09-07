# coding=UTF-8

from library.imexport.class_MongoDB import *
from library.region.class_AdminCode import *
import pandas as pd

# 类RegionData用来从数据库MongoDB中导出区域数据
class RegionalData:
    # 构造函数
    def __init__(self,collection='CEIC'):
        # to connect to Mongodb database
        self.db = MongoDB()
        self.conn = self.db.connect('regionDB',collection)

    # 从数据库中获取区域数据
    def query(self,region=None,year=None,variable=None,projection={'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1},sorts=[('year',ASCENDING),('acode',ASCENDING)]):
        if region is not None:
            if isinstance(region,dict):
                region = [region]
            regioncode = [item['acode'] for item in region]
        if isinstance(year,(int,str)):
            year = [year]
        if isinstance(variable,(str)):
            variable = [variable]

        if (region is not None) and (year is not None) and (variable is not None):
            result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable},'acode':{'$in':regioncode}},projection).sort(sorts)))
        elif (region is not None) and (year is not None):
            result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'acode':{'$in':regioncode}},projection).sort(sorts)))
        elif (region is not None) and (variable is not None):
            result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable},'acode':{'$in':regioncode}},projection).sort(sorts)))
        elif (year is not None) and (variable is not None):
            result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable}},projection).sort(sorts)))
        elif (region is not None):
            result = pd.DataFrame(list(self.conn.find({'acode':{'$in':regioncode}},projection).sort(sorts)))
        elif(year is not None):
            result = pd.DataFrame(list(self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]}},projection).sort(sorts)))
        else:
            result = pd.DataFrame(list(self.conn.find({'variable':{'$in':variable}},projection).sort(sorts)))
        return result

if __name__ == '__main__':
    ad = AdminCode()
    rdata = RegionalData()
    #mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    #mdata = rdata.query(region=ad[u'浙江',u'f'],variable=u'财政支出',year=2012)
    mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)
    print(mdata)