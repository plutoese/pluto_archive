# coding = UTF-8

from application.dataworld.admindivision.class_admindivision import AdminDivision
from application.dataworld.CEIC.class_ceic import CEICDatabase, CEIC

adivision = AdminDivision(year='2010')
print(adivision.province.columns)
province_name = list(adivision.province['region'])
print(province_name)

mceic = CEIC()
print(mceic.variables)
result = mceic.find(variable=[u'财政支出', u'财政收入', u'国内生产总值', u'从业人数_制造业'], year=list(range(2010, 2011)))
print(result)