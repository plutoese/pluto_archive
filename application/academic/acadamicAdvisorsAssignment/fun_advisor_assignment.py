# coding = UTF-8

"""
@title: 学术导师分配主程序
@author: Glen
@date: 2018/10/06
"""

import copy
import pandas as pd
from app_advisorsAssignment import AdvisorsAssignment


class AdvisorsAssignmentForR:
    def __init__(self):
        self._first_assign_manager = AdvisorsAssignment()
        self._second_assign_manager = AdvisorsAssignment()

    def first_match(self):
        self._first_assign_manager.load_data()
        self._first_assign_manager.import_special_data()
        self._first_assign_manager.append_simulation_prefereces()

        self._first_assign_manager.match_once()

    def second_match(self):
        copy_pursuer_preference = copy.deepcopy(
            self._first_assign_manager._matcher_manager.pursuer_preferences)
        copy_pursued_prefrernce = copy.deepcopy(
            self._first_assign_manager._matcher_manager.pursued_preferences)
        copy_pursued_max_accepted = copy.deepcopy(
            self._first_assign_manager._matcher_manager.pursued_max_accepted)

        for pursuer in self.first_match_for_pursuers:
            if self.first_match_for_pursuers[pursuer][0] is not None:
                copy_pursuer_preference.pop(pursuer)

        for pursued in self.first_match_for_pursueds:
            if self.first_match_for_pursueds[pursued][0] is not None:
                copy_pursued_max_accepted[pursued] = copy_pursued_max_accepted[pursued] - len(self.first_match_for_pursueds[pursued])

        left_students = list(copy_pursuer_preference.keys())
        self._second_assign_manager._matcher_manager.setup(pursuer_preferences=copy_pursuer_preference,
                                                           pursued_preferences=copy_pursued_prefrernce,
                                                           pursued_max_accepted=copy_pursued_max_accepted)
        self._second_assign_manager.import_special_data()
        self._second_assign_manager._matcher_manager.copy_for_matching()

        all_foreign_students = self._second_assign_manager._foreign_students
        all_trade_students = self._second_assign_manager._trade_major_students
        left_foreign_students = set(left_students) & set(all_foreign_students)
        left_trade_students = set(left_students) & set(all_trade_students)
        left_rest_students = set(left_students) - set(left_foreign_students) - set(left_trade_students)
        self._second_assign_manager._matcher_manager.append_preferences(list(left_foreign_students),
                                                                        self._second_assign_manager._English_teachers,
                                                                        type='pursuer', random_order=True)
        self._second_assign_manager._matcher_manager.append_preferences(list(left_trade_students),
                                                                        self._second_assign_manager._English_teachers,
                                                                        type='pursuer', random_order=True)
        self._second_assign_manager._matcher_manager.append_preferences(list(left_rest_students),
                                                                        list(copy_pursued_prefrernce.keys()),
                                                                        type='pursuer', random_order=True)
        self._second_assign_manager._matcher_manager.append_preferences(list(copy_pursued_prefrernce.keys()),
                                                                        left_students,
                                                                        type='pursued', random_order=True)
        self._second_assign_manager.match_once()

    @property
    def first_match_result(self):
        return self._first_assign_manager.match_results[0]

    @property
    def first_match_for_pursuers(self):
        return self.first_match_result['match_for_pursuers']

    @property
    def first_match_for_pursueds(self):
        return self.first_match_result['match_for_pursueds']

    @property
    def second_match_result(self):
        return self._second_assign_manager.match_results[0]

    @property
    def second_match_for_pursuers(self):
        return self.second_match_result['match_for_pursuers']

    @property
    def second_match_for_pursueds(self):
        return self.second_match_result['match_for_pursueds']

    @property
    def isDone(self):
        pass

    @property
    def teachers_result(self):
        teachers_result = []
        count = 0
        for pursued in self.first_match_for_pursueds:
            if self.first_match_for_pursueds[pursued][0] is not None:
                count += len(self.first_match_for_pursueds[pursued])
                directed_students = ','.join(self.first_match_for_pursueds[pursued])
                if self.second_match_for_pursueds[pursued][0] is not None:
                    count += len(self.second_match_for_pursueds[pursued])
                    directed_students = ','.join([directed_students, ','.join(self.second_match_for_pursueds[pursued])])
            else:
                count += len(self.second_match_for_pursueds[pursued])
                if self.second_match_for_pursueds[pursued] is not None:
                    directed_students = ','.join(self.second_match_for_pursueds[pursued])
            teachers_result.append((pursued, directed_students))
        return pd.DataFrame(teachers_result), count

    @property
    def students_result(self):
        students_result = []
        for pursuer in self.first_match_for_pursuers:
            if self.first_match_for_pursuers[pursuer][0] is not None:
                students_result.append((pursuer, self.first_match_for_pursuers[pursuer][0]))
            else:
                if self.second_match_for_pursuers[pursuer][0] is not None:
                    students_result.append((pursuer, self.second_match_for_pursuers[pursuer][0]))
                else:
                    print('Not matched!', pursuer)
        return students_result

    def run(self):
        sign = True
        while sign:
            self.first_match()
            self.second_match()
            if self.teachers_result[1] >= 141:
                sign = False

if __name__ == '__main__':
    aa = AdvisorsAssignmentForR()
    aa.run()
