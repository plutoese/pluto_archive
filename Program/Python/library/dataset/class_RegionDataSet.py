# coding=UTF-8

from library.dataset.class_DataSet import *
from library.region.class_Layout import *
from library.dataanalysis.class_DataVisualization import *
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 类RegionDataSet是DataSet子类，专门处理区域数据集
class RegionDataSet(DataSet):
    '''
    类RegionDataSet是DataSet子类，专门处理区域数据集。
    
    属性：
    self.data：读入的数据，类型是pandas类型，即Series或者dataframe或者panel
    self.information：数据的基本信息
    self.ndim：数据的维度
    
    方法：
    __init__(self, data)：构造函数，用来进行初始化数据并进行格式转换。
    plot(self,**kargs)：通用作图函数

    Demo：
    ad = AdminCode()
    regiondata = RegionalData()
    layout = Layout(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出',u'国内生产总值_人均'],year=2012))
    data = layout.stackToNormal()
    information = layout.information
    data[u'财政支出'] = np.log(data[u'财政支出'])
    data[u'国内生产总值_人均'] = np.log(data[u'国内生产总值_人均'])
    rdata = RegionDataSet(data,information)
    rdata.plot(kind='scatter',x=u'国内生产总值_人均',y=u'财政支出',alpha=0.5)
    '''
    # 构造函数
    def __init__(self,data=None,information=None):
        DataSet.__init__(self,data)
        if information is not None:
            self.information = information
            self.ndim = len(information)

    # 通用作图函数
    def plot(self,**kargs):
        kargs['grid'] = True
        self._data.plot(**kargs)
        plt.show()

    # 时间序列图
    def tsline(self,var:str=None,region:str=None):
        if self.ndim == 2:
            self.plot()



if __name__ == '__main__':
    ad = AdminCode()
    regiondata = RegionalData()
    #rdata = RegionDataSet(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出',u'国内生产总值_人均'],year=2012))
    # 初始化数据和类型
    #layout = Layout(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出',u'国内生产总值_人均'],year=range(2010,2012)))
    #layout = Layout(regiondata.query(region=ad[u'浙江',u'杭州'],variable=[u'国内生产总值_人均']))
    layout = Layout(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'国内生产总值_人均']))
    data = layout.stackToNormal()
    information = layout.information
    #data[u'财政支出'] = np.log(data[u'财政支出'])
    #data[u'国内生产总值_人均'] = np.log(data[u'国内生产总值_人均'])
    #data.iloc([1,2]).applymap(np.log)
    rdata = RegionDataSet(data,information)
    print(data)
    print(rdata.information)
    print(rdata.ndim)
    rdata.tsline()
    #print(rdata.data)
    #print(list(rdata.data.axes[1])[1:])
    #print(rdata.information)

    #rdata.plot(kind='scatter',x=u'国内生产总值_人均',y=u'财政支出',alpha=0.5)

