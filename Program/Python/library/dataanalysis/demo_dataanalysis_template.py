# coding=UTF-8

from library.dataset.class_RegionDataSet import *

# 1. to setup Parameters and Objects
AD = AdminCode()
regionData = RegionalData()

# 2. to make a query
#query = regionData.query(region=AD[u'浙江',u'f'],variable=[u'国内生产总值_人均'])
#query = regionData.query(region=AD[u'浙江',u'杭州'],variable=[u'国内生产总值_人均'])
query = regionData.query(region=AD[u'浙江',u'f'],variable=[u'财政支出',u'国内生产总值_人均'])

# 3. to transform data struct and configure information
layout = Layout(query)
data = layout.stackToNormal()
information = layout.information

# 4. to pack a data set
mdataset = RegionDataSet(data,information)

# 5. to data analysis
print(mdataset._data)
mdataset.tsline(region=[u'杭州市',u'宁波市'],var=u'财政支出')



