# coding = UTF-8

import re
import pandas as pd
from pymongo import ASCENDING
from lib.base.database.class_mongodb import MongoDB, MonCollection
from application.dataworld.admindivision.class_admindivision import AdminDivision
from application.dataworld.citystat.class_citystatisticsdatabase import CityStatisticsDatabase, CityStatistics

# 1. 初始化
city_database = CityStatisticsDatabase()
city_stat = CityStatistics()

college_with_city_filepath = r'E:\cyberspace\worklot\college\colleges_with_city_stat.xlsx'
college_with_city = pd.read_excel(college_with_city_filepath)

adivision = AdminDivision(year='2012')

# 2. 城市名称
cities = list(college_with_city['city'])
cities = set(cities)
cities = list(cities)

city_name = []
city_code = []
for city in cities:
    result = adivision[city]
    city_name.append(result['region'].values[0])
    city_code.append(result['acode'].values[0])

# 3. city statistics
city_stat_pd = city_stat.find(variable=['人口密度','人均地区生产总值','地区生产总值','地区生产总值增长率',
                                  '年末总人口','普通高等学校数'],region=city_name,boundary='全市')

'''
result = pd.DataFrame({'region': cities, 'region_name': city_name, 'region_code': city_code})
result = result.sort_values(by=['region_code'])
result.to_excel(r'E:\cyberspace\worklot\college\city_statistics.xlsx')'''

city_stat_pd.to_excel(r'E:\cyberspace\worklot\college\city_statistics_pd.xlsx')