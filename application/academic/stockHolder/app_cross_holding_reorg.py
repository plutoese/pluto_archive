import os
import pickle
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonDatabase, MonCollection

mongo = MongoDB(conn_str='mongodb://root:z1Yh2900@dds-bp162bb74b8184e41658-pub.mongodb.rds.aliyuncs.com:3717')
mdb = MonDatabase(mongodb=mongo, database_name='enterprise')
mcon = MonCollection(mongo,mdb,'stock_share_holder')

#select = mcon.collection.find().distinct('所属基金/股票的代码_SecuCd')

#found = mcon.collection.find({'所属基金/股票的代码_SecuCd':'300342'})
found1 = mcon.collection.find({'所属基金/股票的代码_SecuCd': {'$regex': '^\d{6}$'}},
                              projection={'_id': 0, '上市公司代码_ComCd': 1, '最新公司全称_LComNm': 1,
                                          '截止日期_EndDt': 1, '信息发布日期_InfoPubDt': 1, '信息来源_InfoSource': 1,
                                          '股东名单_SHLst': 1, '股东性质_SHChrct': 1, '归属机构名称_InsBelNm': 1,
                                          '所属基金/股票的代码_SecuCd': 1, '所属基金/股票简称_SecuAbbr': 1,
                                          '公司总股数(股)_ComFullShr': 1, '流通股总股数(股)_TrdShr': 1,
                                          '持股数(股)_HoldSum': 1, '持股数占总股本比例_PctTotShr': 1,
                                          '持股数占流通股比例_PctTrdShr': 1})

pickle_file = open(r'E:\datahouse\projectdata\shareholder\all_cross_holding_data.pkl','wb')
pickle.dump(list(found1), pickle_file)
pickle_file.close()
