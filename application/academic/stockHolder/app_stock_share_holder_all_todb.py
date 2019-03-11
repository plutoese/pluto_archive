# coding = UTF-8

import os
import pickle
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonDatabase, MonCollection

mongo = MongoDB(conn_str='mongodb://root:z1Yh2900@dds-bp162bb74b8184e41658-pub.mongodb.rds.aliyuncs.com:3717')
mdb = MonDatabase(mongodb=mongo, database_name='enterprise')
mcon = MonCollection(mongo,mdb,'stock_share_holder')

share_holder_all_path = r'E:\cyberspace\notebook\Academic\Stock Holder\data\share_holder_all'

for a_file in os.listdir(share_holder_all_path):
    print(a_file)
    file_path = os.path.join(share_holder_all_path,a_file)
    share_holder_all_df = pd.read_excel(file_path)
    share_holder_all_df = share_holder_all_df.fillna('')
    '''
    columns_list = list(share_holder_all_df.columns)
    for ind in share_holder_all_df.index:
        data = list(share_holder_all_df.loc[ind,])
        record = dict(zip(columns_list,data))
        print(record)
        mcon.collection.insert_one(record)
    '''
    records = share_holder_all_df.to_dict('records')
    print(len(records))

    mcon.collection.insert_many(records)


