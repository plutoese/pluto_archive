# coding = UTF-8

from application.dataworld.admindivision.class_admindivision import AdminDivision
from application.dataworld.citystat.class_citystatisticsdatabase import CityStatisticsDatabase, CityStatistics

adivision = AdminDivision(year='2010')
print(adivision.province.columns)
province_name = list(adivision.province['region'])
print(province_name)

city_database = CityStatisticsDatabase()
vars = [var[0] for var in city_database.variables.values]
print(vars)

'''
city_stat = CityStatistics()
result = city_stat.find(year=list(range(2000,2016)),boundary='全市')
result.to_excel('D:/down/yadongdata/citydata.xlsx')'''