# coding=UTF-8

from library.dataset.class_DataSet import *
from library.region.class_Layout import *
from library.dataanalysis.class_DataVisualization import *

# 类RegionDataSet是子类
class RegionDataSet(DataSet):
    # 构造函数
    def __init__(self, data):
        DataSet.__init__(self, data)
        # 初始化数据和类型
        self.layout = Layout(data)
        self.data = self.layout.stackToNormal()
        self.information = self.layout.information
        self.style = len(self.information)

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