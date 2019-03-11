# coding = UTF-8

"""
=========================================
匹配管理者
=========================================

:Author: glen
:Date: 2018.10.03
:Tags: match manager
:abstract: to admin individual and matching

**类**
==================
MatcherManager
匹配管理者

**使用方法**
==================
无
"""

import os
import re
import copy
import pandas as pd
from collections import defaultdict, Counter
from class_preferences_generator import PreferencesGenerator
from class_DAMatch import Male, Female, StableMatcher


class MatcherManager:
    """匹配管理者.

    匹配管理者
    """

    def __init__(self):
        """初始化.

        初始化
        """
        self._imported_pursuers_dataframe = None
        self._imported_pursueds_dataframe = None

        self._pursuer_preferences = dict()
        self._pursued_preferences = dict()
        self._pursued_max_accepted = dict()

        self._pursuer_preferences_for_matching = None
        self._pursued_preferences_for_matching = None
        self._pursued_max_accepted_for_matching = None

        self._pursuers = None
        self._pursueds = None

        self._pursuer_recorder = defaultdict(list)
        self._pursued_recorder = defaultdict(list)

        self._match_results = []

    def setup(self, pursuer_preferences, pursued_preferences,
              pursued_max_accepted):
        """初始化方法.

        初始化方法
        """
        self._pursuer_preferences = pursuer_preferences
        self._pursued_preferences = pursued_preferences
        self._pursued_max_accepted = pursued_max_accepted

    def match(self, echo=False):
        """匹配.

        :param int times: 匹配次数
        :return: 返回匹配结果
        """
        matcher = StableMatcher(men=self.pursuers,
                                women=self.pursueds)
        matcher.match()

        if echo:
            print(matcher)

        result = copy.deepcopy(matcher.result)
        result['result_for_print'] = matcher.__repr__()
        result['pursuer_preferences'] = self.pursuer_preferences_for_matching
        result['pursued_preferences'] = self.pursued_preferences_for_matching
        result['pursued_max_accepted'] = self.pursued_max_accepted_for_matching

        self._match_results.append(result)

    @property
    def match_results_stat(self):
        """匹配结果统计.

        匹配结果统计
        """
        results_stat = dict()

        results_stat['round_number'] = len(self.match_results)

        pursuers_recorder = defaultdict(list)
        pursueds_recorder = defaultdict(list)
        for result in self.match_results:
            match_result_for_pursuers = result['match_for_pursuers']
            for pursuer in match_result_for_pursuers:
                pursuers_recorder[pursuer].\
                    extend(match_result_for_pursuers[pursuer])

            match_result_for_pursueds = result['match_for_pursueds']
            for pursued in match_result_for_pursueds:
                pursueds_recorder[pursued].\
                    extend(match_result_for_pursueds[pursued])

        pursuers_counter = dict()
        pursueds_counter = dict()
        for pursuer in pursuers_recorder:
            pursuers_counter[pursuer] = Counter(pursuers_recorder[pursuer])
        for pursued in pursueds_recorder:
            pursueds_counter[pursued] = Counter(pursueds_recorder[pursued])

        results_stat['pursuers_recorder'] = pursuers_recorder
        results_stat['pursueds_recorder'] = pursueds_recorder

        results_stat['pursuers_counter'] = pursuers_counter
        results_stat['pursueds_counter'] = pursueds_counter

        return results_stat

    def append_preferences(self, group, preferences, type='pursuer',
                           random_order=False):
        """添加偏好.

        :param str,list group: 个体或个体集合
        :param list preferences: 偏好序
        :param bool random_order: 是否乱序，默认为是
        """
        if type == 'pursuer':
            group_with_preferences = \
                {name: self._pursuer_preferences_for_matching[name]
                 for name in group}
        elif type == 'pursued':
            group_with_preferences = \
                {name: self._pursued_preferences_for_matching[name]
                 for name in group}
        else:
            print('Wrong Type!')
            raise Exception

        pg = PreferencesGenerator(group_with_preferences)
        pg.append_preferences(preferences, random_order)
        generated_preference = pg.to_dict()
        for name in generated_preference:
            if type == 'pursuer':
                self._pursuer_preferences_for_matching[name] \
                    = generated_preference[name]
            elif type == 'pursued':
                self._pursued_preferences_for_matching[name] \
                    = generated_preference[name]
            else:
                print('Wrong Type!')
                raise Exception

        return self

    def import_pursuers(self, source, type='excel'):
        """导入追求者数据.

        :param str source: 数据来源，可以是excel文件或者其他格式
        :param str type: 来源类型，'excel'表示excel文件
        """
        imported_dataframe = None

        if type == 'excel':
            imported_dataframe = self.__import_individuals_data(source, type)

        if self._imported_pursuers_dataframe is None:
            self._imported_pursuers_dataframe = imported_dataframe
        else:
            self._imported_pursuers_dataframe = pd.concat([
                self._imported_pursuers_dataframe,
                imported_dataframe
            ])

        self._imported_pursuers_dataframe.index = \
            range(self._imported_pursuers_dataframe.shape[0])

        return self

    def import_pursueds(self, source, type='excel'):
        """导入被追求者数据.

        :param str source: 数据来源，可以是excel文件或者其他格式
        :param str type: 来源类型，'excel'表示excel文件
        """
        imported_dataframe = None

        if type == 'excel':
            imported_dataframe = self.__import_individuals_data(source, type)

        if self._imported_pursueds_dataframe is None:
            self._imported_pursueds_dataframe = imported_dataframe
        else:
            self._imported_pursueds_dataframe = pd.concat([
                self._imported_pursueds_dataframe,
                imported_dataframe
            ])

        self._imported_pursueds_dataframe.index = \
            range(self._imported_pursueds_dataframe.shape[0])

        return self

    def to_compose_preferences(self, pursuer_col=('name', 'preference'),
                               pursued_col=('name', 'preference', 'number')):
        """分解变量.

        :param tuple pursuer_col: 表示追求者名称和偏好的变量名
        :param tuple pursued_col: 表示被追求者名称和偏好的变量名
        :return: 返回自身
        """
        # 追求者的循环
        pursuer_data = self._imported_pursuers_dataframe
        for ind in pursuer_data.index:
            # 追求者的姓名
            pursuer_name = pursuer_data.loc[ind, pursuer_col[0]]
            # 追求者的偏好
            pursuer_preference = pursuer_data.loc[ind, pursuer_col[1]]

            # 分解追求者的偏好，并储存到追求者的姓名和偏好字典
            if isinstance(pursuer_preference, float):
                self._pursuer_preferences[pursuer_name] = []
            else:
                self._pursuer_preferences[pursuer_name] = \
                    re.split('\|', pursuer_preference)

        # 被追求者的循环
        pursued_data = self._imported_pursueds_dataframe
        for ind in pursued_data.index:
            # 被追求者的姓名
            pursued_name = pursued_data.loc[ind, pursued_col[0]]
            # 被追求者的偏好
            pursued_preference = pursued_data.loc[ind, pursued_col[1]]
            # 被追求者可接受的限额人数
            pursued_max_accepted_number = pursued_data.loc[ind, pursued_col[2]]

            # 分解被追求者的偏好，并储存到被追求者的姓名和偏好字典
            if isinstance(pursued_preference, float):
                self._pursued_preferences[pursued_name] = []
            else:
                self._pursued_preferences[pursued_name] = \
                    re.split('\|', pursued_preference)
            # 被追求者的姓名和限额字典
            self._pursued_max_accepted[pursued_name] = \
                int(pursued_max_accepted_number)

        return self

    def copy_for_matching(self):
        """复制偏好副本，为匹配做准备.

        复制偏好副本，为匹配做准备
        """
        self._pursuer_preferences_for_matching \
            = copy.deepcopy(self._pursuer_preferences)
        self._pursued_preferences_for_matching \
            = copy.deepcopy(self._pursued_preferences)
        self._pursued_max_accepted_for_matching \
            = copy.deepcopy(self._pursued_max_accepted)

        return self

    @property
    def pursuer_preferences(self):
        """返回追求者偏好序.

        返回追求者偏好序
        """
        return self._pursuer_preferences

    @property
    def pursued_preferences(self):
        """返回被追求者偏好序.

        返回被追求者偏好序
        """
        return self._pursued_preferences

    @property
    def pursued_max_accepted(self):
        """返回被追求者的限额.

        返回被追求者的限额
        """
        return self._pursued_max_accepted

    @property
    def pursuer_preferences_for_matching(self):
        """用于匹配的追求者偏好序.

        用于匹配的追求者偏好序
        """
        return self._pursuer_preferences_for_matching

    @property
    def pursued_preferences_for_matching(self):
        """用于匹配的被追求者偏好序.

        用于匹配的被追求者偏好序
        """
        return self._pursued_preferences_for_matching

    @property
    def pursued_max_accepted_for_matching(self):
        """用于匹配的被追求限额.

        用于匹配的被追求者限额
        """
        return self._pursued_max_accepted_for_matching

    @property
    def pursuer_set(self):
        """追求者集合.

        追求者集合
        """
        return set(self.pursuer_preferences.keys())

    @property
    def pursued_set(self):
        """被追求者集合.

        被追求者集合
        """
        return set(self.pursued_preferences.keys())

    @property
    def pursuers(self):
        """追求者列表.

        追求者列表
        """
        pursuers_list = []
        for pursuer in self.pursuer_preferences_for_matching:
            pursuers_list.append(
                Male(pursuer, self.pursuer_preferences_for_matching[pursuer]))

        return pursuers_list

    @property
    def pursueds(self):
        """追求者列表.

        追求者列表
        """
        pursueds_list = []
        for pursued in self.pursued_preferences_for_matching:
            pursueds_list.append(Female(
                pursued,
                self.pursued_preferences_for_matching[pursued],
                self.pursued_max_accepted_for_matching[pursued]))

        return pursueds_list

    @property
    def match_results(self):
        """返回匹配结果.

        返回匹配结果
        """
        return self._match_results

    def __import_individuals_data(self, source=None, type='excel'):
        """导入数据.

        :param str source: 数据来源，可以是excel文件或者其他格式
        :param str type: 来源类型，'excel'表示excel文件
        """
        if type == 'excel':
            return self.__import_from_excel(source)

    def __import_from_excel(self, excel_file):
        """导入Excel文件.

        导入Excel文件
        """
        return pd.read_excel(excel_file)


