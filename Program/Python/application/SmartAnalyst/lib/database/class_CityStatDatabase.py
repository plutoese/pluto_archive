# coding=UTF-8

#-----------------------------------------------------------------------------------
# class_CityStatDatabase文件
# @class: CityStatDatabase类
# @introduction: CityStatDatabase类用来处理城市统计数据库
# @dependency: re包，pandas包，pymongo包，Database类，AdminData类，RegionFormat类
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------------

'''
.. code-block:: python

    db = CityStatDatabase()
    print(db.period(u'职工平均工资'))

    print(db.variables)
    print(db.collection)
    projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
    conds = {'region':[[u'上海'],[u'浙江',u'杭州市']],'year':[2010],'variable':[u'人均地区生产总值',u'职工平均工资'],'scale':u'全市','projection':projection}
    conds = {'region':[u't'],'year':[2012],'variable':[u'人均地区生产总值',u'职工平均工资'],'projection':projection}
    mdata = db.find(conds)
    print('-----------------------------')
    print(mdata)
'''

import re
import pandas as pd
from lib.database.class_Database import Database
from lib.data.class_AdminData import AdminData
from lib.data.class_RegionFormat import RegionFormat
from pymongo import ASCENDING

class CityStatDatabase(Database):
    '''CityStatDatabase类用来处理城市统计数据库

    '''
    def __init__(self):
        Database.__init__(self)
        self.connect('regionDB','CityStatistics')
        self.ad = AdminData()

    def find(self,conds,is_to_standard_form=True):
        '''查询城市统计年鉴的区域数据

        :param dict conds: 查询条件
        :param bool is_to_standard_form: 标示参数，表示是否输出为标准格式
        :return: 城市统计年鉴的区域数据
        :rtype: list
        '''
        projection = conds.get('projection')
        if projection is None:
            projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
        else:
            conds.pop('projection')
        # 设置sorts
        sorts = conds.get('sorts')
        if sorts is None:
            sorts= [('year',ASCENDING),('acode',ASCENDING)]
        else:
            conds.pop('sorts')

        # 设置时间
        period = conds.get('year')
        if period is None:
            variables = conds.get('variable',self.variables)
            period = self.period(variables)
        else:
            conds.pop('year')

        result = []
        conditions = dict()
        for key in conds:
            if re.match('region',key) is not None:
                continue
            if isinstance(conds[key],list):
                conditions[key] = {'$in':conds[key]}
            else:
                conditions[key] = conds[key]

        # 重点是设置区域
        if 'region' in conds:
            for year in period:
                conditions['year'] = year
                self.ad.set_year(year)
                conditions['acode'] = {'$in':[region['acode'] for item in conds['region'] for region in self.ad[tuple(item)]]}
                result.extend(list(self.collection.find(conditions,projection).sort(sorts)))
            result_found = pd.DataFrame(result)
        else:
            if isinstance(period,list):
                conditions['year'] = {'$in':period}
            else:
                conditions['year'] = period
            result_found = pd.DataFrame(list(self.collection.find(conditions,projection).sort(sorts)))

        result = result_found.drop_duplicates(take_last=True)

        if is_to_standard_form:
            return RegionFormat(result).transform()
        else:
            return result

    @property
    def variables(self):
        return self.collection.find().distinct('variable')

    def period(self,variable):
        '''获得变量的所有时期

        :param str,list variable: 变量
        :return: 变量的年份
        :rtype: list
        '''
        if isinstance(variable,str):
            posts = self.collection.find({'variable':variable}).distinct('year')
        else:
            posts = set()
            for var in variable:
                periods = self.collection.find({'variable':var}).distinct('year')
                posts.update(periods)
            posts = list(posts)
        return sorted(posts)


if __name__ == '__main__':
    db = CityStatDatabase()
    print(db.period(u'职工平均工资'))

    print(db.variables)
    print(db.collection)
    projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
    conds = {'region':[[u'上海'],[u'浙江',u'杭州市']],'year':[2010],'variable':[u'人均地区生产总值',u'职工平均工资'],'scale':u'全市','projection':projection}
    conds = {'region':[u't'],'year':[2012],'variable':[u'人均地区生产总值',u'职工平均工资'],'projection':projection}
    mdata = db.find(conds)
    print('-----------------------------')
    print(mdata)


















