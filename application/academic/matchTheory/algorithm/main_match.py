# coding = UTF-8

import random
import os
import sys
import io
import re
import copy
import pandas as pd
from collections import Counter, defaultdict
from application.academic.matchTheory.algorithm.class_DAmatch import Male, \
    Female, StableMatcher

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


# 函数
# 数据导入函数
def import_data(pursuer_file, pursued_file):
    """导入追求者和被追求者的数据.

    导入数据文件（规范格式的数据文件，第一列是姓名或id，第二列是偏好，用|分隔，被追求者有第三列，是最大可接受对象的数量），储存到相应的变量中.
    """
    # 读取追求者的数据到变量pursuer_data
    pursuer_data = pd.read_excel(pursuer_file)
    # 读取被追求者的数据到变量pursued_data
    pursued_data = pd.read_excel(pursued_file)

    return pursuer_data, pursued_data


# 导入组别数据
def import_grouped_data(file_path):
    """导入组别数据.

    分组数据对数据添加组别条件
    """
    imported_data = pd.read_excel(file_path)
    return list(imported_data.iloc[:, 0])


def compose_data(pursuer_data, pursued_data,
                 pursuer_col=('name', 'preference'),
                 pursued_col=('name', 'preference', 'number')):
    """分解变量.

    分解数据到不同的变量中
    """
    # 追求者的姓名和偏好字典
    pursuer_preferences = dict()
    # 被追求者的姓名和偏好字典
    pursued_preferences = dict()
    # 被追求者的姓名和最多可接受对象数目字典
    pursued_max_accepted = dict()

    # 追求者的循环
    for ind in pursuer_data.index:
        # 追求者的姓名
        pursuer_name = pursuer_data.loc[ind, pursuer_col[0]]
        # 追求者的偏好
        pursuer_preference = pursuer_data.loc[ind, pursuer_col[1]]

        # 分解追求者的偏好，并储存到追求者的姓名和偏好字典
        if isinstance(pursuer_preference, float):
            pursuer_preferences[pursuer_name] = []
        else:
            pursuer_preferences[pursuer_name] = re.split('\|',
                                                         pursuer_preference)

    # 被追求者的循环
    for ind in pursued_data.index:
        # 被追求者的姓名
        pursued_name = pursued_data.loc[ind, pursued_col[0]]
        # 被追求者的偏好
        pursued_preference = pursued_data.loc[ind, pursued_col[1]]
        # 被追求者可接受的限额人数
        pursued_max_accepted_number = pursued_data.loc[ind, pursued_col[2]]

        # 分解被追求者的偏好，并储存到被追求者的姓名和偏好字典
        if isinstance(pursued_preference, float):
            pursued_preferences[pursued_name] = []
        else:
            pursued_preferences[pursued_name] = re.split('\|',
                                                         pursued_preference)
        # 被追求者的姓名和限额字典
        pursued_max_accepted[pursued_name] = int(pursued_max_accepted_number)

    return pursuer_preferences, pursued_preferences, pursued_max_accepted


def append_preferences(setA, setB, random=True):
    """根据setB添加偏好到setA的个体中.

    :param dict setA: 需要添加偏好的集合
    :param list setB: 偏好个体集合
    :param bool random: 是否添加随机偏好序
    """
    copy_setA = copy.deepcopy(setA)
    if random:
        preferences


def generate_random_preferences(pursuer_preferences, pursued_preferences):
    """生成随机偏好，补充缺失的偏好.

    利用随机生成的偏好，来补充缺失的偏好
    """
    # 追求者偏好副本
    copy_pursuer_preferences = copy.deepcopy(pursuer_preferences)
    # 被追求者偏好副本
    copy_pursued_preferences = copy.deepcopy(pursued_preferences)

    # 所有追求者列表
    copy_all_pursuer = list(copy_pursuer_preferences.keys())
    # 所有被追求者列表
    copy_all_pursued = list(copy_pursued_preferences.keys())

    # 生成追求者的随机偏好，填充缺失的偏好
    gen_pursuer_preferences = dict()
    for pursuer in copy_pursuer_preferences:
        rest_pursuer = list(set(copy_all_pursued) -
                            set(copy_pursuer_preferences[pursuer]))
        random.shuffle(rest_pursuer)
        copy_preferences = copy_pursuer_preferences[pursuer]
        copy_preferences.extend(rest_pursuer)
        gen_pursuer_preferences[pursuer] = copy_preferences

    # 生成被追求者的随机偏好，填充缺失的偏好
    gen_pursued_preferences = dict()
    for pursued in copy_pursued_preferences:
        rest_pursued = list(set(copy_all_pursuer) -
                            set(copy_pursued_preferences[pursued]))
        random.shuffle(rest_pursued)
        copy_preferences = copy_pursued_preferences[pursued]
        copy_preferences.extend(rest_pursued)
        gen_pursued_preferences[pursued] = copy_preferences

    return gen_pursuer_preferences, gen_pursued_preferences


