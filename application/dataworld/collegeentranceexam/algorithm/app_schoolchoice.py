# coding = UTF-8

import random
import numpy as np
import pandas as pd
from scipy.stats import uniform
from application.dataworld.collegeentranceexam.algorithm.class_SDAlgorithm import Student, School, StableMatcher

# 0. 参数设置
# location
location = ['Shanghai', 'Lanzhou']
# 学校数量
school_number = 100


def simulation(accepted_number=100, theta=0.5, location_preference_for_Shanghai=1, location_preference_for_Lanzhou=0.6):
    # 1. 生成学校
    schools = []
    total_students = 10000
    for i in range(1,school_number+1):
        school_location = random.choice(location)
        if school_location == 'Shanghai':
            schools.append(School(''.join(['u',str(i)]), max_accepted=accepted_number,
                                  location=school_location, score=uniform.rvs(loc=0.2,scale=0.8,size=1)[0]))
        else:
            schools.append(School(''.join(['u', str(i)]), max_accepted=accepted_number,
                                  location=school_location, score=uniform.rvs(loc=0, scale=0.6, size=1)[0]))
        total_students += accepted_number

    # 生成学生
    students = []
    for j in range(0, total_students):
        student_name = ''.join(['s',str(j)])
        preference = dict()
        student_score = random.randint(400,700) + np.random.rand()
        for school in schools:
            if school.location == 'Shanghai':
                preference_score = uniform.rvs(loc=0,scale=location_preference_for_Shanghai,size=1)[0]
            else:
                preference_score = uniform.rvs(loc=0,scale=location_preference_for_Lanzhou,size=1)[0]
            preference_score = theta * school.score + (1-theta) * preference_score
            preference[preference_score] = school.name
        student_preference = [preference[key] for key in sorted(preference, reverse=True)]
        students.append(Student(student_name, student_preference, student_score))

    matcher = StableMatcher(students=students, schools=schools, isOrdered=False)
    matcher.match()

    school_name = []
    school_max_accepted = []
    school_score = []
    school_location = []
    school_average_score = []
    for school in schools:
        school_name.append(school.name)
        school_max_accepted.append(school._max_accepted)
        school_score.append(school.score)
        school_location.append(school.location)
        school_average_score.append(school.average_score)

    pdframe = pd.DataFrame({'school_name':school_name, 'school_max_accepted': school_max_accepted,
                            'school_score': school_score, 'school_location': school_location,
                            'school_average_score': school_average_score})
    pdframe['location_preference_for_Lanzhou'] = location_preference_for_Lanzhou
    pdframe['location_preference_for_Shanghai'] = location_preference_for_Shanghai
    pdframe['theta'] = theta

    return pdframe
'''
count_number = 0
for theta in range(1, 10, 2):
    print(count_number)
    theta = theta / 10
    if count_number < 1:
        dataframe = simulation(theta=theta)
    else:
        dataframe = pd.concat([dataframe, simulation(theta=theta)])
    count_number += 1

dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\secondtime\sim_by_theta2.xlsx')

'''
count_number = 0
for location_preference_for_Lanzhou in range(4, 11, 2):
    print(count_number)
    location_preference_for_Lanzhou = location_preference_for_Lanzhou / 10
    if count_number < 1:
        dataframe = simulation(location_preference_for_Lanzhou=location_preference_for_Lanzhou)
    else:
        dataframe = pd.concat([dataframe, simulation(location_preference_for_Lanzhou=location_preference_for_Lanzhou)])
    count_number += 1

dataframe.to_excel(r'E:\cyberspace\worklot\college\dataset\secondtime\sim_by_location_preference2.xlsx')




