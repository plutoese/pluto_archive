# coding=UTF-8

from library.imexport.class_MongoDB import *
from library.region.AdminCode.class_AdministrativeCode import *
import pandas as pd

# 0 function
def query(conn,**conds):
    cons = dict()
    for key in conds:
        if isinstance(conds[key],list):
            cons[key] = {'$in':conds[key]}
        else:
            cons[key] = conds[key]
    print(cons)
    result = conn.find(cons)
    return result

# to connect to Mongodb database
db = MongoDB()
conn = db.connect('regionDB','CityStatistics')
#result = query(conn,year={'$in':[2010,2011]})
result = query(conn,year=[2010,2011])
print(list(result))




