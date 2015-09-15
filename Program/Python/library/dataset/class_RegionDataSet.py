# coding=UTF-8

from library.dataset.class_DataSet import *
from library.region.class_Layout import *
from library.dataanalysis.class_DataVisualization import *

# 类RegionDataSet是DataSet子类，专门处理区域数据集
class RegionDataSet(DataSet):
    '''
    类RegionDataSet是DataSet子类，专门处理区域数据集。
    
    属性：
    self.data：normal格式的数据，类型是pandas类型，即Series或者dataframe或者panel
    self.information：数据的基本信息
    self.ndim：数据的维度
    
    方法：
    __init__(self, data)：构造函数，用来进行初始化数据并进行格式转换。

    Demo：
    构建区域数据集
    ad = AdminCode()
    regiondata = RegionalData()
    rdata = RegionDataSet(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出'],year=2012))
    '''
    # 构造函数
    def __init__(self, data):
        DataSet.__init__(self, data)
        # 初始化数据和类型
        self.layout = Layout(data)
        self.data = self.layout.stackToNormal()
        self.information = self.layout.information
        self.ndim = len(self.information)

        # 建立数据可视化的类接口
        self.datavisualization = DataVisualization(self.data)

    # 通用作图函数
    def plot(self,**args):
        #args['x'] = self.data['region']
        args['grid'] =True
        print('args',args)
        self.datavisualization.plot(kind='barh')

if __name__ == '__main__':
    ad = AdminCode()
    regiondata = RegionalData()
    rdata = RegionDataSet(regiondata.query(region=ad[u'浙江',u'f'],variable=[u'财政支出'],year=2012))
    print(rdata.data)
    print(list(rdata.data.axes[1])[1:])
    print(rdata.information)

    rdata.plot(kind='barh')