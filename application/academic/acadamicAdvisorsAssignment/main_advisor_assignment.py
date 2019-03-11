# coding = UTF-8

"""
@title: 学术导师分配主程序
@author: Glen
@date: 2018/10/06
"""

import copy
import pandas as pd
from app_advisorsAssignment import AdvisorsAssignment

# 初次匹配
first_assign_manager = AdvisorsAssignment()
first_assign_manager.load_data()
first_assign_manager.import_special_data()
first_assign_manager.append_simulation_prefereces()

first_assign_manager.match_once()
first_match_result = first_assign_manager.match_results[0]
print(first_match_result.keys())

pdata = pd.DataFrame(first_match_result['match_for_pursuers'])
pdata.T.to_excel(
    'E:/datahouse/projectdata/academictutor/result_first_students.xlsx')

# 再次匹配
first_match_for_pursuers = first_match_result['match_for_pursuers']
first_match_for_pursueds = first_match_result['match_for_pursueds']

copy_pursuer_preference = copy.deepcopy(first_assign_manager._matcher_manager.pursuer_preferences)
copy_pursued_prefrernce = copy.deepcopy(first_assign_manager._matcher_manager.pursued_preferences)
copy_pursued_max_accepted = copy.deepcopy(first_assign_manager._matcher_manager.pursued_max_accepted)

for pursuer in first_match_for_pursuers:
    if first_match_for_pursuers[pursuer][0] is not None:
        copy_pursuer_preference.pop(pursuer)
print(copy_pursuer_preference)

for pursued in first_match_for_pursueds:
    if first_match_for_pursueds[pursued][0] is not None:
        copy_pursued_max_accepted[pursued] = copy_pursued_max_accepted[pursued] - len(first_match_for_pursueds[pursued])
print(copy_pursued_max_accepted)

left_students = list(copy_pursuer_preference.keys())

second_assign_manager = AdvisorsAssignment()
second_assign_manager._matcher_manager.setup(pursuer_preferences=copy_pursuer_preference,
                                             pursued_preferences=copy_pursued_prefrernce,
                                             pursued_max_accepted=copy_pursued_max_accepted)
second_assign_manager.import_special_data()
second_assign_manager._matcher_manager.copy_for_matching()

all_foreign_students = second_assign_manager._foreign_students
all_trade_students = second_assign_manager._trade_major_students
left_foreign_students = set(left_students) & set(all_foreign_students)
left_trade_students = set(left_students) & set(all_trade_students)
left_rest_students = set(left_students) - set(left_foreign_students) - set(left_trade_students)
second_assign_manager._matcher_manager.append_preferences(list(left_foreign_students),
                                                          second_assign_manager._English_teachers,
                                                          type='pursuer', random_order=True)
#second_assign_manager._matcher_manager.append_preferences(list(left_foreign_students),
#                                                          list(copy_pursued_prefrernce.keys()),
#                                                          type='pursuer', random_order=True)
second_assign_manager._matcher_manager.append_preferences(list(left_trade_students),
                                                          second_assign_manager._English_teachers,
                                                          type='pursuer', random_order=True)
#second_assign_manager._matcher_manager.append_preferences(list(left_trade_students),
#                                                          list(copy_pursued_prefrernce.keys()),
#                                                          type='pursuer', random_order=True)
second_assign_manager._matcher_manager.append_preferences(list(left_rest_students),
                                                          list(copy_pursued_prefrernce.keys()),
                                                          type='pursuer', random_order=True)
second_assign_manager._matcher_manager.append_preferences(list(copy_pursued_prefrernce.keys()),
                                                          left_students,
                                                          type='pursued', random_order=True)
second_assign_manager.match_once()
second_match_result = second_assign_manager.match_results[0]
second_match_for_pursuers = second_match_result['match_for_pursuers']
second_match_for_pursueds = second_match_result['match_for_pursueds']

# 结果输出
# 对于教师
teachers_result = []
count = 0
for pursued in first_match_for_pursueds:
    if first_match_for_pursueds[pursued][0] is not None:
        count += len(first_match_for_pursueds[pursued])
        directed_students = ','.join(first_match_for_pursueds[pursued])
        if second_match_for_pursueds[pursued][0] is not None:
            count += len(second_match_for_pursueds[pursued])
            directed_students = ','.join([directed_students, ','.join(second_match_for_pursueds[pursued])])
    else:
        count += len(second_match_for_pursueds[pursued])
        directed_students = ','.join(second_match_for_pursueds[pursued])
    teachers_result.append((pursued, directed_students))
print(count)
teachers_pdata = pd.DataFrame(teachers_result)
teachers_pdata.to_excel(
    'E:/datahouse/projectdata/academictutor/result/result15_for_teachers.xlsx')

# 对于学生
students_result = []
for pursuer in first_match_for_pursuers:
    if first_match_for_pursuers[pursuer][0] is not None:
        students_result.append((pursuer, first_match_for_pursuers[pursuer][0]))
    else:
        if second_match_for_pursuers[pursuer][0] is not None:
            students_result.append((pursuer, second_match_for_pursuers[pursuer][0]))
        else:
            print('Not matched!', pursuer)

students_pdata = pd.DataFrame(students_result)
students_pdata.to_excel(
    'E:/datahouse/projectdata/academictutor/result/result15_for_students.xlsx')
