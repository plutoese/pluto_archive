# coding=UTF-8

from library.imexport.class_FileSystem import *
from library.datapretreatment.class_AdminCodeDataSheet import *
from pymongo import *
import pandas as pd

# 1. Connect to MongoDB collection
client = MongoClient('localhost', 27017)
db = client['regionDB']
collection = db['AdminCode']

# 2. versions
versions = collection.find().distinct('version')
versions = sorted(versions)
versions = versions[1:(len(versions)-1)]

# 3. my collection
latestversion = '2014_10_31'
latestregions = list(collection.find({'version':latestversion}).sort([('acode',ASCENDING)]))
mregions = pd.DataFrame({'acode':[item['acode'] for item in latestregions],latestversion:[item['region'] for item in latestregions]})
mregions = mregions.set_index('acode')

for ver in versions:
    latestregions = list(collection.find({'version':ver}).sort([('acode',ASCENDING)]))
    newregion = pd.DataFrame({'acode':[item['acode'] for item in latestregions],ver:[item['region'] for item in latestregions]})
    newregion = newregion.set_index('acode')

    mregions = pd.merge(mregions,newregion,left_index=True,right_index=True,how='outer')

print(mregions)

file = 'C:/Data/database/region.xlsx'
mregions.to_excel(file)

