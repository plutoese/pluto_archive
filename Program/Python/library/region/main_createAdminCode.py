# coding=UTF-8

from library.imexport.class_FileSystem import *
from library.datapretreatment.class_AdminCodeDataSheet import *
from pymongo import *

# 0. file directory
path = r'C:\Data\acode'
mos = FileSystem(path)
files = mos.listabsdir()

client = MongoClient('localhost', 27017)
db = client['regionDB']
collection = db['AdminCode']

'''
# the nation doc
nation = {"adminlevel":1,"version":"0000_00_00","acode":"000000","region":"中国","parent":None,"year":"0000"}
print(nation)
collection.insert(nation)'''


for f in files:
    # 1. to read the data
    mdatasheet = AdminCodeDataSheet(f)
    mdatasheet.classification()
    print(f)
    print(mdatasheet.provinces_dict)
    print(mdatasheet.prefectures_dict)
    print(mdatasheet.counties_dict)
    print('********************************')

    for item in mdatasheet.provinces_dict:
        parent = collection.find({'acode':u'000000'})
        item['parent'] = parent[0]['_id']
        collection.insert(item)

    for item in mdatasheet.prefectures_dict:
        parentid = item['acode'][0:2] + u'0000'
        parent = collection.find({'acode':parentid,'version':mdatasheet.version})
        print(item)
        item['parent'] = parent[0]['_id']
        collection.insert(item)

    for item in mdatasheet.counties_dict:
        parentid = item['acode'][0:4] + u'00'
        parent = collection.find({'acode':parentid,'version':mdatasheet.version})
        item['parent'] = parent[0]['_id']
        collection.insert(item)