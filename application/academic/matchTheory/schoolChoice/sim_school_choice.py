# 导入库
import copy
import time
import random
import numpy as np
from operator import itemgetter
from scipy.stats import uniform
from itertools import permutations

from application.academic.acadamicAdvisorsAssignment.class_DAMatch import StableMatcher as DAAStableMatcher
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Male as Student
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Female as College
from application.academic.matchTheory.schoolChoice.class_schoolstudentgenerator import CollegeGenerator, StudentGenerator


class SimSchoolChoice:
    def __init__(self, college_number=1, student_number=1, college_capacity=None, score_dist=uniform, colleges=None, students=None):
        # params setup
        self._college_number = college_number
        self._student_number = student_number
        self._college_capacity = college_capacity

        self._score_dist = score_dist
        #self._colleges = None
        self._colleges_generator = None
        #self._students = None
        self._students_generator = None

        self._colleges = colleges
        self._students = students

        self._college_match_objects = None
        self._student_match_objects = None

        self._matcher = None

    def generate_colleges_and_students(self):
        # 生成学校和学生基础信息

        # 学校
        self._colleges_generator = CollegeGenerator(number=self._college_number, capacity=self._college_capacity)
        self._colleges_generator.generator()
        #college_names = [item['name'] for item in self._colleges_generator.colleges]

        # 学生
        self._students_generator = StudentGenerator(number=self._student_number)

        scores = list(self._score_dist.rvs(size=self._student_number))
        self._students_generator.generator().set_score(scores)

        return self

    def generate_student_preference(self, fn):
        self._students_generator.set_preferences(fn(self._student_number, self._colleges_generator))

        return self

    def generate_college_preference(self):
        self._colleges_generator.set_preference_by_score(self.students)

        return self

    def generate_objects(self, College=None, Student=None):
        self._college_match_objects = [College(item['name'], item['preference'], item['capacity']) for item in self.colleges]
        self._student_match_objects = [Student(item['name'], item['preference']) for item in self.students]

        return self

    def set_capacities(self, college_capacity):
        i = 0
        for college in self.colleges:
            college['capacity'] = college_capacity[i]
            i += 1

        return self

    def matching(self, stable_matcher=None, echo=False):
        # 匹配
        self._matcher = stable_matcher(men=self._student_match_objects, women=self._college_match_objects)
        self._matcher.match(echo=echo)

        return self

    def matched_score_summarize(self, fn=min):
        student_scores = {item['name']: item['score'] for item in self.students}
        colleges_result = self._matcher.result['match_for_pursueds']

        college_scores = dict()
        for col_name in colleges_result:
            college_scores[col_name] = fn([student_scores[stu] for stu in colleges_result[col_name]])

        return college_scores

    @staticmethod
    def random_preferences(student_number, colleges_generator):
        college_names = [item['name'] for item in colleges_generator.colleges]
        preferences = []
        for i in range(student_number):
            college_names = copy.copy(college_names)
            random.shuffle(college_names)
            preferences.append(college_names)

        return preferences

    @staticmethod
    def inclined_preferences_with_academic(student_number, colleges_generator, theta=0.5):
        college_names = [item['name'] for item in colleges_generator.colleges]
        preferences = []
        for i in range(student_number):
            college_value = [theta * item['academic'] + (1 - theta) * np.random.uniform() for item in colleges_generator.colleges]
            college_dict = dict(zip(college_value, college_names))
            preferences.append([college_dict[k] for k in sorted(college_dict, reverse=True)])

        return preferences

    @property
    def colleges_generator(self):
        return self._colleges_generator

    @property
    def students_generator(self):
        return self._students_generator

    @property
    def colleges(self):
        if self._colleges_generator is not None:
            return self._colleges_generator.colleges
        elif self._colleges is not None:
            return self._colleges
        else:
            raise Exception

    @property
    def students(self):
        if self._students_generator is not None:
            return self._students_generator.students
        elif self._students is not None:
            return self._students
        else:
            raise Exception

    @property
    def matcher(self):
        return self._matcher


if __name__ == '__main__':
    sim = SimSchoolChoice(college_number=2, student_number=4, college_capacity=[2]*2)
    sim.generate_colleges_and_students()
    sim.colleges_generator.set_academic([0.4,0.2])
    sim.generate_college_preference().generate_student_preference(sim.inclined_preferences_with_academic)
    sim.generate_objects(College=College, Student=Student)
    print(sim.colleges)
    print(sim.students)

    sim.matching(stable_matcher=DAAStableMatcher, echo=True)
    print(sim.matcher)
    print(sim.matched_score_summarize(fn=np.min))
