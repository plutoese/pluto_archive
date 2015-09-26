# coding=UTF-8

from pymongo import *
import pandas as pd
from library.region.class_AdminCode import *
from library.region.class_RegionalData import *

ad = AdminCode()
rdata = RegionalData(collection='cProvince')
print(rdata.variables())
#mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
#print(mdata)

