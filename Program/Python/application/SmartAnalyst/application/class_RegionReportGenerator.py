# coding=UTF-8

#-----------------------------------------------------------------------------------------------------
# class_RegionReportGenerator文件
# @class: RegionReportGenerator类
# @introduction: RegionReportGenerator类用来生成区域数据分析报告
# @dependency: seaborn包，pandas包，numpy包，statsmodels包，matplotlib包，datetime包，RegionData类
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------------------------------

import re
import numpy as np
import pandas as pd
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
        self.raw_variables = config.get('variables')
        self.variables = list(set(self.raw_variables.keys()))
        self.assist_variables = set(self.raw_variables.values())
        self.assist_variables.discard(None)
        self.assist_variables = list(self.assist_variables)

        self.region = config.get('region')
        self.year = config.get('year')
        self.scale = config.get('scale')
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
            print(self.variables)
            self._data = self.region_data.find(region=self.region,year=self.year,variable=self.variables,scale=self.scale)
            self._assist_data = self.region_data.find(region=self.region,year=self.year,variable=self.assist_variables,scale=self.scale)
        elif self.region is not None:
            self._data = self.region_data.find(region=self.region,variable=self.variables,scale=self.scale)
            self._assist_data = self.region_data.find(region=self.region,variable=self.assist_variables,scale=self.scale)
        elif self.year is not None:
            self._data = self.region_data.find(year=self.year,variable=self.variables,scale=self.scale)
            self._assist_data = self.region_data.find(year=self.year,variable=self.assist_variables,scale=self.scale)
        else:
            self._data = self.region_data.find(variable=self.variables,scale=self.scale)
            self._assist_data = self.region_data.find(variable=self.assist_variables,scale=self.scale)

        self.data = self._data['pdata']
        self.year = list(self.data.items)
        # 格式转换
        for y in self.year:
            self.data[y][self.variables] = self.data[y][self.variables].astype(np.float64)
        self.assist_data = self._assist_data['pdata']

        # 生成报告
        self.report = Report(title=self.report_title,author=self.report_author)

    # 变量转换
    def variable_transformation(self):
        generator_data = dict()
        self.generator_variables = set()
        for year in list(self.data.items):
            assist_data_year = self.assist_data[year]
            del assist_data_year['region']
            total_data = pd.merge(self.data[year], assist_data_year, left_index=True, right_index=True, how='outer')

            csdexplorer = CrossSectionRegionDataExplorer(total_data)
            cross_section_frame = pd.DataFrame({'region':self.data[year]['region']})
            for var in self.data[year].columns[1:]:
                variable_name = var
                dframe = pd.DataFrame({variable_name:self.data[year][variable_name]})

                if self.raw_variables[var] is not None:
                    variable_name = '|'.join([var,self.raw_variables[var]])
                    dframe = csdexplorer.per_variable(pop=self.raw_variables[var],var=[var])

                if (np.min(dframe[variable_name]) > 0) and (np.max(dframe[variable_name]) < 1):
                    dframe = dframe.applymap(lambda x: 100 * x)
                    cross_section_frame = pd.merge(cross_section_frame, dframe, left_index=True, right_index=True, how='outer')
                    continue

                if (np.min(dframe[variable_name]) > 0) and (np.max(dframe[variable_name]) < 100):
                    cross_section_frame = pd.merge(cross_section_frame, dframe, left_index=True, right_index=True, how='outer')
                    continue

                if np.min(dframe[variable_name]) > 0:
                    dframe = dframe.applymap(np.log)
                    dframe.columns = ['|'.join([variable_name,u'对数'])]
                    #print(dframe.columns)
                    cross_section_frame = pd.merge(cross_section_frame, dframe, left_index=True, right_index=True, how='outer')

            generator_data[year] = cross_section_frame
            self.generator_variables.update(list(cross_section_frame.columns))
        self.generate_data = pd.Panel(generator_data)
        for y in self.year:
            self.generate_data[y][list(self.generate_data[y].columns)[1:]] = self.generate_data[y][list(self.generate_data[y].columns)[1:]].astype(np.float64)

        self.generator_variables = list(self.generator_variables)
        self.generator_variables.remove('region')

    # 分析的主接口
    def analysis(self):
        #self.describe()
        #self.describe(data_source='generated')
        self.corr()
        #self.corr(data_source='generated')

    # 相关性分析
    def corr(self,data_source='Raw',model='auto'):
        if re.match('^Raw$',data_source):
            variables = self.variables
            data = self.data
        else:
            variables = self.generator_variables
            data = self.generate_data

        for year in self.year:
            self.report.create_section(year)
            data_frame = data[year]
            cse = CrossSectionRegionDataExplorer(data_frame)
            corr = cse.corr()
            corr2 = corr.applymap(abs)
            corr_rank = corr2.rank(method='max',ascending=False)

            print(corr)
            print(corr.shape[0],len(variables))
            print(corr_rank)
            top_number = min(len(variables)+1,11)
            for var in variables:
                self.report.create_subsection(var)
                #print(corr[var])
                corr_data = {'variable':corr_rank.index,'rank':corr_rank[var],'corr':corr[var]}
                corr_data_frame = pd.DataFrame(corr_data,columns=['rank','variable','corr'])
                corr_data_frame = corr_data_frame.set_index('rank')
                corr_data_frame = corr_data_frame.sort_index()

                corr_data_frame = corr_data_frame.reindex(list(range(2,len(variables)+1)))

                corr_data_frame = corr_data_frame.set_index('variable')
                corr_data_frame = corr_data_frame.applymap(lambda x:'{0:.2f}'.format(x))
                corr_data_frame = corr_data_frame.iloc[:top_number]

                table_data = self.dataframe_to_list(corr_data_frame)
                self.report.add_table(table_data['data'],table_data['nrow'],table_data['ncol'])
                for xvar in corr_data_frame.index:
                    plt = cse.scatter(y=var,x=xvar,save=True)
                    self.report.add_matplotlib_graph(plt,caption='图形')
                    plt.close()

                print('-------------------------')
                print(corr_data_frame)
                print(self.dataframe_to_list(corr_data_frame))
                print('-------------------------')

    # 描述性统计
    def describe(self,data_source='Raw'):
        if re.match('^Raw$',data_source):
            variables = self.variables
            data = self.data
        else:
            variables = self.generator_variables
            data = self.generate_data

        for var in variables:
            # 生成章节
            self.report.create_section(var)

            for year in self.year:
                # 生成分支章节
                self.report.create_subsection(year)
                #data_frame = pd.DataFrame({var:data[year][var]})
                data_frame = data[year][['region',var]]

                cse = CrossSectionRegionDataExplorer(data_frame)
                #print(cse.describe().applymap(lambda x:'{0:.2f}'.format(x)))
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
    '''
    C_variables = {'第一产业占GDP的比重':None,'第二产业占GDP的比重':None, '第三产业占GDP的比重':None,
                   '地区生产总值':'年末总人口','自然增长率':None,'年末单位从业人数':None,
                   '年末总人口':None,'城镇私营和个体从业人员':'年末单位从业人数',
                   '第一产业从业人员比重':None,'第二产业从业人员比重':None,'第三产业从业人员比重':None,
                   '第二产业采矿业年末单位从业人员':'年末单位从业人数','第二产业制造业年末单位从业人员':'年末单位从业人数',
                   '第二产业电力燃气及水的生产和供应业年末单位从业人员':'年末单位从业人数',
                   '第二产业建筑业年末单位从业人员':'年末单位从业人数','行政区划土地面积':None,
                   '建成区面积':'行政区划土地面积','人口密度':'年末总人口','人均地区生产总值':None,
                   '地方财政一般预算内收入':'地区生产总值','地方财政一般预算内支出':'地区生产总值',
                   '规模以上工业总产值':'年末单位从业人数','规模以上内资企业工业总产值':'规模以上工业总产值',
                   '规模以上外商投资企业工业总产值':'规模以上工业总产值','职工平均工资':None}'''
    C_variables = {'第一产业占GDP的比重':None,'人口密度':'年末总人口','人均地区生产总值':None,
                   '职工平均工资':None}
    C_period = list(range(2005,2014))
    C_report_title = u'探索性区域分析报告(Version 1)'
    C_report_author = u'冥王星人'
    C_report_path = 'E:/Report/Region_Report_first_version.pdf'
    C_region = ['t']
    C_scale = u'全市'

    generator = RegionReportGenerator(variables=C_variables,year=C_period,report_title=C_report_title,
                                      report_author=C_report_author,report_path=C_report_path,region=C_region,scale=C_scale)
    generator.variable_transformation()
    print(generator.generate_data)
    for item in list(generator.generate_data.items):
        print(generator.generate_data[item])

    #print(pd.DataFrame({'region':generator._data['pdata']['2005']['region']}))
    #print(list(generator._data['pdata'].ix[1]))
    #print(generator._data['pdata'].major_axis)
    generator.analysis()
    print(generator.report)
    generator.generate_pdf()

