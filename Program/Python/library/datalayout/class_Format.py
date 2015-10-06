# coding=UTF-8

import pandas as pd

from library.region.RegionData.class_RegionData import *


# 类Layout用于各种数据结构的转换
class Foramt:
    def __init__(self,data=None):
        self._data = data
        self.ad = AdministrativeCode()
        self._type()

    # 转换格式的主程序
    def transform(self,sourcetype='stack',targettype='normal',connect='outer'):
        if (re.match('stack',sourcetype) is not None) and (re.match('normal',targettype) is not None):
            return self._stackToNormal(connect=connect)


    def _stackToNormal(self,connect):
        scale = self.ndim.get('scale')
        # 当存在全市和市辖区的差别的时候
        if (scale is not None) and scale > 1:
            # 构建横截面数据(地区|变量)
            if self.ndim['year'] == 1:
                g1 = [group for name,group in self._data.groupby(['year'], sort=True)][0]
                g2 = g1.groupby(['variable','scale'], sort=True)
                i = 0
                mdata = []
                for name,data in g2:
                    rdata = pd.DataFrame({'_'.join(name):data['value'].values},index=data['acode'].values)
                    if i == 0:
                        mdata = rdata
                    else:
                        mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how=connect)
                    i = i + 1
                tags = {'year',self.year[0]}
                mdata.insert(0, 'region', [self.ad.getByAcodeAndYear(acode=item,year=self.year[0])['region'] for item in mdata.index])
                return {'tags':tags,'data':mdata}

            # panel data
            g = self._data.groupby(['year'], sort=True)
            year = []
            pdata =[]
            for y,g1 in g:
                g2 = g1.groupby(['variable','scale'], sort=True)
                i = 0
                mdata = []
                for name,data in g2:
                    rdata = pd.DataFrame({'_'.join(name):data['value'].values},index=data['acode'].values)
                    if i == 0:
                        mdata = rdata
                    else:
                        mdata = pd.merge(mdata,rdata,left_index=True,right_index=True,how='outer')
                    i = i + 1
                mdata.insert(0, 'region', [self.ad.getByAcodeAndYear(acode=item,year=self.year[0])['region'] for item in mdata.index])
                year.append(str(y))
                pdata.append(mdata)
            result = pd.Panel(dict(zip(year,pdata)))
            mdata = result.swapaxes('items','minor')
            mdata = mdata.swapaxes('major','minor')
            mdata = mdata.to_frame(False)
            return {'data':mdata,'pdata':result}
        # 如果没有scale，或者scale为1
        else:
            if (self.ndim['variable'] == 1) and (self.ndim['region'] == 1):
                tags = {'variable':self.variable[0],'region':self.ad.getByAcode(self.acode[0])['region']}
                result = pd.Series(dict(zip(self.year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])))
                if scale is not None:
                    tags['scale'] = self.scale[0]
                return {'tags':tags,'data':result}

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
                mdata.insert(0, 'region', [self.ad.getByAcodeAndYear(acode=item,year=self.year[0])['region'] for item in mdata.index])
                tags = {'year':self.year[0]}
                if scale is not None:
                    tags['scale'] = self.scale[0]
                return {'tags':tags,'data':mdata}

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
                mdata.insert(0, 'region', [self.ad.getByAcodeAndYear(acode=item,year=self.year[0])['region'] for item in mdata.index])
                year.append(str(y))
                pdata.append(mdata)
            print(year,pdata)
            result = pd.Panel(dict(zip(year,pdata)))
            mdata = result.swapaxes('items','minor')
            mdata = mdata.swapaxes('major','minor')
            mdata = mdata.to_frame(False)
            if scale is not None:
                tags = {'scale':self.scale}
                return {'tags':tags,'data':mdata,'pdata':result}
            else:
                return {'data':mdata,'pdata':result}

    # 辅助函数，返回数据结构
    def _type(self)->dict:
        g = self._data.groupby(['year'], sort=True)
        self.year = [str(name) for name, group in g]

        g = self._data.groupby(['acode'], sort=True)
        self.acode = [name for name, group in g]
        self.numOfRegion = len(g.groups)

        g = self._data.groupby(['variable'], sort=True)
        self.variable = [name for name, group in g]

        self.ndim = {'year':len(self.year),'variable':len(self.variable),'region':self.numOfRegion}

        if 'scale' in self._data.columns:
            g = self._data.groupby(['scale'],sort=True)
            self.scale = [name for name, group in g]
            self.ndim['scale'] = len(self.scale)

if __name__ == '__main__':
    rdata = RegionData()
    #mdata = rdata.query(region=[[u'浙江',u'f']],variable=[u'人均地区生产总值',u'职工平均工资'],year=[2012,2013])
    projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
    #mdata = rdata.query(region=[[u'浙江',u'f']],variable=[u'人均地区生产总值',u'职工平均工资'],year=[2010,2012],projection=projection)
    mdata = rdata.query(region=[[u'浙江',u'f']],variable=[u'人均地区生产总值',u'职工平均工资'],year=[2010,2012],projection=projection)
    print(mdata)

    fdata = Foramt(mdata)
    print(fdata.ndim)
    mdata = fdata.transform()
    print(mdata['data'])
    pdata = mdata['pdata']
    print(pdata)
    #print(mdata['stacked'])
    #print(mdata.xs(key='2010',axis=0))
    #mdata = mdata.swapaxes('items','minor')
    #mdata = mdata.swapaxes('major','minor')
    #print(mdata.to_frame(False))
    #g = mdata.groupby(['acode','year'],sort=True).first()
    #print(g)
    #records = g.to_records()
    #print(records)
    #print(dir(records))
    #for name,group in g:
    #    print(name)
    #    print(group)

