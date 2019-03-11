# coding = UTF-8

from tarjan import tarjan
from collections import deque, defaultdict

class Individual:
    """个体基类.

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
        # 偏好序
        self.preferences_rank = self._preferences_rank()
        # 匹配结果
        self.matched = None

    def _preferences_rank(self):
        """偏好序.

        偏好序
        """
        preferences_rank = dict()
        i = 1
        for item in self.preferences:
            if isinstance(item, str):
                preferences_rank[item] = i
            elif isinstance(item, set):
                for unit in item:
                    preferences_rank[unit] = i
            else:
                print('Wrong type!')
                raise Exception
            i = i + 1

        return preferences_rank

    def __repr__(self):
        """打印信息.

        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        return fmt.format(type=self.__class__.__name__, name=self.name,
                          someone=self.matched.__repr__())

class Student(Individual):
    """学生类.

    用于描述学生.
    """

    def __init__(self, name, preferences):
        """男性类.

        :param str name: 名称
        :param list preferences: 偏好
        """
        super().__init__(name=name, preferences=preferences)
        # 追求列表
        self._proposal_list = preferences
        # 被接受者个体
        self._accepted_by = None

    def is_available(self):
        """该学生是否还需要进行匹配

        :return: 返回是否仍然需要匹配
        :rtype: bool
        """
        if (self._accepted_by is None) and (len(self._proposal_list) > 0):
            return True
        else:
            return False

    def point(self):
        """向清单中排名最靠前的被追求者提出请求.

        :return: 返回被追求者的名称
        :rtype: str
        """
        # 如果上一轮没有被女性暂时接受，并且追求列表不为零，
        # 那么返回追求列表中最靠前的个体，否则返回None
        if (self._accepted_by is None) and (len(self._proposal_list) > 0):
            return self._proposal_list[0]
        else:
            return None

    def remove_preference(self, preference):
        """移除一个偏好

        :param str preference: 偏好学校
        :return: 无返回值
        """
        if preference in self._proposal_list:
            self._proposal_list.pop(self._proposal_list.index(preference))

    def __repr__(self):
        """打印信息.

        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        if self._accepted_by is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone=self._accepted_by.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone='None')


class School(Individual):
    """学校类.

    用于描述学校.
    """

    def __init__(self, name, preferences, max_accepted=1):
        """女性类.

        :param str name: 名称
        :param list preferences: 偏好
        :param int max_accepted: 最多可接受追求者的数量，默认为1
        """
        super().__init__(name=name, preferences=preferences)
        # 追求列表
        self._proposal_list = preferences
        # 接受的追求者
        self._accept = []
        # 接受追求者的数量
        self._accept_number = max_accepted

    def is_available(self):
        """该学校是否还有空缺

        :return: 返回是否仍有空缺
        :rtype: bool
        """
        if (len(self._accept) < self._accept_number) and (len(self._proposal_list) > 0):
            return True
        else:
            return False

    def point(self):
        """向清单中排名最靠前的被追求者提出请求.

        :return: 返回被追求者的名称
        :rtype: str
        """
        # 如果上一轮没有被女性暂时接受，并且追求列表不为零，
        # 那么返回追求列表中最靠前的个体，否则返回None
        if len(self._proposal_list) > 0:
            return self._proposal_list[0]
        else:
            return None

    def remove_preference(self, preference):
        """移除一个偏好

        :param str preference: 偏好学校
        :return: 无返回值
        """
        if preference in self._proposal_list:
            self._proposal_list.pop(self._proposal_list.index(preference))

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

    def __init__(self, students=None, schools=None):
        """初始化.

        param list students: 学生列表
        param list schools: 学校列表
        """
        self._students = students
        self._schools = schools

        self._students_mapping = {student.name: student for student in self._students}
        self._schools_mapping = {school.name: school for school in self._schools}

    def matching(self, echo=False):
        # 是否继续匹配的标志
        match_flag = True
        # 匹配的轮次
        round = 1

        not_available_students = []
        not_available_schools = []

        while (match_flag):
            # 组合有向链
            available_individuals = defaultdict(list)

            for student in self._students:
                for nv_school in not_available_schools:
                    student.remove_preference(nv_school)

                if student.is_available():
                    available_individuals[student.name].append(student.point())

            for school in self._schools:
                for nv_student in not_available_students:
                    school.remove_preference(nv_student)

                if school.is_available():
                    available_individuals[school.name].append(school.point())

            if len(available_individuals) < 1:
                break

            tarjan_result = tarjan(available_individuals)
            print(tarjan_result)

            not_available_students = []
            not_available_schools = []
            for cycle in tarjan_result:
                if len(cycle) > 1:
                    cycle_deque = deque(cycle)
                    for n in range(0,int(len(cycle)/2)):
                        student = self._students_mapping[cycle_deque.pop()]
                        school = self._schools_mapping[cycle_deque.pop()]
                        student._accepted_by = school
                        school._accept.append(student)

                        not_available_students.append(student.name)
                        if not school.is_available():
                            not_available_schools.append(school.name)

            if echo:
                print('-' * 10, 'round{}'.format(round), '-' * 10)
                for student in self._students:
                    print(student)

                for school in self._schools:
                    print(school)

            round += 1

    @property
    def result(self):
        students_result = defaultdict(list)
        for item in self._students:
            if item._accepted_by is None:
                students_result[item.name].append(item._accepted_by)
            else:
                if isinstance(item._accepted_by, School):
                    students_result[item.name].append(item._accepted_by.name)

        schools_result = defaultdict(list)
        for item in self._schools:
            if item._accept is None:
                schools_result[item.name].append(item._accept)
            else:
                if isinstance(item._accept, Student):
                    schools_result[item.name].append(item._accept.name)
                else:
                    schools_result[item.name].\
                        extend([unit.name for unit in item._accept])

        return {'match_for_students': students_result,
                'match_for_schools': schools_result}

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

    students = [Student('s1', ['B', 'A']),
                Student('s2', ['A']),
                Student('s3', ['A', 'B'])]
    schools = [School('A', ['s1', 's2', 's3']),
               School('B', ['s3', 's1'])]

    matcher = StableMatcher(students=students, schools=schools)
    matcher.matching()
    print(matcher)
    print(matcher.result)