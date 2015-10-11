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
    mdata = rdata.query(region=[[u'上海'],[u'浙江',u'杭州市']],year=[2009,2010],variable=[u'人均地区生产总值',u'职工平均工资'],scale=u'全市')
    print(mdata.keys())

















