# coding=UTF-8

from pymongo import *
import pandas as pd
from library.region.class_AdminCode import *

# 类MongoDB用来连接MongoDB数据库
class MongoDB:
    '''
    类MongoDB用来连接MongoDB数据库。
    
    属性：
    client: 数据库连接端口
    db: 数据库中的database
    collection：数据库中的集合
    
    方法：
    connect(self,dbname=None,colname=None)：连接数据库中特定的集合，参数dbname表示数据库名称，colname表示集合名称，它们类型都为字符串，默认为None。返回数据库中集合的句柄。
    '''
    def __init__(self):
        self.client = MongoClient('localhost',27017)

    # 连接数据库中的集合
    def connect(self,dbname=None,colname=None):
        self.db = self.client[dbname]
        self.collection = self.db[colname]
        return self.collection

    # 从数据库中获得数据
    def find(self,condition,projection):
        result = self.collection.find(condition,projection).sort([('year',ASCENDING),('acode',ASCENDING)])
        return result


if __name__ == '__main__':
    db = MongoDB()
    db.connect('regionDB','CEIC')
    ad = AdminCode()
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


