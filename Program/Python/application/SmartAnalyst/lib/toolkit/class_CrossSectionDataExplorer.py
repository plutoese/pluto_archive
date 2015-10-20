# coding=UTF-8

#-----------------------------------------------------------------------------------------------------
# class_CrossSectionDataExplorer文件
# @class: CrossSectionDataExplorer类
# @introduction: CrossSectionDataExplorer类用来进行横截面数据分析
# @dependency: seaborn包，pandas包，numpy包，statsmodels包，matplotlib包，datetime包，RegionData类
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------------------------------

'''
.. code-block:: python

    rdata = RegionData()
    mdata = rdata.find(region=['t'],year=[2010],variable=[u'地区生产总值',u'年末总人口'],scale=u'全市')
    mdata = mdata['data']
    csdexplorer = CrossSectionRegionDataExplorer(mdata)
    dframe = csdexplorer.per_variable(pop=mdata[u'年末总人口'],var=[u'地区生产总值',u'年末总人口'])
    print(dframe)
    dframe = csdexplorer.log_variable(u'地区生产总值')
    dframe2 = csdexplorer.describe().applymap(lambda x:'{0:.2f}'.format(x))
    print(dframe2)
    csdexplorer.hist(var=u'地区生产总值',save=True)
    csdexplorer.scatter(y=u'地区生产总值',x=u'年末总人口',kind='kde')
    csdexplorer.pair(vars=[u'地区生产总值',u'年末总人口'])

    csdexplorer.ols(y=u'地区生产总值',x=u'年末总人口')
    print(csdexplorer.corr())

    pdata = {'region':['1','2','3'],'x':[1,2,-3],'y':[4,5,6]}
    pdata = pd.DataFrame(pdata)
    cs2 = CrossSectionRegionDataExplorer(pdata)
    print(cs2.is_positive(var=['y']))
'''

import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
from lib.data.class_RegionData import RegionData

class CrossSectionDataExplorer:
    '''类CrossSectionDataExplorer用来进行横截面数据分析

    :param pandas.DataFrame data: 数据
    '''
    def __init__(self,data):
        self._data = data
        self.index = self._data.index
        self.columns = self._data.columns


