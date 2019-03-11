# 导入库
import numpy as np
from application.academic.matchTheory.schoolChoice.sim_school_choice import SimSchoolChoice
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import StableMatcher as DAAStableMatcher
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Male as Student
from application.academic.acadamicAdvisorsAssignment.class_DAMatch import Female as College

class MatchQuality:
    def __init__(self, colleges, students, matcher):
        # params setup
        self._colleges = colleges
        self._students = students
        self._matcher = matcher

        # 学生的偏好
        self._student_preferences = {item['name']:item['preference'] for item in self._students}
        # 学生的成绩
        self._student_scores = {item['name']: item['score'] for item in self._students}

        # 学校的偏好
        self._college_preferences = {item['name']: item['preference'] for item in self._colleges}
        # 学校的招生名额
        self._college_capacities = {item['name']: item['capacity'] for item in self._colleges}

        # 学校匹配的结果
        self._colleges_result = self._matcher.result['match_for_pursueds']
        # 学生匹配的结果
        self._students_result = self._matcher.result['match_for_pursuers']

    def score_summarize(self, fn=min):
        """分数的描述性统计

        :param fn: 统计函数
        :return:
        """
        college_score_summarize = dict()
        for col_name in self.matched_college_scores:
            college_score_summarize[col_name] = fn(self.matched_college_scores[col_name])

        return college_score_summarize

    def matched_percent(self, rank=1):
        matched_students = [key for key in self.matched_student_rank if self.matched_student_rank[key] == rank]
        matched_percent = 100 * len(matched_students) / self.matched_students_numbers

        return matched_percent

    def mismatch(self, another_mq):
        matched_student_rank = self.matched_student_rank
        another_matched_student_rank = another_mq.matched_student_rank

        over_mismatched = []
        under_mismatched = []
        right_matched = []
        for student in matched_student_rank:
            if matched_student_rank[student] < 0:
                if another_matched_student_rank[student] < 0:
                    right_matched.append(student)
                else:
                    under_mismatched.append(student)
            else:
                if matched_student_rank[student] == another_matched_student_rank[student]:
                    right_matched.append(student)
                elif matched_student_rank[student] < another_matched_student_rank[student]:
                    under_mismatched.append(student)
                else:
                    over_mismatched.append(student)

        return 100 * len(right_matched) / len(matched_student_rank), 100 * len(under_mismatched) / len(matched_student_rank), 100 * len(over_mismatched) / len(matched_student_rank)

    @property
    def matched_average_rank(self):
        matched_students = [self.matched_student_rank[key] for key in self.matched_student_rank if self.matched_student_rank[key] > 0]
        matched_percent = np.mean(matched_students)

        return matched_percent

    @property
    def matched_students_numbers(self):
        matched_students = [key for key in self.matched_student_rank if self.matched_student_rank[key] > 0]

        return len(matched_students)

    @property
    def matched_student_percent(self):
        matched_percent = 100 * self.matched_students_numbers / len(self.matched_student_rank)

        return matched_percent

    @property
    def matched_college_scores(self):
        _college_scores = dict()
        for col_name in self._colleges_result:
            _college_scores[col_name] = [self._student_scores[stu] for stu in self._colleges_result[col_name]]

        return _college_scores

    @property
    def matched_student_rank(self):
        student_matched_rank = dict()
        for student in self._students_result:
            if self._students_result[student][0] is not None:
                student_matched_rank[student] = self._student_preferences[student].index(
                    self._students_result[student][0]) + 1
            else:
                student_matched_rank[student] = -1

        return student_matched_rank


if __name__ == '__main__':
    sim = SimSchoolChoice(college_number=2, student_number=4, college_capacity=[2, 2])
    sim.generate_colleges_and_students()
    sim.colleges_generator.set_academic([0.4, 0.2])
    sim.generate_college_preference().generate_student_preference(sim.inclined_preferences_with_academic)
    sim.generate_objects(College=College, Student=Student)
    print(sim.students)
    print(sim.colleges)
    sim.matching(DAAStableMatcher, echo=True)
    matcher1 = sim.matcher
    print(matcher1)

    sim2 = SimSchoolChoice(college_number=2, student_number=4, college_capacity=[2, 2], colleges=sim.colleges, students=sim.students)
    sim2.set_capacities([3, 1])
    sim2.generate_objects(College=College, Student=Student)
    sim2.matching(DAAStableMatcher, echo=True)
    matcher2 = sim2.matcher
    print(matcher2)

    sim3 = SimSchoolChoice(college_number=2, student_number=4, college_capacity=[2, 2], colleges=sim.colleges,
                           students=sim.students)
    sim3.set_capacities([1, 3])
    sim3.generate_objects(College=College, Student=Student)
    sim3.matching(DAAStableMatcher, echo=True)
    matcher3 = sim3.matcher
    print(matcher3)

    '''
    mq = MatchQuality(colleges=sim.colleges, students=sim.students, matcher=sim.matcher)
    print(mq.score_summarize(fn=np.mean))

    print(mq.matched_college_scores)
    print(mq.matched_student_rank)

    print(mq.mismatch(MatchQuality(colleges=sim2.colleges, students=sim2.students, matcher=sim2.matcher)))

    
    print(mq.matched_students_numbers)
    print(mq.matched_student_percent)

    print(mq.matched_percent())
    print(mq.matched_percent(rank=2))

    print(mq.matched_average_rank)'''
