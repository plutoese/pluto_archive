# coding=UTF-8

from library.imexport.class_Excel import *
from library.imexport.class_MongoDB import *
from library.region.class_AdminCode import *

# 类RegionData用来从数据库MongoDB中导出区域数据
class RegionData:
    # Construction
    def __init__(self):
        # to connect to Mongodb database
        self.db = MongoDB()
        # Admin district
        self.AD = AdminDistrict()
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
    ad = AdminDistrict()
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
