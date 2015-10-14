# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.10
# @class: RegionData
# @introduction: 类RegionData表示区域数据。
# @property:
# @method:
# -----------------------------------------------------------------------------------------

import re
from application.DataWarehouse.data.class_data import Data
from application.DataWarehouse.database.class_citystatdatabase import CityStatDatabase


class RegionData:
    '''
    类Data表示行政区划数据
    '''
    # 设置数据库集合
    databases = {'citystatiscs':CityStatDatabase()}

    # 构造函数
    def __init__(self):
        Data.__init__(self)


    # 查询
    def query(self,**conds):
        for key in self.databases:
            result = self.databases[key].find(conds)

        return result

if __name__ == '__main__':
    rdata = RegionData()
    mdata = rdata.query(region=['t'],year=[2010])
    print(mdata.keys())
    print(mdata['data'])
    file = 'd:/down/citydata.xls'
    mdata['data'].to_excel(file)

















