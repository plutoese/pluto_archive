# coding=UTF-8
#--------------------------------------------------
# RegionData类是区域数据输入输出更改的接口
#--------------------------------------------------

from library.imexport.class_MongoDB import *
from library.region.AdminCode.class_AdministrativeCode import *
import pandas as pd

# 类RegionalData是区域数据输入输出更改的接口
class RegionData:
    '''
    类RegionalData用来从数据库MongoDB中导出区域数据，读入数据到MongoDB，以及更新数据
    
    属性：
    self.conn: 数据库MongoDB某集合的接口
    
    方法：
    __init__(self,collection:str='CEIC')：构造函数，参数collection表示集合名称。
    query(self,region:list=None,year:list=None,variable:list=None,projection:dict={'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1},sorts:list=[('year',ASCENDING),('acode',ASCENDING)])->pd.DataFrame：查询返回区域数据。

    Demo：
    查询返回区域数据
    ad = AdminCode()
    rdata = RegionalData()    # 初始化，连接MongoDB中的区域数据
    mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])    # 查询返回区域数据
    mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)    # 查询返回区域数据

    mdata得到的结果
             acode region    value   variable  year
    0   330100    杭州市  27548.0       财政支出  2006
    1   330100    杭州市   1162.4  从业人数_在岗职工  2006
    2   330200    宁波市  29270.0       财政支出  2006
    3   330200    宁波市    887.8  从业人数_在岗职工  2006

    '''
    # 构造函数
    def __init__(self,collection:str='CityStatistics'):
        # to connect to Mongodb database
        self.collectionname = collection
        self.db = MongoDB()
        self.conn = self.db.connect('regionDB',collection)
        # 初始化区域代码
        self.AD = AdministrativeCode()

    # 获得所有的变量名
    def variables(self):
        posts = self.conn.find()
        return sorted(posts.distinct('variable'))

    # 获得变量所有的时期
    def period(self,variable):
        posts = self.conn.find({'variable':{'$in':variable}})
        return sorted(posts.distinct('year'))

    # 获得变量，时期的区域
    def region(self,variable,year):
        print(variable,year)
        posts = self.conn.find({'year':{'$gte':year[0],'$lte':year[len(year)-1]},'variable':{'$in':variable}})
        return [(code,self.AD.getByAcode(code)['region']) for code in sorted(posts.distinct('acode'))]

    # 从数据库中获取区域数据
    def query(self,**conds)->pd.DataFrame:
        projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1}
        sorts= [('year',ASCENDING),('acode',ASCENDING)]
        conditions = dict()
        for key in conds:
            if re.match('projection',key):
                projection = conds[key]
                continue
            if re.match('sorts',key):
                sorts = conds[key]
                continue
            if isinstance(conds[key],list):
                conditions[key] = {'$in':conds[key]}
            else:
                conditions[key] = conds[key]
        result = pd.DataFrame(list(self.conn.find(conditions,projection).sort(sorts)))
        return result

if __name__ == '__main__':
    ad = AdministrativeCode()
    rdata = RegionData()
    print(rdata.variables())
    mdata = rdata.query(acode=[region['acode'] for region in ad[u'安徽',u'f']],year=[2006,2007,2010],variable=[u'职工平均工资',u'人均地区生产总值'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    #mdata = rdata.query(region=ad[u'浙江',u'f'],variable=u'财政支出',year=2012)
    #mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)
    print(mdata)