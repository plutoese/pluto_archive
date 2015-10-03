# coding=UTF-8

from application.DBConstructor.CityStatistics.class_CityStatisticsDataSheet import *
from library.imexport.class_FileSystem import *
from library.imexport.class_Excel import *

# 设置参数
YEAR = 2002
DATADIR = r'C:\Data\city\data'
VARFILE = r'C:\Data\city\var\m2002.xlsx'

ad = AdministrativeCode(year=YEAR)

# 连接MongoDB数据库
client = MongoClient('localhost', 27017)
db = client['regionDB']
collection = db['CityStatistics']

# 1. 列出DATA目录下所有的文件
mos = FileSystem(DATADIR)
files = mos.listabsdir()

n = 0
wrong = []
wrongnumber = []
regions = []
# 2. 循环开始
for file in files:
    mdatasheet = CityStatisticsDataSheet(filename=file,year=YEAR)

    variables = Excel(VARFILE).read(sheetnum=0)
    var = variables[n][1:]
    mdatasheet.setVariables(var)
    n = n + 1

    result = mdatasheet.todataTable()
    print(result)
    wrong.append(mdatasheet.wrongdata)
    regions.append(mdatasheet.region)
    wrongnumber.extend(mdatasheet.wrongnumber)

    for item in result:
        collection.insert(item)

outfile = u'c:\\down\\wrong1.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(wrong)
moutexcel.close()

outfile = u'c:\\down\\wrong2.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(regions)
moutexcel.close()

print(wrongnumber)
outfile = u'c:\\down\\wrong3.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(wrongnumber)
moutexcel.close()