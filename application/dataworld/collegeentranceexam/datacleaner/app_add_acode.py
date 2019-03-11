# coding = UTF-8

import re
from pymongo import ASCENDING
from lib.base.database.class_mongodb import MongoDB, MonCollection

mongo = MongoDB(conn_str='localhost:27017')
province_con = MonCollection(mongo, database='regiondata', collection_name='provinces').collection
college_info_con = MonCollection(mongo, database='webdata', collection_name='college_info').collection
entrance_score_con = MonCollection(mongo, database='webdata', collection_name='gaokao_entrancescore').collection

provinces = province_con.find(projection={'_id':False, 'name':True, 'id':True}, sort=[('id',ASCENDING)])
province_dict = {province['name']:province['id'] for province in provinces}

COLLEGE_INFO = False
ENTRANCE_EXAM = True

if COLLEGE_INFO:
    for item in college_info_con.find(projection={'_id':True, '高校所在地':True, '学校':True}):
        location = item['高校所在地']
        for province in province_dict:
            if re.search(location,province) is not None:
                location_acode = province_dict[province]
                break
        college_info_con.find_one_and_update({'_id': item['_id']},{'$set': {'高校所在地行政代码': location_acode}})

if ENTRANCE_EXAM:
    for item in entrance_score_con.find(projection={'_id':True, 'region':True, 'university':True}):
        location = item['region']
        for province in province_dict:
            if re.search(location,province) is not None:
                location_acode = province_dict[province]
                break
        print(item)
        entrance_score_con.find_one_and_update({'_id': item['_id']},{'$set': {'regioncode': location_acode}})