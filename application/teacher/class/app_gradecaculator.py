# coding = UTF-8

import pandas as pd

# 1. 导入数据文件
BASE_FILE_PATH = r'E:\datahouse\classdata\econometrics2018'

data_file = pd.read_excel("\\".join([BASE_FILE_PATH,'homework.xlsx']),header=None)

# 2. 检验
print(data_file)

# 3. 计算平时成绩
base_grade = 39
w1 = 5
w2 = 3
w3 = 3

# 中级计量经济学课程
econometrics_base_grade = 25
econometrics_w1 = 0.3
econometrics_w2 = 5
econometrics_w3 = 2

grade = base_grade + data_file[3].mul(w1) + data_file[4].mul(w1) + data_file[5].mul(w1)
grade = grade + data_file[6].mul(w2) + data_file[7].mul(w2)
grade = grade + data_file[8].mul(w3) + data_file[9].mul(w3) + data_file[10].mul(w3)
grade = grade.apply(int)

econometrics_grade = econometrics_base_grade + data_file[11].mul(econometrics_w1)
econometrics_grade = econometrics_grade + data_file[3].mul(econometrics_w2) + data_file[4].mul(econometrics_w2) + data_file[5].mul(econometrics_w2)
econometrics_grade = econometrics_grade + data_file[6].mul(econometrics_w3) + data_file[7].mul(econometrics_w3) + data_file[8].mul(econometrics_w3) + data_file[9].mul(econometrics_w3) + data_file[10].mul(econometrics_w3)
econometrics_grade = econometrics_grade.apply(int)

data_file[12] = econometrics_grade
#data_file.iloc[:,11] = list(grade)

data_file.to_excel("\\".join([BASE_FILE_PATH,'grade.xlsx']))