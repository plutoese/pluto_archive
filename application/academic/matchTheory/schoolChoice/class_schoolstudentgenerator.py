# coding = UTF-8

"""
=========================================
学校选择模型中的学校和学生生成器
=========================================

:Author: glen
:Date: 2019.1.16
:Tags: preferences generator
:abstract: to generate different preferences based on conditions

**类**
==================
CityGenerator
地区生成器

StudentsGenerator
个体偏好生成器

SchoolGenerator
偏好生成器

**使用方法**
==================
无
"""

import random
from operator import itemgetter
from scipy.stats import uniform
from itertools import permutations


class CityGenerator:
    """城市生成器

    用于生成城市
    """
    def __init__(self, name, economy):
        self._name = name
        self._economy = economy

    @property
    def name(self):
        return self.name


class CollegeGenerator:
    """学校生成器

    用于生成学校
    """
    def __init__(self, number=1, capacity=None, academic=None, city=None):
        """ 初始化

        :param int number: 学校数量
        :param capacity: 学校招生名额
        :param academic: 学校的学术水平
        :param city: 学校所在城市
        """
        self._number = number
        self._capacity = capacity
        self._academic = academic
        self._city = city
        self._colleges = []

    def generator(self):
        for i in range(1, self._number + 1):
            college_name = ''.join(['C', "%02d" % i])
            college_capacity = self._capacity[i-1]
            self._colleges.append({'name': college_name, 'capacity': college_capacity})

        return self

    def set_academic(self, academic):
        i = 0
        for college in self._colleges:
            college['academic'] = academic[i]
            i += 1

        return self

    def set_preference_by_score(self, students):
        preference = [item['name'] for item in sorted(students, key=itemgetter('score'), reverse=True)]

        for college in self._colleges:
            college['preference'] = preference

        return self

    @property
    def colleges(self):
        return self._colleges


class StudentGenerator:
    """学生生成器

    用于生成学生
    """
    def __init__(self, number=1, score=None, city=None):
        self._number = number
        self._score = score
        self._city = city
        self._students = []

    def generator(self):
        for i in range(1, self._number + 1):
            student_name = ''.join(['S', "%02d" % i])
            self._students.append({'name': student_name})

        return self

    def set_score(self, scores):
        for i in range(len(self._students)):
            self._students[i]['score'] = scores[i]

        return self

    def set_preferences(self, preferences):
        for i in range(len(self._students)):
            self._students[i]['preference'] = preferences[i]

        return self

    @property
    def students(self):
        return self._students

if __name__ == '__main__':
    colleges_generator = CollegeGenerator(number=2, capacity=[1, 1])
    colleges = colleges_generator.generator().colleges
    print(colleges)
    college_names = [item['name'] for item in colleges]

    num = 10
    students_generator = StudentGenerator(number=num)
    rv = uniform()
    r = uniform.rvs(size=num)
    students_generator.generator().set_score(list(r))
    preferences = [random.choice(list(permutations(college_names, len(college_names)))) for i in range(num)]
    students_generator.set_preferences(preferences)
    students = students_generator.students
    print(students)

    colleges_generator.set_preference_by_score(students)
    print(colleges_generator.colleges)
