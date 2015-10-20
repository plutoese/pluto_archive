# coding=UTF-8

#-----------------------------------------------------------------------------------------------------
# class_RegionReportGenerator文件
# @class: RegionReportGenerator类
# @introduction: RegionReportGenerator类用来生成区域数据分析报告
# @dependency: seaborn包，pandas包，numpy包，statsmodels包，matplotlib包，datetime包，RegionData类
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------------------------------

from lib.report.class_Report import Report
from lib.data.class_RegionData import RegionData
from lib.toolkit.class_CrossSectionDataExplorer import CrossSectionRegionDataExplorer

class RegionReportGenerator():
    '''类RegionReportGenerator是区域分析报告生成器

    :param dict config: 参数配置
    '''
    # 构造函数
    def __init__(self,**config):
        # 设置参数，必要参数
        self.variables = config.get('variables')
        self.region = config.get('region')
        self.year = config.get('year')
        self.report_title = config.get('report_title')
        self.report_path = config.get('report_path')

        # 设置参数，非必要参数
        if 'report_author' in config.keys():
            self.report_author = config.get('report_author')
        else:
            self.report_author = 'Plutoese'

        # 区域数据
        self.region_data = RegionData()
        # 查询数据
        if (self.region is not None) and (self.year is not None):
            self._data = self.region_data.find(region=self.region,year=self.year,variable=list(self.variables.keys()))
        elif self.region is not None:
            self._data = self.region_data.find(region=self.region,variable=list(self.variables.keys()))
        elif self.year is not None:
            self._data = self.region_data.find(year=self.year,variable=list(self.variables.keys()))
        else:
            self._data = self.region_data.find(variable=list(self.variables.keys()))
        generator_data = {}
        for year in list(self._data['pdata'].items):
            pass

        # 生成报告
        self.report = Report(title=self.report_title,author=self.report_author)

    # 描述性统计
    def describe(self):
        vars = list(self.variables)
        for i in range(len(vars)):
            var = vars.pop(0)

            # 生成章节
            self.report.create_section(var)

            if self.year is None:
                period = self.region_data.databases['citystatiscs'].period(var)
            else:
                period = self.year

            for year in period:
                # 生成分支章节
                self.report.create_subsection(year)
                mdata = self.region_data.find(region=self.region,year=[year],variable=[var])
                mdata = mdata['data']

                cse = CrossSectionRegionDataExplorer(mdata)
                tdata = cse.describe().applymap(lambda x:'{0:.2f}'.format(x))
                tdata = self.dataframe_to_list(tdata)
                print(var,year)
                self.report.add_table(tdata['data'],tdata['nrow'],tdata['ncol'])

    # 生成pdf报告
    def generate_pdf(self):
        self.report.flush()
        self.report.generate_pdf(self.report_path)

    # 把data.frame转化为list
    def dataframe_to_list(self,dframe):
        dict_data = dframe.to_dict('split')
        result = dict_data['data']
        [result[i].insert(0,dict_data['index'][i]) for i in range(len(result))]

        title = [u'变量']
        title.extend(dict_data['columns'])
        result.insert(0,title)

        nrow = len(result)
        ncol = len(result[0])

        return {'data':result,'ncol':ncol,'nrow':nrow}


if __name__ == '__main__':
    C_variables = {'第一产业占GDP的比重':None,'第二产业占GDP的比重':None, '第三产业占GDP的比重':None}
    C_period = list(range(2005,2014))
    C_report_title = u'探索性区域分析报告(Version 1)'
    C_report_author = u'冥王星人'
    C_report_path = 'E:/Report/Region_Report_first_version.pdf'
    C_region = ['t']

    generator = RegionReportGenerator(variables=C_variables,year=C_period,report_title=C_report_title,
                                      report_author=C_report_author,report_path=C_report_path,region=C_region)
    print(generator._data['pdata']['2005']['region'])
    print(list(generator._data['pdata'].ix[1]))
    print(generator._data['pdata'].major_axis)
    #generator.describe()
    #generator.generate_pdf()

