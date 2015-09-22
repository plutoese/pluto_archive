# coding=UTF-8

from library.imexport.class_FileSystem import *
from library.datapretreatment.class_AdminCodeDataSheet import *
from pymongo import *
import pandas as pd

# 1. Connect to MongoDB collection
client = MongoClient('localhost', 27017)
db = client['regionDB']
collection = db['cCity']

# 2. query
YEAR = '2000'
#SORT = [('source.tablenum',ASCENDING),('acode',ASCENDING)]
#querydict = {'year':YEAR}
#mdata = list(collection.find(querydict).sort(SORT).distinct('variable')

result = []
mdata = collection.find({'year':YEAR}).distinct('source.tablenum')
for tnum in mdata:
    rdata = collection.aggregate([{'$match':{'year':YEAR,'source.tablenum':tnum}},{'$group':{'_id':'$variable'}}])
    rdata = list(reversed([item['_id'] for item in rdata]))
    inresult = [tnum]
    for item in rdata:
        cdata1 = collection.find_one({'year':YEAR,'variable':item,'scale':'全市'})
        if cdata1 is not None:
            if cdata1['unit'] is not None:
                inresult.append(':'.join([item,'全市',cdata1['unit']]))
            else:
                inresult.append(':'.join([item,'全市']))
        cdata2 = collection.find_one({'year':YEAR,'variable':item,'scale':u'市辖区'})
        if cdata2 is not None:
            if cdata2['unit'] is not None:
                inresult.append(':'.join([item,u'市辖区',cdata2['unit']]))
            else:
                inresult.append(':'.join([item,u'市辖区']))
    result.append(inresult)
    print(inresult)

print(result)

outfile = 'C:/Data/database/m2000.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(result)
moutexcel.close()