class CrossSectionRegionDataExplorer(CrossSectionDataExplorer):
    '''类CrossSectionRegionDataExplorer用来对横截面区域数据进行分析处理

    :param pandas.DataFrame data: 区域数据
    '''
    def __init__(self,data=None):
        CrossSectionDataExplorer.__init__(self,data)
        self.region = self._data['region']

        # 初始化图形接口
        sns.set(style="white", palette="muted", color_codes=True)
        # 设置中文字体
        sns.set_style('white',{"font.sans-serif":  ['Microsoft YaHei','Arial', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']})

    def describe(self):
        '''数据的概要统计分析

        :return: 概要统计分析
        :rtype: pandas.DataFrame
        '''
        return self._data.describe()

    def ols(self,y=None,x=None):
        '''最小二乘法

        :param str y: 被解释变量
        :param str,list x: 解释变量
        :return: 回归结果
        :rtype: statsmodels.RegressionResults对象
        '''
        y = self._data[y]
        x = pd.DataFrame(self._data[x])
        x.insert(0,'constant',1)
        mod = sm.OLS(y,x)
        res = mod.fit()
        print(res.summary())
        return res

    def corr(self,vars=None):
        '''相关系数

        :param list vars: 变量
        :return: 相关系数
        :rtype: pandas.DataFrame
        '''
        if vars is None:
            return self._data[self.columns[1:]].corr()
        else:
            return self._data[vars].corr()

    def ratio_variable(self,total,var):
        '''计算占比变量

        :param str total: 总体变量
        :param str,list var: 局部变量
        :return: 占比变量
        :rtype: pandas.DataFrame
        '''
        return self.per_variable(pop=total,var=var,weight=100,prefix=u'占比')

    def per_variable(self,pop,var,weight=1,prefix=u'人均'):
        '''计算人均变量

        :param str,list pop: 总体变量
        :param str,list var: 局部变量
        :param int weight: 权重
        :param str prefix: 变量前缀
        :return: 人均变量
        :rtype: pandas.DataFrame
        '''
        if isinstance(pop,str):
            pop = self._data[pop]
        if isinstance(var,str):
            var = [var]
        ndata = {}
        for v in var:
            if weight is None:
                ndata['_'.join([prefix,v])] = self._data[v]/pop
            else:
                ndata['_'.join([prefix,v])] = weight*self._data[v]/pop
        frame = pd.DataFrame(ndata)
        frame.index = self.index
        frame.insert(0, 'region',self._data['region'])
        return frame

    def log_variable(self,var):
        '''计算对数变量

        :param str,list var: 变量
        :return: 对数变量
        :rtype: pandas.DataFrame
        '''
        if isinstance(var,str):
            var = [var]
        ndata = {}
        for v in var:
            if self.is_positive(v):
                ndata['_'.join([v,u'对数'])] = np.log(self._data[v])
            else:
                print(v,' is not all positive.')
                raise ValueError
        frame = pd.DataFrame(ndata)
        frame.index = self.index
        frame.insert(0, 'region',self._data['region'])
        return frame

    def hist(self,var,save=False):
        '''直方图

        :param str,list var: 变量
        :param bool save: 指示变量，表示是否存储图片
        :return: 对数变量
        :rtype: pandas.DataFrame
        '''
        sns.distplot(self._data[var])
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    def scatter(self,y=None,x=None,kind='reg',save=False):
        '''散点图

        :param str y: 被解释变量
        :param str x: 解释变量
        :param str kind: 添加的拟合线，可以使'reg'或'kde'
        :param bool save: 指示变量，表示是否存储图片
        :return: 无返回值
        '''
        g = sns.jointplot(x=x, y=y, data=self._data, kind=kind)
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    def pair(self,vars=None,save=False):
        '''散点图矩阵

        :param str vars: 变量
        :param bool save: 指示变量，表示是否存储图片
        :return: 无返回值
        '''
        sns.pairplot(self._data[vars])
        if save:
            self._save()
        else:
            plt.show()
        plt.close()

    def is_positive(self,var):
        '''检验变量是否为正

        :param str,list vars: 变量
        :return: 某个变量是否为正
        :rtype: bool
        '''
        if isinstance(var,str):
            var = [var]
        for v in var:
            if not (self._data[v]>0).all():
                return False
        return True

    # 储存图像
    def _save(self,savepath='E:/Report/'):
        x = str(int(datetime.now().timestamp()*1000))
        filename = savepath + 'graph/' + x + '.pdf'
        plt.savefig(filename)


if __name__ == '__main__':
    rdata = RegionData()
    mdata = rdata.find(region=['t'],year=[2010],variable=[u'地区生产总值',u'年末总人口'],scale=u'全市')
    mdata = mdata['data']
    csdexplorer = CrossSectionRegionDataExplorer(mdata)
    dframe = csdexplorer.per_variable(pop=mdata[u'年末总人口'],var=[u'地区生产总值',u'年末总人口'])
    print(dframe)
    dframe = csdexplorer.log_variable(u'地区生产总值')
    dframe2 = csdexplorer.describe().applymap(lambda x:'{0:.2f}'.format(x))
    print(dframe2)
    csdexplorer.hist(var=u'地区生产总值',save=True)
    csdexplorer.scatter(y=u'地区生产总值',x=u'年末总人口',kind='kde')
    csdexplorer.pair(vars=[u'地区生产总值',u'年末总人口'])

    csdexplorer.ols(y=u'地区生产总值',x=u'年末总人口')
    print(csdexplorer.corr())

    pdata = {'region':['1','2','3'],'x':[1,2,-3],'y':[4,5,6]}
    pdata = pd.DataFrame(pdata)
    cs2 = CrossSectionRegionDataExplorer(pdata)
    print(cs2.is_positive(var=['y']))
















