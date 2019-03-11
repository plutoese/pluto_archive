# coding = UTF-8

"""
=========================================
偏好生成器
=========================================

:Author: glen
:Date: 2018.10.02
:Tags: preferences generator
:abstract: to generate different preferences based on conditions

**类**
==================
PreferenceGeneratorForIndividual
个体偏好生成器

PreferencesGenerator
偏好生成器

**使用方法**
==================
无
"""

import copy
import random
from collections import deque


class PreferenceGeneratorForIndividual:
    """个体偏好生成器.

    用于生成个体的偏好
    """

    def __init__(self, individual):
        """初始化.

        :param str,dict individual: 个体
        """
        self._name, self._preference = self.__init(individual)

    def append_preferences(self, preferences, random_order=False,
                           difference=True):
        """添加偏好.

        :param str,list preference: 偏好序
        :param bool random: 是否乱序
        :param bool difference: 是否删除重复的偏好
        :return: 无返回值
        """
        if isinstance(preferences, str):
            preferences = [preferences]

        # 复制不会出现引用的错误
        copy_preferences = copy.deepcopy(preferences)

        # 删除重复的偏好
        if difference:
            common_preferences = set(copy_preferences) & set(self._preference)
            for cp in common_preferences:
                copy_preferences.remove(cp)

        # 乱序偏好
        if random_order:
            random.shuffle(copy_preferences)

        print('append: ', preferences, copy_preferences)
        self._preference.extend(copy_preferences)

    def __init(self, individual):
        """初始化个体名称和偏好.

        :param str,dict,tuple,list individual: 个体
        :return: 返回姓名和偏好
        :rtype: tuple
        """
        if isinstance(individual, str):
            return individual, []

        if isinstance(individual, dict):
            if len(individual) < 2:
                copy_individual = copy.deepcopy(individual)
                return list(copy_individual.keys())[0], \
                    list(copy_individual.values())[0]
            else:
                print('Too much!')
                raise Exception

        if isinstance(individual, (tuple, list)):
            if len(individual) < 2:
                return individual[0], []
            elif len(individual) < 3:
                if isinstance(individual[1], (tuple, list)):
                    return copy.deepcopy(individual)
                else:
                    print('Too much!')
                    raise Exception
            else:
                print('Too much!')
                raise Exception

    @property
    def name(self):
        """返回名称.

        返回名称
        """
        return self._name

    @property
    def preference(self):
        """返回偏好.

        返回偏好
        """
        return self._preference

    @property
    def individual(self):
        """返回个体名称和偏好.

        返回个体名称和偏好
        """
        return (self.name, self.preference)

    def __repr__(self):
        """打印信息.

        打印信息
        """
        fmt = '{}: {}'
        return fmt.format(self.name, ','.join(self.preference))


class PreferencesGenerator:
    """偏好生成器.

    偏好生成器
    """

    def __init__(self, group):
        """初始化.

        :param str,list,dict group: 个体集合
        """
        self._individuals = self.__init(group)

    def append_preferences(self, preferences, random_order=False,
                           difference=True):
        """添加偏好.

        :param list preferences: 偏好序
        :param bool random_order: 是否乱序，默认为否
        :param bool difference: 是否删除重复偏好，默认为是
        :return: 返回自身
        """
        for individual in self._individuals:
            individual.append_preferences(preferences,
                                          random_order,
                                          difference)
        return self

    def to_dict(self):
        """转换为字典.

        转换为字典类型
        """
        individuals_list = []
        for individual in self._individuals:
            individuals_list.append(individual.individual)

        return dict(individuals_list)

    def __init(self, group):
        """初始化.

        :param str,list,dict group: 个体集合
        """
        if isinstance(group, str):
            return [PreferenceGeneratorForIndividual(group)]

        if isinstance(group, (list, tuple)):
            individuals = []
            individual_deque = deque()
            for item in group:
                if len(individual_deque) < 1:
                    if isinstance(item, str):
                        individual_deque.append(item)
                    else:
                        print('Wrong Type!')
                        raise Exception
                else:
                    if isinstance(item, str):
                        individuals.append(PreferenceGeneratorForIndividual
                                           (individual_deque.pop()))
                        individual_deque.append(item)
                    elif isinstance(item, (tuple, list)):
                        individuals.append(PreferenceGeneratorForIndividual
                                           ([individual_deque.pop(), item]))
                    else:
                        print('Wrong Type!')
                        raise Exception

            if len(individual_deque) > 0:
                individuals.append(PreferenceGeneratorForIndividual
                                   (individual_deque.pop()))

            return individuals

        if isinstance(group, dict):
            individuals = []
            for name in group:
                individuals.append(PreferenceGeneratorForIndividual
                                   ([name, group[name]]))

            return individuals

    @property
    def individuals(self):
        """返回个体列表.

        返回个体列表
        """
        return self._individuals

    def __repr__(self):
        """打印信息.

        打印信息
        """
        fmt = ''
        for individual in self.individuals:
            fmt = '\n'.join([fmt, individual.__repr__()])
        return fmt


if __name__ == '__main__':
    individual_check = False
    if individual_check:
        p1 = {'m': ['w1', 'w2']}
        pgfi = PreferenceGeneratorForIndividual(p1)
        print(pgfi.name, pgfi.preference)
        p1['m'].append('w3')
        print(p1, pgfi.preference)
        p2 = ['w1', 'w4', 'w5']
        pgfi.append_preferences(p2)
        print(p2, pgfi.preference)
        p2.append('w6')
        print(p2, pgfi.preference)

        p3 = ['m', ['w1']]
        pgfi = PreferenceGeneratorForIndividual(p3)
        print(pgfi.name, pgfi.preference)
        p3[1].append('w4')
        print(p3, pgfi.preference)

    individuals_check = True
    if individuals_check:
        g1 = 'm1'
        pg = PreferencesGenerator(g1)
        print(pg)
        g2 = ['m1', ['w1', 'w2'], 'm2', 'm3', ['w1', 'w3']]
        pg = PreferencesGenerator(g2)
        print(pg)
        g3 = {'m1': ['w1', 'w2'], 'm2': [], 'm3': ['w1', 'w3']}
        pg = PreferencesGenerator(g3)
        print(pg)
        pg.append_preferences(['w1', 'w4', 'w5']).append_preferences(['w6'])
        print(pg)
        print(pg.to_dict())