if __name__ == '__main__':
    mm = MatcherManager()
    check_one = True
    if check_one:
        BASELINE_PATH = 'E:/datahouse/projectdata/academictutor/checkdir'
        pursuer_file = os.path.join(BASELINE_PATH, 'students.xlsx')
        pursuer2_file = os.path.join(BASELINE_PATH, 'students2.xlsx')
        pursued_file = os.path.join(BASELINE_PATH, 'teachers.xlsx')

        mm.import_pursuers(pursuer_file).import_pursueds(pursued_file)
        print(mm._imported_pursuers_dataframe)
        print(mm._imported_pursueds_dataframe)

    check_two = True
    if check_two:
        print('--------Check TWO--------')
        mm.to_compose_preferences()
        print(mm.pursuer_preferences)
        print(mm.pursued_preferences)
        print(mm.pursued_max_accepted)
        print(mm.pursuer_set)
        print(mm.pursued_set)

    check_three = True
    if check_three:
        print('--------Check THREE-------')
        mm.copy_for_matching()
        mm.append_preferences(list(mm.pursuer_set), list(mm.pursued_set),
                              type='pursuer')
        print(mm.pursuer_preferences_for_matching)
        mm.copy_for_matching()
        #mm.append_preferences(list(mm.pursuer_set), list(mm.pursued_set),
        #                      type='pursuer')
        #mm.append_preferences(list(mm.pursued_set), list(mm.pursuer_set),
        #                      type='pursued')
        print(mm.pursuer_preferences_for_matching)
        print(mm.pursuers)

    check_four = True
    if check_four:
        print('--------Check FOUR-------')
        mm.match()
        print(mm.match_results[0]['result_for_print'])

    check_five = True
    if check_five:
        print('--------Check Five-------')
        mm2 = MatcherManager()
        mm2.setup(pursuer_preferences=mm.pursuer_preferences,
                  pursued_preferences=mm.pursued_preferences,
                  pursued_max_accepted=mm.pursued_max_accepted)
        mm2.copy_for_matching()
        mm2.match()
        print(mm2.match_results[0]['result_for_print'])
