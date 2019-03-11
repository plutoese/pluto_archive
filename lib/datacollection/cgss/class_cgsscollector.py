# coding=UTF-8

"""
=========================================
CGSSCollector类
=========================================

:Author: glen
:Date: 2018.06.2
:Tags: cgss data_collection
:abstract:

**类**
==================
CgssStataSheet
    读取stata文件

**使用方法**
==================
"""

from lib.base.imexport.class_Stata import Stata
from lib.base.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from pathlib import Path
import re
import pandas as pd
import time


class CgssStataSheet:
    def __init__(self, file_path, label_path):
        """ 读取stata的数据文件，整理并导入到数据库

        :param file_path: .dta数据文件路径
        """
        path_obj = Path(file_path)

        # stata的数据文件
        if path_obj.is_file():
            self._file_list = [file_path]
        else:
            self._file_list = [file for file in path_obj.iterdir()]

        label_path_obj = Path(label_path)

        # 生成的变量和值标签关联的数据文件列表
        if label_path_obj.is_file():
            self._label_file_list = [label_path]
        else:
            self._label_file_list = [file for file in label_path_obj.iterdir()]

        self._stata_object = dict()
        self._stata_label_object = dict()

    def read_data(self, year_fun = lambda filename: re.search("\d{4}", filename).group()):
        """ 读取stata数据文件，存入stata对象到self._stata_object

        :param year_fun: 获取文件名中年份的函数
        :return: 返回self
        """
        for stata_file_path in self._file_list:
            year = year_fun(Path(stata_file_path).name)
            stata_obj = Stata(stata_file_path, convert_dates=False, convert_categoricals=False)
            self._stata_object[year] = stata_obj

        return self

    def read_variable_label(self, year_fun = lambda filename: re.search("\d{4}", filename).group()):
        """ 读取stata中变量和值标签关联的stata数据文件，存入信息到self._stata_label_object

        :param year_fun: 取文件名中年份的函数
        :return: 返回self
        """
        for stata_label_file in self._label_file_list:
            year = year_fun(Path(stata_label_file).name)
            stata_obj = Stata(stata_label_file, convert_dates=False, convert_categoricals=False)
            self._stata_label_object[year] = stata_obj

        return self

    @property
    def stata_object(self):
        """ 返回stata对象

        :return: 返回stata对象
        """
        return self._stata_object

    @property
    def stata_label_object(self):
        """ 返回stata中变量和值标签关联对象

        :return:
        """
        return self._stata_label_object

    def store_data_to_db(self, data_collection=None, label_collection=None):
        """ 把stata对象中的数据存入数据库

        :param data_collection:
        :param label_collection:
        :return: 返回self
        """
        if data_collection is None:
            data_collection = MonCollection(database=MonDatabase(mongodb=MongoDB(), database_name='surveydata'),
                                            collection_name='cgssdata').collection

        if label_collection is None:
            label_collection = MonCollection(database=MonDatabase(mongodb=MongoDB(), database_name='surveydata'),
                                             collection_name='cgsslabel').collection

        for year in self._stata_object:

            stata_data = self._stata_object[year].read()
            records = stata_data.to_dict("records")
            for record in records:
                record["year"] = year
                print(record)
                data_collection.insert_one(record)

            value_labels = self._stata_object[year].value_labels
            str_value_labels = dict()
            for key in value_labels:
                str_value_labels[key] = {str(inn_key):value_labels[key][inn_key] for inn_key in value_labels[key]}
            str_value_labels["year"] = year
            str_value_labels["type"] = "value labels"
            print(str_value_labels)
            label_collection.insert_one(str_value_labels)

            variable_labels = self._stata_object[year].variable_labels
            variable_labels["year"] = year
            variable_labels["type"] = "variable labels"
            print(variable_labels)
            label_collection.insert_one(variable_labels)

        return self

    def store_label_to_db(self, label_collection=None):
        """ 把变量和值标签关联存储到数据库

        :param label_collection:
        :return: 返回self
        """
        if label_collection is None:
            label_collection = MonCollection(database=MonDatabase(mongodb=MongoDB(), database_name='surveydata'),
                                             collection_name='cgsslabel').collection

        for year in self._stata_label_object:
            stata_label_data = self._stata_label_object[year].read()
            records = dict(zip(stata_label_data.loc[:,"name"], stata_label_data.loc[:,"vallab"]))
            records["year"] = year
            records["type"] = "variable value lables"
            print(records)
            label_collection.insert_one(records)

        return self


