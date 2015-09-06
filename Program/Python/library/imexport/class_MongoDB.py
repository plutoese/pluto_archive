# coding=UTF-8

from pymongo import *

# 类MongoDB用来连接MongoDB数据库
class MongoDB:
    def __init__(self):
        self.client = MongoClient('localhost',27017)

    # 连接数据库中的集合
    def connect(self,dbname=None,colname=None):
        self.db = self.client[dbname]
        self.collection = self.db[colname]
        return self.collection

if __name__ == '__main__':
    db = MongoDB()
    db.connect('regionDB','CEIC')

