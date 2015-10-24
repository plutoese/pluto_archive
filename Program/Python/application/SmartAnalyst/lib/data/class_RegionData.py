# coding=UTF-8

#--------------------------------------------------------------
# class_RegionData文件
# @class: RegionData类
# @introduction: RegionData类表示区域数据
# @dependency: pandas包，Data类，CityStatDatabase类
# @author: plutoese
# @date: 2015.10.18
#--------------------------------------------------------------

'''
.. code-block:: python

    rdata = RegionData()
    vars = ['年末总人口', '第一产业年末单位从业人员']
    mdata = rdata.find(region=['t'],year=[2010])
    mdata = rdata.find(region=[[u'北京'],[u'上海']],variable=vars)
    print(mdata.keys())
    print(mdata['data'])
    file = 'd:/down/citydata.xls'
    mdata['data'].to_excel(file)
'''

import pandas as pd
from lib.data.class_Data import Data
from lib.database.class_CityStatDatabase import CityStatDatabase

class RegionData:
    '''RegionData类表示区域数据

    '''
    # 设置数据库集合
    databases = [CityStatDatabase()]

    # 构造函数
    def __init__(self):
        Data.__init__(self)

    def find(self,**conds):
        '''查询多个数据库得到结果

        :param dict conds: 查询条件
        :return: 查询得到的区域数据
        :rtype: dict
        '''
        merge_type = conds.get('merge_type')
        if merge_type is None:
            merge_type = 'outer'
        else:
            conds.pop('merge_type')

        print(conds)
        result = self.databases[0].find(conds)

        # 连接多个数据库查询的结果
        for key in self.databases[1:]:
            result_found = self.databases[key].find(conds)
            result['data'] = pd.merge(result['data'], result_found['data'], left_index=True, right_index=True, how=merge_type)

        return result

if __name__ == '__main__':
    rdata = RegionData()
    vars = ['年末总人口', '第一产业年末单位从业人员']
    mdata = rdata.find(region=['t'],year=[2010])
    #mdata = rdata.find(region=[[u'北京'],[u'上海']],variable=vars)
    print(mdata.keys())
    print(mdata['data'])
    file = 'd:/down/citydata.xls'
    mdata['data'].to_excel(file)


















