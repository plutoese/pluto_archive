# coding = UTF-8

import random
import numpy as np
import pandas as pd
import os
import re
import copy
from collections import Counter, defaultdict
from application.academic.matchTheory.algorithm.class_DAmatch import Male, Female, StableMatcher

# 1. to generate data
# 1'. to import data
BASELINE_PATH = r'E:\datahouse\projectdata\academictutor'
teacher_data = pd.read_excel(os.path.join(BASELINE_PATH,'new_teacher.xlsx'))
student_data = pd.read_excel(os.path.join(BASELINE_PATH,'new_students.xlsx'))

# 所有的学生
all_students = [re.sub('\s+','',stu) for stu in student_data.iloc[:,1]]
# 所有的老师
all_teachers = [re.sub('\s+','',tea) for tea in teacher_data.iloc[:,0]]

teacher_preference = {}
teacher_number = {}
for ind in teacher_data.index:
    teacher = teacher_data.loc[ind,'教师']
    preference = teacher_data.loc[ind,'偏好的学生']
    number = teacher_data.loc[ind,'指导学生数']

    if isinstance(preference,float):
        teacher_preference[teacher] = []
    else:
        teacher_preference[teacher] = re.split('\|',preference)
    teacher_number[teacher] = int(number)

student_preference = {}
for ind in student_data.index:
    student = student_data.loc[ind,'姓名']
    preference = student_data.loc[ind,'偏好的老师']

    if isinstance(preference,float):
        student_preference[student] = []
    else:
        student_preference[student] = re.split('\|',preference)

for teacher in teacher_preference:
    for student in teacher_preference[teacher]:
        if student not in all_students:
            print('Not good! ', student)

for student in student_preference:
    for teacher in student_preference[student]:
        if teacher not in all_teachers:
            print('Not good! ', student, '->', teacher)


# 2 to generate data
def generate_random_preference(all_teacher, all_student, teacher_preferences, student_preferences, teacher_numbers):
    all_teacher_copy = copy.copy(all_teacher)
    all_student_copy = copy.copy(all_student)
    teacher_preferences_copy = copy.deepcopy(teacher_preferences)
    student_preferences_copy = copy.deepcopy(student_preferences)
    teacher_numbers_copy = copy.copy(teacher_numbers)

    gen_teacher_preference = []
    for teacher in teacher_preferences_copy:
        rest = list(set(all_student_copy) - set(teacher_preferences_copy[teacher]))
        random.shuffle(rest)
        preferences = teacher_preferences_copy[teacher]
        preferences.extend(rest)
        #print(teacher,len(preferences),teacher_numbers[teacher])
        gen_teacher_preference.append(Female(teacher,preferences,teacher_numbers_copy[teacher]))

    gen_student_preference = []
    for student in student_preferences_copy:
        rest = list(set(all_teacher_copy) - set(student_preferences_copy[student]))
        random.shuffle(rest)
        preferences = student_preferences_copy[student]
        preferences.extend(rest)
        #print(student, len(preferences))
        gen_student_preference.append(Male(student, preferences))

    return gen_teacher_preference, gen_student_preference

sim_number = 1000
student_recorder = defaultdict(list)

for n in range(sim_number):
    print(n)
    gen_teacher_preference, gen_student_preference = generate_random_preference(all_teachers,
                                                                                all_students,
                                                                                teacher_preference,
                                                                                student_preference,
                                                                                teacher_number)

    '''
    print('-'*50)
    for item in gen_teacher_preference:
        print(item.name,' -> ',item.preferences)
    print('-'*50)
    print('\n')'''

    # 2. to run match model
    matcher = StableMatcher(men=gen_student_preference, women=gen_teacher_preference)
    matcher.match()

    # 3. to report result
    for student in matcher._men:
        #print(student.name,student._accepted_by.name)
        student_recorder[student.name].append(student._accepted_by.name)

#print(student_recorder)
teacher_recorder = defaultdict(list)
for student in student_recorder:
    counter = Counter(student_recorder[student])
    most_common = counter.most_common(2)
    print(student,most_common,most_common[0][1])

    if len(most_common) < 2:
        teacher_recorder[most_common[0][0]].append(student)
        continue

    if (most_common[0][1] > 100) and (most_common[0][1] > most_common[1][1]*2):
        teacher_recorder[most_common[0][0]].append(student)

left_all_student = copy.copy(all_students)
left_all_teacher = copy.copy(all_teachers)
left_student_preference = copy.copy(student_preference)
student_selected = []
left_teacher_preference = copy.copy(teacher_preference)
left_teacher_number = copy.copy(teacher_number)

final_result_teacher = defaultdict(list)
for teacher in teacher_recorder:
    print(teacher,'->',teacher_recorder[teacher])
    final_result_teacher[teacher].extend(teacher_recorder[teacher])
    left_teacher_number[teacher] = left_teacher_number[teacher] - len(teacher_recorder[teacher])
    student_selected.extend(teacher_recorder[teacher])
    for student in teacher_recorder[teacher]:
        del left_student_preference[student]

left_all_student = list(left_student_preference.keys())

#print(len(student_selected),student_selected)
for teacher in left_teacher_preference:
    new_preference = []
    for pref in left_teacher_preference[teacher]:
        if pref in student_selected:
            #print('Found!', pref)
            pass
        else:
            new_preference.append(pref)
    left_teacher_preference[teacher] = new_preference

#print(left_teacher_number)
#print(left_teacher_preference)
#print(left_student_preference)
#print(left_all_student)
#print(left_all_teacher)

gen_teacher_preference2, gen_student_preference2 = generate_random_preference(left_all_teacher,
                                                                              left_all_student,
                                                                              left_teacher_preference,
                                                                              left_student_preference,
                                                                              left_teacher_number)
matcher = StableMatcher(men=gen_student_preference2, women=gen_teacher_preference2)
matcher.match()
for teacher in matcher._women:
    if teacher._accept is not None:
        final_result_teacher[teacher.name].extend([item.name for item in teacher._accept])

for student in matcher._men:
    print(student)

for key in final_result_teacher:
    print(key,' ', ' '.join(final_result_teacher[key]))