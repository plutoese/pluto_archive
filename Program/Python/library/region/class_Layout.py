# coding=UTF-8

from library.region.class_RegionalData import *

# 类Layout用于各种数据结构的转换
class Layout:
    # 构造函数
    def __init__(self,data=None):
        self._data = data
        self._determType()

    # 格式转换
    def stackToNormal(self):
        pass

    def _determType(self):
        g = mdata.groupby(['year'], sort=True)
        self.year = [name for name, group in g]

        g = mdata.groupby(['acode'], sort=True)
        self.region = [name for name, group in g]

        g = mdata.groupby(['variable'], sort=True)
        self.variable = [name for name, group in g]




if __name__ == '__main__':
    ad = AdminCode()
    rdata = RegionalData()
    #mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    #mdata = rdata.query(region=ad[u'浙江',u'f'],variable=u'财政支出',year=2012)
    mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=2012)
    lout = Layout(mdata)

    g = mdata.groupby(['acode'], sort=True)
    print(g)

    for name, group in g:
        print(name)
        print(group)
        print(group['value'])
