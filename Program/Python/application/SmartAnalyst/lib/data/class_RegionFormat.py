# coding=UTF-8

#-----------------------------------------------------------------------------
# class_RegionFormat文件
# @class: RegionFormat类
# @introduction: RegionFormat类用来转换区域数据格式
# @dependency: re包，pandas包，Database类，AdminData类，Format类
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------

import re
import pandas as pd
from lib.data.class_Format import Format
from lib.data.class_AdminData import AdminData

class RegionFormat(Format):
    '''RegionFormat类用来进行区域数据格式转换

    :param list data: 区域数据
    '''
    def __init__(self,data):
        Format.__init__(self,data)
        self.ad = AdminData()
        self.to_set_type()

    # 转换格式
    def transform(self,sourcetype='stack',targettype='normal',connect='outer'):
        if (re.match('stack',sourcetype) is not None) and (re.match('normal',targettype) is not None):
            return self.stack_to_normal(connect=connect)

    def stack_to_normal(self,connect):
        '''转换区域数据格式，从stack格式到normal格式

        :param str connect: 区域横截面数据连接方式，可以分别是'inner'或'outer'
        :return: dict
        '''
        scale = self.ndim.get('scale')
        # 当存在全市和市辖区的差别的时候
        if (scale is not None) and scale > 1:
            # 构建横截面数据(地区|变量)
            if self.ndim['year'] == 1:
                g1 = [group for name,group in self._data.groupby(['year'], sort=True)][0]
                region_dict = dict(zip(g1['acode'],g1['region']))
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
                mdata.insert(0, 'region', [region_dict[i] for i in mdata.index])
                return {'tags':tags,'data':mdata}

            # panel data
            g = self._data.groupby(['year'], sort=True)
            year = []
            pdata =[]
            for y,g1 in g:
                region_dict = dict(zip(g1['acode'],g1['region']))
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
                mdata.insert(0, 'region', [region_dict[i] for i in mdata.index])
                year.append(str(y))
                pdata.append(mdata)
            result = pd.Panel(dict(zip(year,pdata)))
            mdata = result.swapaxes('items','minor')
            mdata = mdata.swapaxes('major','minor')
            mdata = mdata.to_frame(False)
            result2 = result.dropna(axis=1)
            mdata2 = result2.swapaxes('items','minor')
            mdata2 = mdata2.swapaxes('major','minor')
            mdata2 = mdata2.to_frame(False)
            return {'data':mdata,'pdata':result,'balanceddata':mdata2}
        # 如果没有scale，或者scale为1
        else:
            # 时间序列模型
            if (self.ndim['variable'] == 1) and (self.ndim['region'] == 1):
                tags = {'variable':self.variable[0],'region':self.ad.get_by_acode(self.acode[0])[0]['region']}
                result = pd.Series(dict(zip(self.year,[group for name, group in self._data.groupby(['acode','variable'],sort=True)][0]['value'])))
                if scale is not None:
                    tags['scale'] = self.scale[0]
                return {'tags':tags,'data':result}

            # 构建横截面数据(地区|变量)
            if self.ndim['year'] == 1:
                g1 = [group for name,group in self._data.groupby(['year'], sort=True)][0]
                region_dict = dict(zip(g1['acode'],g1['region']))
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
                mdata.insert(0, 'region', [region_dict[i] for i in mdata.index])
                tags = {'year':self.year[0]}
                if scale is not None:
                    tags['scale'] = self.scale[0]
                return {'tags':tags,'data':mdata}

            # panel data
            g = self._data.groupby(['year'], sort=True)
            year = []
            pdata =[]
            for y,g1 in g:
                region_dict = dict(zip(g1['acode'],g1['region']))
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
                mdata.insert(0, 'region', [region_dict[i] for i in mdata.index])
                year.append(str(y))
                pdata.append(mdata)
            result = pd.Panel(dict(zip(year,pdata)))
            mdata = result.swapaxes('items','minor')
            mdata = mdata.swapaxes('major','minor')
            mdata = mdata.to_frame(False)
            result2 = result.dropna(axis=1)
            mdata2 = result2.swapaxes('items','minor')
            mdata2 = mdata2.swapaxes('major','minor')
            mdata2 = mdata2.to_frame(False)
            if scale is not None:
                tags = {'scale':self.scale}
                return {'tags':tags,'data':mdata,'pdata':result,'balanceddata':mdata2}
            else:
                return {'data':mdata,'pdata':result,'balanceddata':mdata2}

    # 辅助函数，返回数据结构
    def to_set_type(self):
        '''辅助函数，用来设置区域数据的参数

        :return: 无返回值
        '''
        # 设定年份
        g = self._data.groupby(['year'], sort=True)
        self.year = [str(name) for name, group in g]

        # 设定行政区域代码
        g = self._data.groupby(['acode'], sort=True)
        self.acode = [name for name, group in g]
        self.number_of_region = len(g.groups)

        # 设定变量
        g = self._data.groupby(['variable'], sort=True)
        self.variable = [name for name, group in g]

        # 设定变量的维度
        self.ndim = {'year':len(self.year),'variable':len(self.variable),'region':self.number_of_region}

        # 设定区域尺度：全市或者市辖区
        if 'scale' in self._data.columns:
            g = self._data.groupby(['scale'],sort=True)
            self.scale = [name for name, group in g]
            self.ndim['scale'] = len(self.scale)

if __name__ == '__main__':
    pass




















