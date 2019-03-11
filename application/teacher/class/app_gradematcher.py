# coding = UTF-8

import pandas as pd

# 1. 导入数据文件
BASE_FILE_PATH = r'D:\backup'

stud_names = pd.read_excel("\\".join([BASE_FILE_PATH,'names.xlsx']),header=None)
stud_names.columns = ['name']

stud_grade = pd.read_excel("\\".join([BASE_FILE_PATH,'grade.xlsx']),header=None)
stud_grade.columns = ['id','sid','name','3','4','5','6','7','8','9','10','11','12','13','14']

result = pd.merge(stud_names, stud_grade, on='name')
result.to_excel("\\".join([BASE_FILE_PATH,'result.xlsx']))