class CgssDatabase:
    def __init__(self, data_collection=None, label_collection=None):
        """ 初始化数据库连接

        :param data_collection:
        :param label_collection:
        """
        if data_collection is None:
            self._data_collection = MonCollection(database=MonDatabase(mongodb=MongoDB(conn_str='localhost:27017'), database_name='surveydata'),
                                                  collection_name='cgssdata').collection
        else:
            self._data_collection = data_collection

        if label_collection is None:
            self._label_collection = MonCollection(database=MonDatabase(mongodb=MongoDB(conn_str='localhost:27017'), database_name='surveydata'),
                                                   collection_name='cgsslabel').collection
        else:
            self._label_collection = label_collection

    def query(self, year, variables=None):

        if variables is not None:
            projection = {"_id": False}
            for var in variables:
                projection[var] = True

            found = self._data_collection.find({"year":year}, projection=projection)
        else:
            found = self._data_collection.find({"year":year}, projection={"_id": False, "year": False})

        pdataframe = iterator2dataframes(found,2000)
        #found = list(found)
        #pdataframe = pd.DataFrame(found)

        pdataframe = pd.DataFrame(pdataframe, columns=variables)
        pdataframe.index = range(1,pdataframe.shape[0]+1)

        return {"dataframe": pdataframe,
                "variable_labels": self.get_variable_label_df(year=year,variables=variables),
                "value_labels": self.get_variable_value_label_df(year=year,variables=variables)}

    def get_variable_label_df(self, year, variables=None):
        var_label_dict = self.get_variable_label(year=year)

        if variables is not None:
            result = pd.DataFrame([(var,var_label_dict[var]) for var in variables], columns=['variable','lable'])
        else:
            result = pd.DataFrame([(var,var_label_dict[var]) for var in var_label_dict], columns=['variable','label'])

        result.index = range(1, result.shape[0]+1)
        return result

    def get_variable_value_label_df(self, year, variables=None):
        var_value_link = self.get_variable_value_link(year=year)
        value_labels = self.get_value_label(year=year)
        value_label_dataframe = None

        if variables is None:
            variables = [var for var in self.get_variable_label(year=year)]

        for var in variables:
            value_label = var_value_link[var]
            if len(value_label) > 0:
                #print(var_value_link[var], " ---> ", value_labels[value_label])
                if value_label_dataframe is None:
                    value_label_dataframe = pd.DataFrame([(key, value_labels[value_label][key])
                                                          for key in value_labels[value_label]],
                                                         columns=["value", "label"])
                    value_label_dataframe['variable'] = var
                    value_label_dataframe = pd.DataFrame(value_label_dataframe, columns=["variable", "value", "label"])
                else:
                    tmp_dataframe = pd.DataFrame([(key, value_labels[value_label][key])
                                                  for key in value_labels[value_label]], columns=["value", "label"])
                    tmp_dataframe['variable'] = var
                    tmp_dataframe = pd.DataFrame(tmp_dataframe, columns=["variable", "value", "label"])
                    value_label_dataframe = pd.concat([value_label_dataframe, tmp_dataframe])

        return value_label_dataframe

    def get_variable_value_link(self, year):
        """ 返回变量和值标签关联信息

        :param year:
        :return:
        """
        return self._label_collection.find({"type": "variable value lables", "year": year},
                                           projection={"_id": False, "type": False, "year": False})[0]

    def get_variable_label(self, year):
        """ 返回某年份的cgss变量

        :param year:
        :return:
        """
        return self._label_collection.find({"type":"variable labels", "year":year},
                                           projection={"_id": False, "type":False, "year":False})[0]

    def get_value_label(self, year):
        """ 返回某年份的cgss值标签

        :param year:
        :return:
        """
        return self._label_collection.find({"type":"value labels", "year":year},
                                           projection={"_id": False, "type":False, "year":False})[0]

    @property
    def year(self):
        """ 返回数据库中cgss的时间跨度

        :return:
        """
        return self._data_collection.find().distinct('year')


def iterator2dataframes(iterator, chunk_size: int):
    """Turn an iterator into multiple small pandas.DataFrame
    This is a balance between memory and efficiency
    """
    records = []
    frames = []
    for i, record in enumerate(iterator):
        records.append(record)
        if i % chunk_size == chunk_size - 1:
            frames.append(pd.DataFrame(records))
            records = []
    if records:
        frames.append(pd.DataFrame(records))

    return pd.concat(frames) if frames else pd.DataFrame()


if __name__ == '__main__':
    """
    file_path = r"E:\plutoese\project\lasting\datacollector\CGSS\to_be_import\data"
    sheet = CgssStataSheet(file_path)
    print(sheet.read_data().stata_object)"""

    cgssdb = CgssDatabase()
    print(cgssdb.year)
    cgssdb.get_variable_label_df(year="2005").to_excel(r'E:\plutoese\project\lasting\datacollector\CGSS\output\vars.xlsx')


