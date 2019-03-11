# coding=UTF-8

"""
=========================================
dta数据存入MongoDB
=========================================

:Author: glen
:Date: 2018.06.10
:Tags: cgss mongodb
:abstract:

**使用方法**
==================
"""

from lib.datacollection.cgss.class_cgsscollector import CgssStataSheet

# 设置数据文件路径
FILE_PATH = r"E:\plutoese\project\lasting\datacollector\CGSS\to_be_import\data"

# 设置变量标签文件路径
LABEL_PATH = r"E:\plutoese\project\lasting\datacollector\CGSS\to_be_import\label"

# 创建CgssStataSheet类对象
sheet = CgssStataSheet(FILE_PATH, LABEL_PATH)

# 打印读取的stata对象信息
print(sheet.read_data().stata_object)

sheet.read_variable_label().store_label_to_db()

