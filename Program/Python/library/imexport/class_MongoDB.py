# coding=UTF-8

from pymongo import *
import pandas as pd
import re
from library.region.AdminCode.class_AdministrativeCode import *

# 类MongoDB用来连接MongoDB数据库
class MongoDB:
    '''
    类MongoDB用来连接MongoDB数据库。
    
    属性：
    client: 数据库连接端口
    db: 数据库中的database
    collection：数据库中的集合
    
    方法：
    __init__(self)：初始化，连接MongoDB数据库。
    connect(self,dbname:str=None,colname:str=None)->pymongo.collection.Collection：连接数据库中特定的集合，参数dbname表示数据库名称，colname表示集合名称。返回数据库中集合的句柄了，类型pymongo.collection.Collection。
    find(self,condition:dict=None,projection:dict=None)->pymongo.cursor.Cursor：在数据库中查询，并返回结果，类型pymongo.cursor.Cursor。

    Demo：
    查询数据
    db = MongoDB()    # 连接数据库
    db.connect('regionDB','CEIC')
    ad = AdminCode()
    regions = [item['acode'] for item in ad[u'浙江',u'f']]    # regions实质上是地区acode的列表
    mdata = pd.DataFrame(list(db.find({'year':{'$gt':2000,'$lt':2012},'variable':{'$in':[u'财政支出',u'从业人数_在岗职工']},'acode':{'$in':regions}},{'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1})))    # 查询数据
    
    mdata得到的结果
              acode region     value   variable  year
    0    110000    北京市   55911.0       财政支出  2001
    1    110000    北京市    4003.0  从业人数_在岗职工  2001
    2    330100    杭州市     808.8  从业人数_在岗职工  2001
    3    330200    宁波市     555.3  从业人数_在岗职工  2001
    4    330300    温州市     497.4  从业人数_在岗职工  2001
    5    330400    嘉兴市     263.6  从业人数_在岗职工  2001
    6    330500    湖州市     165.5  从业人数_在岗职工  2001
    7    330600    绍兴市     342.2  从业人数_在岗职工  2001
    8    330700    金华市     247.6  从业人数_在岗职工  2001
    9    330800    衢州市     129.9  从业人数_在岗职工  2001
    10   330900    舟山市     105.7  从业人数_在岗职工  2001
    11   331000    台州市     289.2  从业人数_在岗职工  2001
    '''
    def __init__(self):
        self.client = MongoClient('localhost',27017)

    # 连接数据库中的集合
    def connect(self,dbname:str=None,colname:str=None):
        self.db = self.client[dbname]
        self.collection = self.db[colname]
        return self.collection

    # 从数据库中获得数据
    def find(self,condition:dict=None,projection:dict=None):
        # 此处有纰漏的地方是sort部分，如果没有year和acode，那么这条语句会出错，所以后续需要修改
        result = self.collection.find(condition,projection).sort([('year',ASCENDING),('acode',ASCENDING)])
        return result

if __name__ == '__main__':
    db = MongoDB()
    db.connect('regionDB','CEIC')
    ad = AdministrativeCode(year=2014)
    regions = [item['acode'] for item in ad[u'浙江',u'f']]
    regions.append('110000')
    #print(list(db.find({'year':2012,'variable':u'财政支出'},{'region':1,'year':1,'value':1,'acode':1,'_id':0}))[0:10])
    #mdata = pd.DataFrame(list(db.find({'year':2012,'variable':u'财政支出'},{'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1}))[0:10])
    #mdata = pd.DataFrame(list(db.find({'year':{'$gt':2000,'$lt':2012},'variable':{'$in':[u'财政支出',u'从业人数']}},{'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1}))[0:20])
    mdata = pd.DataFrame(list(db.find({'year':{'$gt':2000,'$lt':2012},'variable':{'$in':[u'财政支出',u'从业人数_在岗职工']},'acode':{'$in':regions}},{'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'year':1})))
    print(mdata)
    g = mdata.groupby(['variable','year'], sort=True)

    for name, group in g:
        print(name)
        print(group)
        print(group['value'])


