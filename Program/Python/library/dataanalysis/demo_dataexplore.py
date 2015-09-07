# coding=UTF-8

from pylab import *
from library.datapretreatment.class_DataSet import *
from library.dataanalysis.class_DataExplore import *
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

F = open(r'C:\Room\Warehouse\GitWork\Program\Python\library\dataset\CEICPdata.pkl','rb')
pdata = pickle.load(F)
dset = DataSet(pdata)
dset.setSubset(year=range(2000,2014),region=[[u'上海']],variable=[u'国内生产总值_人均'])
dset.noNA()
print(dset.data.T)
dset.data.T.plot()
plt.show()

dset.setSubset(year=range(2005,2014),region=[[u'北京'],[u'上海'],[u'浙江',u'杭州']],variable=[u'国内生产总值_人均'])
dset.noNA()
print(dset.data)
dset.data.T.plot()
plt.show()