# coding=UTF-8

from library.datastruct.class_SeriesData import *
from library.datalayout.class_Layout import *

# 类RegionDataInterface提供了区域数据的接口
class RegionDataInterface:
    '''
    类RegionDataInterface是区域数据的接口。
    
    属性：
    self.regionData：类RegionalData的一个实例
    self.variable：该数据库集合内所有的变量
    
    方法：
    __init__(self,collection:str='CEIC')：构造函数，用来进行初始化区域数据接口，参数collection用来指定集合名称，默认是CEIC。
    query(self,query:dict=None)：查询接口
    '''
    # 构造函数
    def __init__(self,collection:str='CEIC'):
        # RegionalData的一个对象
        self.regionData = RegionalData(collection)

    # 查询返回结果
    def query(self,query:dict=None):
        # 查询数据返回结果
        result = self.regionData.query(**query)
        # 重新转换格式
        if result.size < 1:
            return None
        layout = Layout(result)
        data = layout.stackToNormal()
        # 记录数据集的信息
        tags = layout.tags
        qresult = {'data':data,'tags':tags}
        return qresult

    # 返回该数据集合的变量
    @property
    def variable(self):
        return self.regionData.variables()

if __name__ == '__main__':
    dinterface = RegionDataInterface(collection='cCity')
    #dinterface = RegionDataInterface()
    print(dinterface.variable)
    ad = AdminCode()
    querydict = {'variable':[u'年末总人口'],'scale':'全市','year':2001}
    #querydict = {'region':ad[u'浙江',u'f'],'variable':[u'人均地区生产总值'],'scale':'全市','year':[2012]}
    #querydict = {'region':ad[u'浙江',u'f'],'variable':[u'财政支出'],'year':[2012]}
    result = dinterface.query(querydict)
    print(result['data'])