# coding=UTF-8

import re
import pymongo
import pandas as pd
from lib.base.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from application.dataworld.admindivision.class_admindivision import AdminDivision


class CEICDatabase:
    def __init__(self):
        """ 初始化中国城市统计数据库接口

        """
        mongo = MongoDB(conn_str='localhost:27017')
        self.conn = MonCollection(mongo,database='regiondata',collection_name='CEIC').collection

    def find(self,*args,**kwargs):
        """ 调用查询接口

        :param args:
        :param kwargs:
        :return:
        """
        found = list(self.conn.find(*args,**kwargs))
        if len(found) > 0:
            found_data = pd.DataFrame(found)
            found_data['var'] = found_data['variable'] + found_data['unit'].apply(lambda x: ''.join(['(',x,')']))
            pdata = pd.pivot_table(found_data, values='value', index=['year', 'acode', 'region'], columns=['var'])
            pdata = pdata.swaplevel(0, 1, axis=0)
            return pdata

    @property
    def variables(self):
        found = self.conn.find().distinct('variable')
        return found

    @property
    def regions(self):
        return None

class CEIC:
    # Construction
    def __init__(self):
        # to connect to Mongodb database
        self.ceic_databse = CEICDatabase()
        # Admin district
        self.admindivision = AdminDivision()

    def find(self,year=list(range(2000,2016)),variable=None,region=None):
        query_str = {'year':{'$in':year}}
        if variable is not None:
            if isinstance(variable,str):
                query_str['variable'] = variable
            elif isinstance(variable,(tuple,list)):
                query_str['variable'] = {'$in':variable}
            else:
                print('Unknown type!')
                raise Exception
        if region is not None:
            if isinstance(region,str):
                if re.match('^\d{6}$',region) is not None:
                    query_str['acode'] = region
                else:
                    for ye in year:
                        self.admindivision.set_year(ye)
                        found = self.admindivision[region]
                        if found.shape[0] > 0:
                            query_str['acode'] = str(found.iloc[0,0])
                            break
            elif isinstance(region,(tuple,list)):
                acodes = []
                for reg in region:
                    if isinstance(reg,str):
                        if re.match('^\d{6}$', reg) is not None:
                            acodes.append(region)
                        else:
                            for ye in year:
                                self.admindivision.set_year(ye)
                                found = self.admindivision[reg]
                                if found.shape[0] > 0:
                                    acodes.append(str(found.iloc[0, 0]))
                                    break
                    else:
                        for ye in year:
                            self.admindivision.set_year(ye)
                            found = self.admindivision[tuple(reg)]
                            if found.shape[0] > 0:
                                acodes.append(str(found.iloc[0, 0]))
                                break
                query_str['acode'] = {'$in':acodes}
            else:
                print('Unknown type!')
                raise Exception

        return self.ceic_databse.find(query_str,
                                      projection={'_id':0,'year':1,'acode':1,'region':1,'value':1,'unit':1,'variable':1},
                                      sort=[('year',pymongo.ASCENDING),('acode',pymongo.ASCENDING)])

    # to find out variable in database
    @property
    def variables(self):
        result = self.ceic_databse.variables
        return result

    # to sort regions
    def _sorted(self,alist,keyword):
        return sorted(alist,key = lambda x:x['keyword'])

if __name__ == '__main__':
    mceic = CEIC()
    result = mceic.find(variable=[u'财政支出',u'财政收入',u'国内生产总值',u'从业人数_制造业'],year=list(range(2005,2010)),region=[u'北京',u'上海'])
    print(result)

    print(mceic.variables)
    '''
    outfile = u'c:\\down\\demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new()
    moutexcel.append(result)
    moutexcel.close()'''
