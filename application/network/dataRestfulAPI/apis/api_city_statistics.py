# coding=UTF-8

import re
from flask_restplus import Resource, Namespace, fields
from dist.lib.class_admindivision import AdminDivision
from dist.lib.class_citystatisticsdatabase import CityStatisticsDatabase, CityStatistics


api = Namespace('City Statistics', description='中国城市统计年鉴数据')

# 连接城市统计年鉴数据库
city_database = CityStatisticsDatabase()
city_stat_variables = [var[0] for var in city_database.variables.values]
city_stat_period = [int(var[0]) for var in city_database.period.values]

# City Statistics Variables
@api.route('/variables/<string:var>')
class CityStatVariable(Resource):
    def get(self, var):
        if var == 'all':
            return {'variable': city_stat_variables}
        else:
            result = []
            for item in city_stat_variables:
                if re.search(var,item):
                    result.append(item)
            return {'variable': result}

# City Statistics Period
@api.route('/period')
class CityStatPeriod(Resource):
    def get(self):
        print({'period': city_stat_period})
        return {'period': city_stat_period}
