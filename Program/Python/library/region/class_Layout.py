# coding=UTF-8

from library.region.class_RegionalData import *
import pandas as pd

# 类Layout用于各种数据结构的转换
class Layout:
    # 构造函数
    def __init__(self,data=None):
        self.ad = AdminCode()
        self._data = data
        self._type()

        self.type = self._type()
        self.ndim = {'year':len(self.type['year']),'variable':len(self.type['variable']),'region':len(self.type['region'])}

    # 格式转换
    def stackToNormal(self):
        #  构建时间序列数据
        if (self.ndim['variable'] == 1) and (self.ndim['region'] == 1):
            #data = pd.Series(dict(zip(year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])))
            #d = dict(zip(year,data))
            sname = '|'.join([self.region[0],self.variable[0]])
            return pd.Series(dict(zip(self.year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])),name=sname)

        # 构建横截面数据(地区|变量)
        if self.ndim['year'] == 1:
            g1 = [group for name,group in self._data.groupby(['year'], sort=True)][0]
            g2 = g1.groupby(['variable'], sort=True)
            i = 0
            mdata = []
            for name,data in g2:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.getByAcode(item)['region'] for item in mdata.index])
            return mdata

        # 构建横截面数据(地区|时间)
        if self.ndim['variable'] == 1:
            g = self._data.groupby(['year'], sort=True)
            i = 0
            mdata = []
            for name,data in g:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.getByAcode(item)['region'] for item in mdata.index])
            return mdata

        # panel data
        g = self._data.groupby(['year'], sort=True)
        year = []
        pdata =[]
        for y,g1 in g:
            g2 = g1.groupby(['variable'], sort=True)
            i = 0
            mdata = []
            for name,data in g2:
                rdata = pd.DataFrame({name:data['value'].values},index=data['acode'].values)
                if i == 0:
                    mdata = rdata
                else:
                    mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                i = i + 1
            mdata.insert(0, 'region', [self.ad.getByAcode(item)['region'] for item in mdata.index])
            year.append(str(y))
            pdata.append(mdata)
        result = pd.Panel(dict(zip(year,pdata)))
        return result


    # 辅助函数，返回数据结构
    def _type(self):
        g = self._data.groupby(['year'], sort=True)
        self.year = [name for name, group in g]
        self.year = [str(item) for item in self.year]

        g = self._data.groupby(['acode'], sort=True)
        self.acode = [name for name, group in g]
        self.region = [ad.getByAcode(item)['region'] for item in self.acode]

        g = self._data.groupby(['variable'], sort=True)
        self.variable = [name for name, group in g]

        return {'year':self.year,'region':self.region,'variable':self.variable}

if __name__ == '__main__':
    ad = AdminCode()
    rdata = RegionalData()
    mdata = rdata.query(region=ad[u'浙江',u'f'],year=range(2006,2010),variable=[u'财政支出',u'从业人数_在岗职工'])
    #mdata = rdata.query(region=[ad[u'浙江',u'杭州']],variable=[u'财政支出'])
    #mdata = rdata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出'],year=range(2005,2013))
    #mdata = rdata.query(region=ad[u'浙江',u'杭州'],variable=u'财政支出',year=range(2000,2012))
    lout = Layout(mdata)
    print(lout.type)
    print(lout.ndim)

    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    g = mdata.groupby(['year'], sort=True)
    print(g)

    for name, group in g:
        print(name)
        print(group)
        print(group['value'])

    print('*****************************************')
    g = group.groupby(['variable'], sort=True)
    i = 0
    for name, group in g:
        print('not',i)
        print(name)
        print(group)
        i = i + 1

    print('-----------------------------------------')
    mdata = lout.stackToNormal()
    print(mdata)
    print(mdata.axes)
    print(mdata['2007'])

