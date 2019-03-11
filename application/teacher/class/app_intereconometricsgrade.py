# coding = UTF-8

import pandas as pd

# 1. 导入数据文件
BASE_FILE_PATH = r'E:\datahouse\classdata\intereconometrics'

data_file = pd.read_excel("\\".join([BASE_FILE_PATH,'raw_grade.xlsx']),header=None)

# 2. 检验
print(data_file.iloc[:,0:9])

# 3. 计算平时成绩
base_grade = 54
w1 = 5
w2 = 4

grade = base_grade + data_file[3].mul(w1) + data_file[4].mul(w1)
grade = grade + data_file[6].mul(w2) + data_file[7].mul(w2)
grade = grade.apply(int)

data_file[9] = grade
data_file.to_excel("\\".join([BASE_FILE_PATH,'grade.xlsx']))