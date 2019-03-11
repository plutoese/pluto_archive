# coding = UTF-8


import sys
import os
import io
import re
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# to import data
BASE_FILEPATH = r'E:\datahouse\projectdata\academictutor\checkstudent'

students = []
for item in os.listdir(os.path.join(BASE_FILEPATH, 'econ163')):
    students.append(re.sub('\s+', '', re.split('-', item)[0]))

econ161 = pd.read_excel(os.path.join(BASE_FILEPATH, 'econ161.xlsx'))
students.extend([re.sub('\s+', '', item) for item in econ161['姓名']])

econ162 = pd.read_excel(os.path.join(BASE_FILEPATH, 'econ162.xlsx'))
students.extend([re.sub('\s+', '', item) for item in econ162['姓名']])

trade160 = pd.read_excel(os.path.join(BASE_FILEPATH, 'trade160.xlsx'))
students.extend([re.sub('\s+', '', item) for item in trade160['姓名']])

print(len(students), len(set(students)))

all_students_data = pd.read_excel(os.path.join(BASE_FILEPATH,
                                               'allstudents.xlsx'))
all_students = [re.sub('\s+', '', item) for item in all_students_data['姓名']]

print(len(all_students), len(set(all_students)))

print(set(students) - set(all_students))
print(set(all_students) - set(students))
