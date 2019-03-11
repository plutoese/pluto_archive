# coding = UTF-8

import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonCollection

mongo = MongoDB(conn_str='localhost:27017')
college_info_con = MonCollection(mongo, database='webdata', collection_name='college_info').collection

found = college_info_con.find({"高校性质" : "本科"}, projection={'_id':False, '高校所在地':True, '学校':True})
college_pd = pd.DataFrame(list(found))

college_pd.to_excel(r'E:\cyberspace\worklot\college\colleges.xlsx')

