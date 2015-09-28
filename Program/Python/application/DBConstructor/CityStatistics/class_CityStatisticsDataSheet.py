# coding=UTF-8

from library.datapretreatment.class_DataSheet import *
from library.region.class_AdministrativeCode import *

# 类CityStatisticsDataSheet用来处理中国城市统计年鉴的数据
class CityStatisticsDataSheet(DataSheet):
    '''
    类CityStatisticsDataSheet用来处理中国城市统计年鉴的数据
    
    属性：
    self.rawdata: 原始数据
    '''
    # 构造函数
    def __init__(self, filename=None,sheetnum=0,year=None):
        DataSheet.__init__(self,filename=filename,sheetnum=sheetnum)
        self._data = pd.DataFrame(self.rawdata)
        self.year = year

        # 设置ad选项
        self.ad = AdministrativeCode(year=year)

    # 析出数据表格
    def todataTable(self):
        mdata = self.data
        result = []
        prefix = []
        for i in mdata.index:
            if len(re.sub('\s+','',mdata.iloc[i][0])) < 1:
                continue
            if len(prefix) < 1:
                region = ad[re.sub('\s+','',mdata.iloc[i][0])]
                if region is None:
                    print('Wrong:',mdata.iloc[i][0])
                else:
                    tmpresult = [region['acode'],region['region']]
                    tmpresult.extend(list(mdata.iloc[i][2:]))
                    result.append(tmpresult)
                    prefix.append(region['region'])
            elif len(prefix) < 2:
                region = ad[re.sub('\s+','',mdata.iloc[i][0])]
                if region is None:
                    region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                    if region is None:
                        print('Wrong:',mdata.iloc[i][0])
                    else:
                        tmpresult = [region['acode'],region['region']]
                        tmpresult.extend(list(mdata.iloc[i][2:]))
                        result.append(tmpresult)
                        prefix.append(region['region'])
                else:
                    if re.match(ad[prefix[len(prefix)-1]]['acode'],region['acode']) is not None:
                        region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                        if region is None:
                            print('Wrong:',mdata.iloc[i][0])
                        else:
                            tmpresult = [region['acode'],region['region']]
                            tmpresult.extend(list(mdata.iloc[i][2:]))
                            result.append(tmpresult)
                            prefix.append(region['region'])
                    else:
                        prefix = [region['region']]
            else:
                region = ad[re.sub('\s+','',mdata.iloc[i][0])]
                if region is None:
                    region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                    if region is None:
                        region = ad[prefix[0],prefix[1],re.sub('\s+','',mdata.iloc[i][0])]
                        if region is None:
                            print('Wrong:',mdata.iloc[i][0])
                        else:
                            tmpresult = [region['acode'],region['region']]
                            tmpresult.extend(list(mdata.iloc[i][2:]))
                            result.append(tmpresult)
                    else:
                        tmpresult = [region['acode'],region['region']]
                        tmpresult.extend(list(mdata.iloc[i][2:]))
                        result.append(tmpresult)
                        prefix[1] = region['region']
                else:
                    tmpresult = [region['acode'],region['region']]
                    tmpresult.extend(list(mdata.iloc[i][2:]))
                    result.append(tmpresult)
                    prefix = [region['region']]
        return pd.DataFrame(result)

if __name__ == '__main__':
    ad = AdministrativeCode(year=2012)
    mdatasheet = CityStatisticsDataSheet(r'C:\Data\city\data\m01.xlsx',year=2012)
    print(list(mdatasheet.data.iloc[5][3:]))
    result = mdatasheet.todataTable()
    print(result.to_dict('records'))
    '''
    mindex = []
    prefix = []
    for i in mdata.index:
        if len(re.sub('\s+','',mdata.iloc[i][0])) < 1:
            continue
        if len(prefix) < 1:
            region = ad[re.sub('\s+','',mdata.iloc[i][0])]
            if region is None:
                print('Wrong:',mdata.iloc[i][0])
            else:
                mindex.append(i)
                prefix.append(region['region'])
        elif len(prefix) < 2:
            region = ad[re.sub('\s+','',mdata.iloc[i][0])]
            if region is None:
                region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                if region is None:
                    print('Wrong:',mdata.iloc[i][0])
                else:
                    mindex.append(i)
                    prefix.append(region['region'])
            else:
                if re.match(ad[prefix[len(prefix)-1]]['acode'],region['acode']) is not None:
                    region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                    if region is None:
                        print('Wrong:',mdata.iloc[i][0])
                    else:
                        mindex.append(i)
                        prefix.append(region['region'])
                else:
                    prefix = [region['region']]
        else:
            region =  region = ad[re.sub('\s+','',mdata.iloc[i][0])]
            if region is None:
                region = ad[prefix[0],re.sub('\s+','',mdata.iloc[i][0])]
                if region is None:
                    region = ad[prefix[0],prefix[1],re.sub('\s+','',mdata.iloc[i][0])]
                    if region is None:
                        print('Wrong:',mdata.iloc[i][0])
                    else:
                        mindex.append(i)
                else:
                    mindex.append(i)
                    prefix[1] = region['region']
            else:
                mindex.append(i)
                prefix = [region['region']]

file = 'c:/down/mresult.xlsx'
mdata.iloc[mindex].to_excel(file)
#print(mdata.iloc[mindex])'''




