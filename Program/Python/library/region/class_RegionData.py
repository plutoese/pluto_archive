# coding=UTF-8

from library.imexport.class_Excel import *
from library.imexport.class_MongoDB import *
from library.region.class_AdminCode import *

# 类RegionData用来从数据库MongoDB中导出区域数据
class RegionData:
    '''
    类RegionData用来从数据库MongoDB中导出区域数据。
    
    属性：
    layout：特定的输出格式，是Layout类的一个实例
    data: 读入的数据
    
    方法：
    toSetCollection(self,collection="CEIC")：设定集合，参数collection表示集合名称，类型字符串，默认是'CEIC'。无返回值。
    query_one(self,variable,year,region)：单个查询，用于查询单个结果。
    query(self,variable=None,period=None,region=None)：查询，并返回标准格式的数据表。参数variable表示变量名，类型字符串或者列表，默认值None，表示所有变量；
    参数period表示时间段，类型整数（int）或列表（range，list），默认值None，表示所有时间段；参数region表示区域，类型AdminCode实例或者其列表，默认值None，表示所有区域。
    返回值为标准格式的数据表，类型列表。

    read(self, sheetnum=0): 读取Excel表的数据，参数sheetnum表示Excel文件表单号，类型整数，默认为0。返回值为Excel表中所有数据，类型列表。
    new(self): 新建一个Excel文件，文件名为self.filename。无返回值。
    def append(self, data=None): 把数据写入Excel文件，参数data表示要写入Excel文件的数据，类型列表，默认值None表示用self.data。无返回值。
    close(self): 关闭Excel文件，无参数。无返回值。
    '''
    # Construction
    def __init__(self):
        # to connect to Mongodb database
        self.db = MongoDB()
        # Admin district
        self.AD = AdminCode()
        # Layout
        self.layout = Layout()

    def toSetCollection(self,collection="CEIC"):
        self.Collection = self.db.connect('regionDB',collection)

    # to get one query
    def query_one(self,variable,year,region):
        mregion = self.AD[region]
        acode = mregion['acode']
        result = self.Collection.find_one({'acode':acode,'year':year,'variable':variable})
        return result

    # to query
    def query(self,variable=None,period=None,region=None):
        if region is None:
            region = self.regions
        if variable is None:
            variable = self.variables
        if isinstance(variable,str):
            variable = [variable]
        if isinstance(period,int):
            period = [period]

        result = self.layout.toRegionLayout(region,period,variable)
        for i in range(1,len(result)):
            for j in range(3,len(result[0])):
                qresult = self.Collection.find({'acode':result[i][0],'year':result[i][2],'variable':result[0][j]})
                qresult = list(qresult)
                if len(qresult) > 0:
                    if len(qresult) < 2:
                        result[i][j] = qresult[0]['value']
                    else:
                        print('Something Wroing...')
                        print(qresult)
                        result[i][j] = qresult[0]['value']
        return result

    # to find out variable in database
    @property
    def variables(self):
        result = self.Collection.distinct('variable')
        return result

    @property
    def regions(self):
        acodes = self.Collection.distinct('acode')
        result = [self.AD.getByAcode(acode) for acode in sorted(acodes)]
        return result   

# 类Layout用来生成各种输出格式
class Layout:
    # Construction
    def __init__(self):
        pass

    def toRegionLayout(self,region,period,variable,downtown=None):
        N = len(region)
        T = len(period)
        K = len(variable)
        result = [['']*(K+3) for i in range(N*T+1)]

        result[0][0] = 'acode'
        result[0][1] = 'region'
        result[0][2] = 'year'
        for i in range(len(variable)):
            result[0][i+3] = variable[i]
        j = 1
        for y in period:
            for r in region:
                result[j][0] = r['acode']
                result[j][1] = r['region']
                result[j][2] = y
                j = j + 1
        return result


if __name__ == '__main__':
    mceic = RegionData()
    mceic.toSetCollection()
    ad = AdminCode()
    #result = mceic.query(variable=[u'财政支出',u'财政收入',u'国内生产总值',u'从业人数_制造业'],period=list(range(1996,2000)),region=[ad[u'北京'],ad[u'上海']])
    result = mceic.query(period=list(range(2000,2014)))
    print(result)

    print(mceic.variables)
    print(mceic.regions)

    outfile = u'c:\\down\\demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new()
    moutexcel.append(result)
    moutexcel.close()