def pursuer_factory(pursuer_preferences):
    """追求者工厂.

    根据追求者偏好，生成追求者列表
    """
    pursuers_list = []
    for pursuer in pursuer_preferences:
        pursuers_list.append(Male(pursuer, pursuer_preferences[pursuer]))

    return pursuers_list


def pursued_factory(pursued_preferences, pursued_max_accepted):
    """被追求者工厂.

    根据被追求者偏好，生成被追求者列表
    """
    pursueds_list = []
    for pursued in pursued_preferences:
        pursueds_list.append(Female(pursued, pursued_preferences[pursued],
                                    pursued_max_accepted[pursued]))

    return pursueds_list


# 1. 参数设置
BASELINE_PATH = 'E:/datahouse/projectdata/academictutor'
pursuer_file = os.path.join(BASELINE_PATH, 'student_preferences.xlsx')
pursued_file = os.path.join(BASELINE_PATH, 'teacher_preferences.xlsx')

# 2. 数据导入
# 2.1 导入追求者和被追求者的偏好数据
pursuer_data, pursued_data = import_data(pursuer_file, pursued_file)

# 2.2 导入追求者的组别数据
foreign_pursuers = import_grouped_data(os.path.join(BASELINE_PATH,
                                                    'foreign_students.xlsx'))
trade_major_pursuers = import_grouped_data(os.path.join(BASELINE_PATH,
                                                        'trade_students.xlsx'))

# 2.3 导入被追求者的组别数据
foreign_pursueds = import_grouped_data(os.path.join(BASELINE_PATH,
                                                    'foreign_teacher.xlsx'))
English_pursueds = import_grouped_data(os.path.join(BASELINE_PATH,
                                                    'English_teachers.xlsx'))

# 3. 数据清洗
# 3.1 根据导入数据生成追求者偏好字典、被追求者偏好字典以及被追求者的限额字典
pursuer_preferences, pursued_preferences, pursued_max_accepted \
    = compose_data(pursuer_data, pursued_data)

to_check_individual = False
if to_check_individual:
    for p in foreign_pursuers:
        if p not in pursuer_preferences.keys():
            print('Wrong')

    for p in trade_major_pursuers:
        if p not in pursuer_preferences.keys():
            print('Wrong')

    for p in foreign_pursueds:
        if p not in pursued_preferences.keys():
            print('Wrong')

    for p in English_pursueds:
        if p not in pursued_preferences.keys():
            print('Wrong')

'''
# 3.2 模拟数据检验
# 3.2.1 生成模拟数据
To_generate_simulation_data = False
if To_generate_simulation_data:
    gen_pursuer_preferences, gen_pursued_preferences = \
        generate_random_preferences(pursuer_preferences, pursued_preferences)

# 3.2.2 检验模拟数据的长度是否一致
To_check_generated_preferences = False
number_of_pursued = 39
number_of_pursuer = 142
if To_check_generated_preferences:
    for pursuer in gen_pursuer_preferences:
        if len(gen_pursuer_preferences[pursuer]) == number_of_pursued:
            pass
        else:
            print(pursuer, 'Wrong!', len(gen_pursuer_preferences[pursuer]))

    # to check
    for pursued in gen_pursued_preferences:
        if len(gen_pursued_preferences[pursued]) == number_of_pursuer:
            pass
        else:
            print(pursuer, 'Wrong!', len(gen_pursued_preferences[pursued]))

# 3.2.3 输出模拟数据到Excel文件
To_export_generated_preferences = False
if To_export_generated_preferences:
    dframe = pd.DataFrame(gen_pursuer_preferences)
    dframe.to_excel(os.path.join(BASELINE_PATH, 'gen_preferences.xlsx'))

# 3.2.4 打印模拟数据
To_check_factory_data = False
if To_check_factory_data:
    factory_data = pursuer_factory(gen_pursuer_preferences)
    for one in factory_data:
        print("{}: {}".format(one.name, ' '.join(one.preferences)))

# 4. 匹配
Simulation_Number = 1
pursuer_recorder = defaultdict(list)
pursued_recorder = defaultdict(list)

for n in range(Simulation_Number):
    print('Round {}'.format(n))
    gen_pursuer_preferences, gen_pursued_preferences = \
        generate_random_preferences(pursuer_preferences, pursued_preferences)

    # to run match model
    matcher = StableMatcher(men=pursuer_factory(gen_pursuer_preferences),
                            women=pursued_factory(gen_pursued_preferences,
                                                  pursued_max_accepted))
    matcher.match()
    print(matcher)
'''
