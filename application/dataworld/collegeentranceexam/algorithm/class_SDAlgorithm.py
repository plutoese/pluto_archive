# coding = UTF-8

"""
=========================================
匹配理论的SD(serial dictatorship mechanism)算法
=========================================

:Author: glen
:Date: 2018.10.24
:Tags: serial dictatorship mechanism
:abstract: DA algorithm of Gale and Shapley(1962)
:source: Roth, A.E. and Sotomayor, M.A.O. (1990). Two-sided matching: a study
in game-theoretic modeling and analysis, Econometric Society Monographs,
Vol. 18 (Cambridge University Press).

**类**
==================
Entity
    基类
School
    学校
Student
    学生类
StableMatcher
    匹配类

**使用方法**
==================
无
"""

from collections import deque


class Entity:
    """基类.

    主要用于被继承.
    """

    def __init__(self, name, preferences):
        """初始化.

        :param str name: 姓名
        :param list preferences: 偏好列表
        """
        # 名称
        self.name = name
        # 偏好
        self.preferences = preferences
        # 匹配结果
        self.matched = None

    def __repr__(self):
        """打印信息.

        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        return fmt.format(type=self.__class__.__name__, name=self.name,
                          someone=self.matched.__repr__())


class Student(Entity):
    """学生类.

    用于描述学生.
    """

    def __init__(self, name, preferences, score=None):
        """学生类.

        :param str name: 名称
        :param list preferences: 偏好
        """
        super().__init__(name=name, preferences=preferences)
        # 追求列表
        self._proposal_list = deque(preferences)
        # 被接受的学校
        self._accepted_by = None
        # 学生成绩
        self._score = score

    def propose(self):
        """向清单中排名最靠前的学校提出请求.

        :return: 返回被追求者的名称
        :rtype: str
        """
        # 如果上一轮没有被学校，并且追求列表不为零，
        # 那么返回追求列表中最靠前的个体，否则返回None
        if (self._accepted_by is None) and (len(self._proposal_list) > 0):
            return self._proposal_list.popleft()
        else:
            return None

    def __repr__(self):
        """打印信息.

        主要用于打印类信息.
        """
        fmt = '{type} {name} is accepted by {someone}'
        if self._accepted_by is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone=self._accepted_by.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone='None')


class School(Entity):
    """学校类.

    用于描述学校.
    """

    def __init__(self, name, max_accepted=1, preferences=None, location=None, score=None):
        """学校类.

        :param str name: 名称
        :param list preferences: 偏好
        :param int max_accepted: 最多可接受学生的数量，默认为1
        """
        super().__init__(name=name, preferences=preferences)
        # 接受的学生
        self._accept = []
        # 最多可接受学生的数量
        self._max_accepted = max_accepted
        # 学校地点
        self._location = location
        # 学校评分
        self._score = score

    def filtrate(self, student):
        """如果名额已满，拒绝学生；未满则接受学生.

        :return: 返回被接受的学生的名称
        """
        # 返回接受者，若无，则返回None
        if len(self._accept) < self._max_accepted:
            self._accept.append(student)
            return True
        else:
            return False

    @property
    def average_score(self):
        scores = []
        for student in self._accept:
            scores.append(student._score)
        return sum(scores)/len(scores)

    @property
    def location(self):
        return self._location

    @property
    def score(self):
        return self._score

    def __repr__(self):
        """打印信息.

        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        if self._accept is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone=' '.join([item.name
                                                for item in self._accept]))
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone='None')


class StableMatcher:
    """匹配主类.

    进行匹配的主类.
    """

    def __init__(self, students=None, schools=None, isOrdered=True):
        """初始化.

        param list students: 学生列表
        param list schools: 学校列表
        """
        if isOrdered:
            self._students = students
        else:
            core_students = {student._score: student for student in students}
            self._students = [core_students[score] for score in sorted(core_students, reverse=True)]

        self._schools = schools

        self._students_mapping = {student.name: student for student in self._students}
        self._schools_mapping = {school.name: school for school in self._schools}

    def match(self, echo=False):
        """进行匹配.

        进行匹配的主要函数
        """
        for student in self._students:
            while True:
                proposed_school = student.propose()
                if proposed_school is not None:
                    # 学校进行筛选
                    if self._schools_mapping[proposed_school].filtrate(student):
                        student._accepted_by = self._schools_mapping[proposed_school]
                        break
                else:
                    break

            if echo:
                print('-' * 10, 'round{}'.format(round), '-' * 10)
                for student in self._students:
                    print(student)

                for school in self._schools:
                    print(school)

    def __repr__(self):
        """打印匹配信息.

        :return: 无返回值
        """
        lines = '-'*50
        return_string = ''.join([lines, 'Final Reslut', lines])
        for student in self._students:
            return_string = '\n'.join([return_string, student.__repr__()])

        return_string = ''.join([return_string, '\n\n', 'In another way...',
                                 '\n'])

        for school in self._schools:
            return_string = '\n'.join([return_string, school.__repr__()])

        return_string = ''.join([return_string, '\n', lines,
                                 '-'*len('Final Reslut'), lines])

        return return_string


if __name__ == '__main__':

    students = [Student('s1', ['u1', 'u2'], 80),Student('s2', ['u2', 'u1'], 90),Student('s3', ['u1', 'u2'], 88),
                Student('s4', ['u2', 'u1'], 92)]
    schools = [School('u1', 3),School('u2', 1)]

    matcher = StableMatcher(students=students, schools=schools, isOrdered=False)
    matcher.match()
    print(matcher)
    for school in schools:
        print(school.name, school.average_score)
