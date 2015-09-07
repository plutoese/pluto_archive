# coding=UTF-8

import re
from pymongo import MongoClient

# 类AdminCode用来获取区域代码
class AdminCode:
    '''
    类AdminCode用来提取区域代码及其他信息。
    
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
    def __init__(self,index=None):
        self.Client = MongoClient('localhost', 27017)
        self.DB = self.Client['regionDB']
        if index is None:
            self.Collection = self.DB['cAdministrationLevel']
        else:
            dbname = 'cAdministrationLevel' + index
            self.Collection = self.DB[dbname]
        self.Province = self._sorted(list(self.Collection.find({'adminlevel':2})))
        self.Prefecture = self._sorted(list(self.Collection.find({'adminlevel':3})))
        self.County = self._sorted(list(self.Collection.find({'adminlevel':4})))

    # to get item
    # f to get all first level
    # s to get all second level
    # b to get all first and second level
    def __getitem__(self, key):
        if isinstance(key,str):
            return self._getProvince(key)
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

    # to sort regions
    def _sorted(self,regions):
        return sorted(regions,key = lambda x:x['acode'])

    # to get a Province
    def _getProvince(self,province):
        _provincepattern = u'省|市|自治区|维吾尔自治区|回族自治区|壮族自治区'
        province = re.sub('\s+','',province)
        province = re.split(_provincepattern,province)[0]
        mprovince = '^' + province +'$'
        result = [item for item in self.Province if re.match(mprovince,re.split(_provincepattern,item['region'])[0]) is not None]
        if len(result) < 1:
            return None
        else:
            return  result[0]

    # to get a Prefecture
    def _getPrefecture(self,province,prefecture):
        prefectures =  self._getPrefectureChildren(province)
        result = [item for item in prefectures if re.match(prefecture,item['region']) is not None]
        if len(result) < 1:
            return None
        else:
            result = result[0]
        return result

    # to get a County
    def _getCounty(self,province,prefecture,county):
        counties =  self._getCountyChildren(province,prefecture)
        result = [item for item in counties if re.match(county,item['region']) is not None][0]
        return result

    # to get Prefecture of a Province
    def _getPrefectureChildren(self,province):
        # to find province item
        provinces = [item for item in self.Province if re.match(province,item['region']) is not None]
        if len(provinces) > 1:
            return None
        prefecture = self.Collection.find({'parent':provinces[0]['_id']})
        return list(prefecture)

    # to get County of a Province and Prefecture
    def _getCountyChildren(self,province,prefecture):
        # to find province item
        prefectures = self._getPrefectureChildren(province)
        theprefecture = [item for item in prefectures if re.match(prefecture,item['region']) is not None]
        if len(theprefecture) > 1:
            return None
        county = self.Collection.find({'parent':theprefecture[0]['_id']})
        return list(county)

    # to get by acode
    def getByAcode(self,acode):
        result = self.Collection.find_one({'acode':acode})
        return result

    # to get by id
    def getByID(self,id):
        result = self.Collection.find_one({'_id':id})
        return result

    @property
    def ProvincePrefecture(self):
        result = []
        provinces = self.Province
        for province in provinces:
            result.append(province)
            result.extend(self._getPrefectureChildren(province['region']))
        return result

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

if __name__ == '__main__':
    ad = AdminDistrict()
    print(ad.Province)
    print(ad._getPrefectureChildren(u'云南'))
    print(ad._getCountyChildren(u'江苏',u'南京'))
    print(ad._getProvince(u'黑龙江'))
    print(ad._getProvince(u''))
    #print(ad._getProvince(u'2-34 交通运输(全市)(二)'))
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
    print(ad[u'安徽',u'巢湖'])

    adold = AdminCode(index=u'09')
    print(adold.Province)
    print(adold[u'吉林'])
    print(adold[[u'吉林']])
    print(adold[u'浙江',u'f'])
    print(adold[u'山东',u'济宁',u'市中'])
    print(adold[u'北京',u'市辖区',u'崇文区'])

    #print(ad.ProvincePrefecture)
    #print(ad.ProvincePrefectureCounty)
    #print(ad.Prefecture)

    print(ad[u'河南', u'漯河',u'临颍'])
    print(ad[u'湖北', u'恩施',u'来凤'])

    region = [u'北京']
    print(ad[region[0]])