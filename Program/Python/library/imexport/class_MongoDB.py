# coding=UTF-8

from pymongo import *

# 处理Excel文件的类
class MongoDB:
	'''
	类MongoDB用来连接MongoDB数据库。
    
    属性：
    client: 连接数据库接口

    方法：
    connnect(self,dbname=None,collectionname=None): 连接MongDB数据库集合，参数dbname为数据库名称，类型字符串，默认为None；参数collectionname为集合名字，类型字符串，默认为None。返回值为集合，类型为MongoDB集合。
	'''
	def __init__(self):
		self.client = MongoClient('localhost', 27017)

	def connnect(self,dbname=None,collectionname=None):
		db = self.client[dbname]
		collection = db[collectionname]

		return collection


if __name__ == '__main__':
    db = MongoDB()
    con = db.connnect('regionDB','cAdministrationLevel09')
    print(con)