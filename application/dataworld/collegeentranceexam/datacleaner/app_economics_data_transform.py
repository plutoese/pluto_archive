# coding = UTF-8

import re
import pandas as pd
from pymongo import ASCENDING
from lib.base.database.class_mongodb import MongoDB, MonCollection

# 1. 初始化
mongo = MongoDB(conn_str='localhost:27017')
province_con = MonCollection(mongo, database='regiondata', collection_name='provinces').collection
provinces = province_con.find(projection={'_id':False, 'name':True, 'id':True}, sort=[('id',ASCENDING)])
province_dict = {province['name']:province['id'] for province in provinces}

perGDP_filepath = r'E:\cyberspace\worklot\college\province_perGDP.xlsx'
perGDP = pd.read_excel(perGDP_filepath)

# 2.匹配省份名称
for ind in perGDP.index:
    region = perGDP.loc[ind,'region']
    region = re.sub('\s+','',region)
    for province in province_dict:
        if re.search(region,province) is not None:
            perGDP.loc[ind, 'province'] = province
            perGDP.loc[ind, 'acode'] = province_dict[province]
            break

# 3. 转换以2011年为基年的实际人均GDP
perGDP['realperGDP2012'] = (perGDP['perGDP2011']).mul(perGDP['index2012']/100)
perGDP['realperGDP2013'] = (perGDP['realperGDP2012']).mul(perGDP['index2013']/100)
perGDP['realperGDP2014'] = (perGDP['realperGDP2013']).mul(perGDP['index2014']/100)
perGDP['realperGDP2015'] = (perGDP['realperGDP2014']).mul(perGDP['index2015']/100)

# 4. 导出数据
perGDP.to_excel(r'E:\cyberspace\worklot\college\province_realperGDP.xlsx')