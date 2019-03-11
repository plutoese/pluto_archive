# coding = UTF-8

import os
import pickle
import numpy as np
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonDatabase, MonCollection

mongo = MongoDB(conn_str='mongodb://root:z1Yh2900@dds-bp162bb74b8184e41658-pub.mongodb.rds.aliyuncs.com:3717')
mdb = MonDatabase(mongodb=mongo, database_name='enterprise')
mcon = MonCollection(mongo,mdb,'cross_holding_data')

PROJECT_DATA_PATH = r'E:\datahouse\projectdata\shareholder'

file_path = os.path.join(PROJECT_DATA_PATH,'cross_holding_main_table.xls')
cross_holding_data_table = pd.read_excel(file_path)

vars = list(cross_holding_data_table.columns)
var_dtype = dict(zip(vars,[str]*len(vars)))
print(var_dtype) 
cross_holding_data_table = pd.read_excel(file_path, dtype=var_dtype)
#cross_holding_data_table = cross_holding_data_table.replace('nan',None)

records = cross_holding_data_table.to_dict('records')








