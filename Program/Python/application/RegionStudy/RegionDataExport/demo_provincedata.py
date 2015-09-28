# coding=UTF-8

from pymongo import *
import pandas as pd
from library.region.class_AdminCode import *
from library.region.class_RegionalData import *
from library.imexport.class_Excel import *

ad = AdminCode()
client = MongoClient('localhost',27017)
db = client['regionDB']
conn = db['cProvince']
conn2 = db['ProvinceStatistics']

result = []
records = conn.find()

conn2 = db['ProvinceStatistics']
for item in records:
    item.pop('_id')
    value = item.pop('value')
    for key in value:
        nitem = item.copy()
        nitem['year'] = key
        nitem['value'] = value[key]
        print(nitem)
        conn2.insert(nitem)




