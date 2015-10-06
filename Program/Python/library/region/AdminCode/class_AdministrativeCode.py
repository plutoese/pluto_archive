# coding=UTF-8
#-------------------------------------------
# AdministrativeCode类是用来进行获取区域信息
#-------------------------------------------

from library.imexport.class_MongoDB import *
import pandas as pd


# 类AdministrativeCode用来获取区域代码
class AdministrativeCode:
    '''
    类AdministrativeCode用来提取区域代码及其他信息。
    
    属性：
    Province: 所有省级行政区域
    Prefecture: 所有地级行政区域
    County：所有县级行政区域
    ProvincePrefecture：所有的省级和地级行政区域
    ProvincePrefectureCounty：所有的省级地级县级区域

    方法：
    __getitem__(self, key)：重载运算符[]。其中的key表示表示区域名称，方法如下：（1）省级区域，用名字直接表示，例如ad[u'北京']；
    （2）地级区域，用省级、地级名称表示，例如ad[u'浙江',u'嘉兴']；（3）县级区域，用省级、地级、县级名称表示，例如ad[u'湖北', u'恩施',u'来凤']；
    （4）如果是本级行政区域加上下级行政区域，下级行政区域用f（first）表示，例如表示浙江省及其所有地级行政区域，用ad[u'浙江',u'f']；
    （5）如果是本级行政区域加上下下级行政区域，下下级行政区域用s（second）表示，例如表示浙江省及其所有县级行政区域，用ad[u'浙江',u's']；
    （6）如果是本级行政区域加上下级及下下级行政区域，下级及下下级行政区域用b（both）表示，例如表示浙江省及其所有地县级行政区域，用ad[u'浙江',u'b']。
    返回值是数据库中查询得到的行政区划的字典（单个）或者列表（多个）。

    getByAcode(self,acode)：通过acode查询区域信息，参数acode表示区域行政代码，类型字符串。返回值为数据库中查询得到的行政区域，类型字典。
    '''
    # Construction
    def __init__(self,version=None,year=None):
        # 连接数据库
        self.Client = MongoClient('localhost', 27017)
        self.DB = self.Client['regionDB']
        self.Collection = self.DB['AdminCode']

        # 设置最新的版本
        self.latestversion = self.versions[len(self.versions)-1]

        # 设置版本和年份
        if (version is None) and (year is None):
            self.version = self.latestversion
            self.year = re.split('_',self.version)[0]
        elif version is not None:
            self.version = version
            self.year = re.split('_',self.version)[0]
        else:
            self.year = str(year)
            self.version = self.yearToVersion(self.year)

        self.Province = self._sorted(list(self.Collection.find({'adminlevel':2,'version':self.version})))
        self.Prefecture = self._sorted(list(self.Collection.find({'adminlevel':3,'version':self.version})))
        self.County = self._sorted(list(self.Collection.find({'adminlevel':4,'version':self.version})))

    # to get item
    # f to get all first level
    # s to get all second level
    # b to get all first and second level
    def __getitem__(self, key):
        if isinstance(key,str):
            if re.match('^s$',key):
                return self.Province
            if re.match('^t$',key):
                return self.Prefecture
            if re.match('^f$',key):
                return self.County
            return self._getProvince(key)
        if isinstance(key,tuple) and len(key) < 2:
            if re.match('^s$',key[0]):
                return self.Province
            if re.match('^t$',key[0]):
                return self.Prefecture
            if re.match('^f$',key[0]):
                return self.County
            return self._getProvince(key[0])
        if isinstance(key,tuple):
            if len(key) < 3:
                if re.match(key[1],u'f') is not None:
                    result = self._getPrefectureChildren(key[0])
                    return self._sorted(result)
                elif re.match(key[1],u's') is not None:
                    prefectures = self._getPrefectureChildren(key[0])
                    result = []
                    for item in prefectures:
                        result.extend(self._getCountyChildren(key[0],item['region']))
                    return self._sorted(result)
                elif re.match(key[1],u'b') is not None:
                    prefectures = self._getPrefectureChildren(key[0])
                    result = []
                    for item in prefectures:
                        result.append(item)
                        result.extend(self._getCountyChildren(key[0],item['region']))
                    return self._sorted(result)
                else:
                    result = self._getPrefecture(key[0],key[1])
                    return result
            else:
                if re.match(key[2],u'f') is not None:
                    result = self._getCountyChildren(key[0],key[1])
                    return self._sorted(result)
                else:
                    result = self._getCounty(key[0],key[1],key[2])
                    return result

    # 获得一个省级单位
    def _getProvince(self,province):
        _provincepattern = u'省|市|自治区|维吾尔自治区|回族自治区|壮族自治区'
        province = re.sub('\s+','',province)
        province = re.split(_provincepattern,province)[0]
        mprovince = '^' + province +'$'
        result = [item for item in self.Province if re.match(mprovince,re.split(_provincepattern,item['region'])[0]) is not None]
        if len(result) < 1:
            return None
        else:
            return  result

    # 获得一个地级单位
    def _getPrefecture(self,province,prefecture):
        prefectures =  self._getPrefectureChildren(province)
        result = [item for item in prefectures if re.match(prefecture,item['region']) is not None]
        if len(result) < 1:
            return None
        else:
            return result

    # 获得一个县级单位
    def _getCounty(self,province,prefecture,county):
        counties =  self._getCountyChildren(province,prefecture)
        result = [item for item in counties if re.match(county,item['region']) is not None]
        if len(result) < 1:
            return None
        #result = [item for item in counties if re.match(county,item['region']) is not None][0]
        return result

    # 获得一个省级单位所有的地级单位
    def _getPrefectureChildren(self,province):
        # to find province item
        provinces = [item for item in self.Province if re.match(province,item['region']) is not None]
        if len(provinces) > 1:
            return None
        prefecture = self.Collection.find({'parent':provinces[0]['_id'],'version':self.version})
        return list(prefecture)

    # 获得一个地级单位所有的县级单位
    def _getCountyChildren(self,province,prefecture):
        # to find province item
        prefectures = self._getPrefectureChildren(province)
        theprefecture = [item for item in prefectures if re.match(prefecture,item['region']) is not None]
        if len(theprefecture) > 1:
            return None
        county = self.Collection.find({'parent':theprefecture[0]['_id'],'version':self.version})
        return list(county)

    # 通过Acode获得区域
    def getByAcode(self,acode):
        result = self.Collection.find_one({'acode':acode,'version':self.version})
        return result

    def getByAcodeAndYear(self,acode,year):
        version = self.yearToVersion(year)
        result = self.Collection.find_one({'acode':acode,'version':version})
        return result

    # 通过ID获得区域
    def getByID(self,id):
        result = self.Collection.find_one({'_id':id,'version':self.version})
        return result

    # 获得省级和地级单位
    @property
    def ProvincePrefecture(self):
        result = []
        provinces = self.Province
        for province in provinces:
            result.append(province)
            result.extend(self._getPrefectureChildren(province['region']))
        return result

    # 获得省级、地级和县级单位
    @property
    def ProvincePrefectureCounty(self):
        result = []
        provinces = self.Province
        for province in provinces:
            result.append(province)
            prefectures = self._getPrefectureChildren(province['region'])
            for prefecture in prefectures:
                result.append(prefecture)
                result.extend(self._getCountyChildren(province['region'],prefecture['region']))
        return result

    # 设置版本
    def setVersion(self,version):
        self.version = version
        self.year = re.split('_',self.version)[0]

        self.Province = self._sorted(list(self.Collection.find({'adminlevel':2,'version':self.version})))
        self.Prefecture = self._sorted(list(self.Collection.find({'adminlevel':3,'version':self.version})))
        self.County = self._sorted(list(self.Collection.find({'adminlevel':4,'version':self.version})))

    # 设置年份
    def setYear(self,year):
        self.year = str(year)
        self.version = self.yearToVersion(self.year)

        self.Province = self._sorted(list(self.Collection.find({'adminlevel':2,'version':self.version})))
        self.Prefecture = self._sorted(list(self.Collection.find({'adminlevel':3,'version':self.version})))
        self.County = self._sorted(list(self.Collection.find({'adminlevel':4,'version':self.version})))

    # 把year转化为version
    def yearToVersion(self,year=None,latest=True):
        result = sorted([v for v in self.versions if re.search(str(year),v) is not None])
        return result[len(result)-1]

    # 根据Acode对地区进行排序
    def _sorted(self,regions):
        return sorted(regions,key = lambda x:x['acode'])

    # 显示所有的版本号
    @property
    def versions(self):
        return sorted(self.Collection.find().distinct('version'))

    # 显示所有年份
    @property
    def years(self):
        return sorted(self.Collection.find().distinct('year'))

    # 显示当前版本的所有区域
    @property
    def regions(self):
        projection ={'region':1,'acode':1,'_id':0}
        sorts = [('acode',ASCENDING)]
        region = pd.DataFrame(list(self.Collection.find({'version':self.version},projection=projection).sort(sorts)))
        region = region.set_index('acode')
        region.columns = [self.year]
        return region

if __name__ == '__main__':
    ad = AdministrativeCode(year=2003)
    print(ad.versions)
    print(ad.Province)
    print(ad._getPrefectureChildren(u'云南'))
    print(ad._getCountyChildren(u'江苏',u'南京'))
    print(ad._getProvince(u'黑龙江'))
    print(ad._getProvince(u''))
    print(ad._getPrefecture(u'浙江',u'宁波'))
    print(ad._getCounty(u'浙江',u'嘉兴',u'海宁'))
    print(ad[u'浙江'])
    print(ad[u'吉林'])
    print(ad[u'浙江',u'f'])
    print(ad[u'浙江',u's'])
    print(ad[u'浙江',u'b'])
    print(ad[u'吉林','吉林'])
    print(ad[u'浙江',u'嘉兴'])
    print(ad[u'浙江',u'嘉兴',u'f'])
    print(ad[u'浙江',u'嘉兴',u'海宁'])
    print(ad[u'山东省',u'荷泽市'])
    print(ad[tuple([u'浙江',u'f'])])
    ad.setYear(2010)
    print(ad[tuple([u'浙江',u'f'])])
    print(ad[tuple([u'北京'])])
