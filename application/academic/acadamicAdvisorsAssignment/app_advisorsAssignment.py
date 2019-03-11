# coding = UTF-8

"""
@title: 学术导师分配主程序
@author: Glen
@date: 2018/10/03
"""

import os
import pandas as pd
from class_matcherManager import MatcherManager


class AdvisorsAssignment:
    """导师分配主类.

    导师分配主类
    """

    def __init__(self):
        """初始化.

        初始化
        """
        self._matcher_manager = MatcherManager()
        self._base_path = 'E:/datahouse/projectdata/academictutor'

        self._foreign_students = None
        self._foreign_teachers = None
        self._trade_major_students = None
        self._English_teachers = None

    def load_data(self):
        """导入追求者和被追求者数据.

        导入追求者和被追求者数据
        """
        pursuer_file = os.path.join(self._base_path,
                                    'student_preferences.xlsx')
        pursued_file = os.path.join(self._base_path,
                                    'teacher_preferences.xlsx')

        self._matcher_manager.import_pursuers(pursuer_file)
        self._matcher_manager.import_pursueds(pursued_file)

        self._matcher_manager.to_compose_preferences()

    def import_special_data(self):
        """导入特别数据.

        导入特别数据
        """
        foreign_students_file = \
            pd.read_excel(os.path.join(self._base_path,
                                       'foreign_students.xlsx'))
        foreign_students = list(foreign_students_file['name'])
        trade_students_file = \
            pd.read_excel(os.path.join(self._base_path,
                                       'trade_students.xlsx'))
        trade_students = list(trade_students_file['name'])
        foreign_teachers_file = \
            pd.read_excel(os.path.join(self._base_path,
                                       'foreign_teachers.xlsx'))
        foreign_teachers = list(foreign_teachers_file['name'])
        English_teachers_file = \
            pd.read_excel(os.path.join(self._base_path,
                                       'English_teachers.xlsx'))
        English_teachers = list(English_teachers_file['name'])

        check = False
        if check:
            print(set(foreign_students) - self._matcher_manager.pursuer_set)
            print(set(trade_students) - self._matcher_manager.pursuer_set)
            print(set(foreign_teachers) - self._matcher_manager.pursued_set)
            print(set(foreign_teachers) - self._matcher_manager.pursued_set)

        self._foreign_students = foreign_students
        self._foreign_teachers = foreign_teachers
        self._trade_major_students = trade_students
        self._English_teachers = English_teachers

        return self

    def append_simulation_prefereces(self):
        """添加模拟偏好.

        添加模拟偏好
        """
        self._matcher_manager.copy_for_matching()

        self._matcher_manager.append_preferences(self._foreign_teachers,
                                                 [set(self._foreign_students)],
                                                 type='pursued')
        self._matcher_manager.append_preferences(self._foreign_students,
                                                 self._foreign_teachers,
                                                 type='pursuer')
        self._matcher_manager.append_preferences(self._English_teachers,
                                                 [set(self._foreign_students),
                                                  set(self._trade_major_students)],
                                                 type='pursued')
        self._matcher_manager.append_preferences(list(self.all_pursued),
                                                 self.all_pursuer,
                                                 type='pursued')

    def match_once(self, echo=False):
        """一次匹配.

        一次匹配
        """
        self._matcher_manager.match(echo=echo)

    def match_many(self, times):
        """多次匹配.

        多次匹配
        """
        for n in range(times):
            self.append_simulation_prefereces()
            self._matcher_manager.match()

    @property
    def all_pursuer(self):
        return self.matcher_manager.pursuer_set

    @property
    def all_pursued(self):
        return self.matcher_manager.pursued_set

    @property
    def matcher_manager(self):
        """匹配管理者.

        匹配管理者
        """
        return self._matcher_manager

    @property
    def match_results(self):
        """匹配结果.

        匹配结果
        """
        return self._matcher_manager.match_results


if __name__ == '__main__':
    assign_manager = AdvisorsAssignment()
    assign_manager.load_data()
    assign_manager.import_special_data()
    assign_manager.append_simulation_prefereces()
    #print(assign_manager.matcher_manager.pursuer_preferences_for_matching)
    print(assign_manager.matcher_manager.pursued_preferences_for_matching)
    #print(assign_manager.matcher_manager.pursued_max_accepted_for_matching)

    assign_manager.match_once()
    print(assign_manager.match_results[0]['result_for_print'])
