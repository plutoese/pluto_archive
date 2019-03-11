# coding=UTF-8

"""
=========================================
cgss管理接口
=========================================

:Author: glen
:Date: 2018.06.11
:Tags: cgss mongodb
:abstract:

**使用方法**
==================
"""

from lib.datacollection.cgss.class_cgsscollector import CgssDatabase

# 连接cgss数据库接口
cgssdb = CgssDatabase()

"""
# 打印相关信息
print(cgssdb.year)

variables = cgssdb.get_variable_label(year="2005")
print(len(variables))

values = cgssdb.get_value_label(year="2005")
print(len(values))

variable_values = cgssdb.get_variable_value_link(year="2005")
print(len(set(variable_values.values())))"""

result = cgssdb.query(year="2010", variables=["s41","s43","s43","a2","a3a","a3b","a4","a5","a7a","a10"])

print("Begin to output......")
# 输出文件
#result['dataframe'].to_excel(r"E:\plutoese\project\lasting\datacollector\CGSS\output\datatable.xlsx")
#result['variable_labels'].to_excel(r"E:\plutoese\project\lasting\datacollector\CGSS\output\variable_label.xlsx")
#result['value_labels'].to_excel(r"E:\plutoese\project\lasting\datacollector\CGSS\output\value_labels.xlsx")
