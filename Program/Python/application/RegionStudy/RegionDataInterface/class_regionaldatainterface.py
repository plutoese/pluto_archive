# coding=UTF-8

from library.datalayout.class_Format import *

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
    def __init__(self,collection:str='CityStatistics'):
        # RegionalData的一个对象
        self.regionData = RegionData(collection)

    # 查询返回结果
    def query(self,query:dict=None):
        # 查询数据返回结果
        result = self.regionData.query(**query)
        # 重新转换格式
        if result.size < 1:
            return None
        rdata = Foramt(result)
        mdata = rdata.transform()
        return mdata

    # 返回该数据集合的变量
    @property
    def variable(self):
        return self.regionData.variables()

if __name__ == '__main__':
    dinterface = RegionDataInterface()
    print(dinterface.variable)
    projection = {'region':1,'year':1,'value':1,'acode':1,'_id':0,'variable':1,'scale':1}
    querydict = {'region':[[u'浙江',u'f']],'variable':[u'人均地区生产总值',u'职工平均工资'],'year':[2009,2010],'projection':projection}
    #querydict = {'region':ad[u'浙江',u'f'],'variable':[u'人均地区生产总值'],'scale':'全市','year':[2012]}
    #querydict = {'region':ad[u'浙江',u'f'],'variable':[u'财政支出'],'year':[2012]}
    result = dinterface.query(querydict)
    print(result)
    mdata = result['data']
    mdata2 = result['balanceddata']
    print(mdata)
    print(mdata2)
    #file = 'c:/down/mresult.xls'
    #mdata.to_excel(file)