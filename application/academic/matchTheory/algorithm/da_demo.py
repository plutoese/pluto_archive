from collections import deque
import numpy as np
import pandas as pd
import random


class Individual:
    """个体基类
    :param str name: 名称
    :param list preferences: 偏好
    """

    def __init__(self, name, preferences, age, edu):
        # 名称
        self.name = name
        # 年龄
        self.age = age
        # 教育水平
        self.edu = edu
        # 偏好
        self.preferences = preferences
        # 匹配结果
        self.matched = None

    def __repr__(self):
        fmt = '{type} {name} matched {someone}'
        return fmt.format(type=self.__class__.__name__, name=self.name, someone=self.matched.__repr__())


class Male(Individual):
    """男性类
    :param str name: 名称
    :param list preferences: 偏好
    """

    def __init__(self, name, preferences, age=None, edu=None):
        super().__init__(name=name, preferences=preferences, age=age, edu=edu)
        # 求婚清单
        self._proposal_list = deque(preferences)
        # 被谁接受
        self._accepted_by = None

    def propose(self):
        """ 向清单中排名最靠前的女性求婚

        :return: 返回求婚对象的名称
        :rtype: str
        """
        # 如果上一轮没有被女性暂时接受，并且清单不为零，那么返回清单中最靠前的女性，否则返回None
        if (self._accepted_by is None) and (len(self._proposal_list) > 0):
            return self._proposal_list.popleft()
        else:
            return None

    def __repr__(self):
        fmt = '{type} {name} matched {someone}'
        if self._accepted_by is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone=self._accepted_by.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone='None')

    @property
    def is_matched(self):
        if self._accepted_by is not None:
            return True
        else:
            return False


class Female(Individual):
    """女性类
    :param str name: 名称
    :param list preferences: 偏好
    """

    def __init__(self, name, preferences, age=None, edu=None):
        super().__init__(name=name, preferences=preferences, age=age, edu=edu)
        # 求婚者列表
        self._be_prosoed_by = []
        # 接受了谁
        self._accept = None

    def filtrate(self):
        """ 筛选求婚者中的男性，接受最偏好的那个，拒绝其他所有求婚者

        :return: 返回被接受的男性的名称
        """
        self._be_prosoed_by[0]._accepted_by = None
        # 生成求婚者在女性偏好中的次序：求婚者姓名的字典
        print(self._be_prosoed_by)
        proposal_dict = {self.preferences.index(man.name): man.name for man in self._be_prosoed_by}
        # 获得求婚者的姓名
        accepted = proposal_dict[sorted(proposal_dict)[0]]
        return accepted

    def __repr__(self):
        fmt = '{type} {name} matched {someone}'
        if self._accept is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone=self._accept.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone='None')

    @property
    def is_matched(self):
        if self._accept is not None:
            return True
        else:
            return False


class StableMatcher:
    def __init__(self, men=None, women=None):
        self._men = men
        self._women = women

        self._men_mapping = {man.name: man for man in self._men}
        self._women_mapping = {woman.name: woman for woman in self._women}

    def match(self):
        # 求婚是否进行的标志
        match_flag = True
        round = 1

        while (match_flag):
            # 匹配中止标志
            match_flag = False

            for man in self._men:
                # 男性求婚
                proposed_female_name = man.propose()
                if proposed_female_name is not None:
                    match_flag = True
                    # 添加该求婚者到女性本轮要筛选的男性求婚者清单中
                    self._women_mapping[proposed_female_name]._be_prosoed_by.append(man)

            for woman in self._women:
                # 如果本轮有男性求婚者
                if len(woman._be_prosoed_by) > 0:
                    # 根据女性的偏好列表筛选男性求婚者，保留最喜欢的男性求婚者，拒绝其他人
                    accepted = woman.filtrate()
                    # 更新女性暂时接受的人选为求婚成功者
                    woman._accept = self._men_mapping[accepted]
                    # 把本轮求婚成功的男性放入向该女性求婚者的列表中，以便下一轮重新进行筛选
                    woman._be_prosoed_by = [woman._accept]
                    # 更新求婚成功者男性的暂时成功匹配对象为该女性
                    woman._accept._accepted_by = woman

            if match_flag:
                print('-' * 10, 'round{}'.format(round), '-' * 10)
                for man in self._men:
                    print(man)

            round += 1

    @property
    def men(self):
        return self._men


## 1. 初始化环境和设置参数
# 1.1 设置男女群体的人数
NUMBER_OF_MEN = 10
NUMBER_OF_WOMEN = 10

# 1.2 设置年龄
MEN_AGE_MU = 30
MEN_AGE_SIGMA = 5
MEN_AGE = list(np.random.normal(MEN_AGE_MU, MEN_AGE_SIGMA, NUMBER_OF_MEN))

WOMEN_AGE_MU = 30
WOMEN_AGE_SIGMA = 5
WOMEN_AGE = list(np.random.normal(WOMEN_AGE_MU, WOMEN_AGE_SIGMA, NUMBER_OF_WOMEN))

# 1.3 设置教育水平
MEN_EDU_MU = 12
MEN_EDU_SIGMA = 3
MEN_EDU = list(np.random.normal(MEN_EDU_MU, MEN_EDU_SIGMA, NUMBER_OF_MEN))

WOMEN_EDU_MU = 10
WOMEN_EDU_SIGMA = 2
WOMEN_EDU = list(np.random.normal(WOMEN_EDU_MU, WOMEN_EDU_SIGMA, NUMBER_OF_WOMEN))

# 1.4 生成群体
men = dict()
for i in range(1, NUMBER_OF_MEN + 1):
    name = "".join(["m", str(i)])

    age = MEN_AGE.pop()
    if age < 25:
        age = 25
    if age > 40:
        age = 40

    edu = MEN_EDU.pop()
    if edu < 0:
        edu = 0
    if edu > 21:
        edu = 21

    men[name] = (age, edu)

women = dict()
for i in range(1, NUMBER_OF_WOMEN + 1):
    name = "".join(["w", str(i)])

    age = WOMEN_AGE.pop()
    if age < 25:
        age = 25
    if age > 40:
        age = 40

    edu = WOMEN_EDU.pop()
    if edu < 0:
        edu = 0
    if edu > 21:
        edu = 21

    women[name] = (age, edu)

# 1.5 生成偏好
man_age_weight = 0.4
man_edu_weight = 0.4
man_random_weight = 0.2
man_patient = 1

all_men = list()
for man_name in men:
    self_evaluation = float(- man_age_weight * (men[man_name][0] - 30) / 5 + man_edu_weight * (
                men[man_name][1] - 12) / 3 + man_random_weight * np.random.normal(0, 1, 1))

    score = [(woman_name, float(- man_age_weight * (women[woman_name][0] - 30) / 5 + man_edu_weight * (
                women[woman_name][1] - 10) / 2 + man_random_weight * np.random.normal(0, 1, 1)))
             for woman_name in women]

    score = [item for item in score if item[1] + man_patient >= self_evaluation]
    preference_list = [item[0] for item in sorted(score, key=lambda x: x[1], reverse=True)]
    all_men.append(Male(man_name, preference_list, age=men[man_name][0], edu=men[man_name][1]))

woman_age_weight = 0.4
woman_edu_weight = 0.4
woman_random_weight = 0.2
woman_patient = 0.5

all_women = list()
for woman_name in women:
    self_evaluation = float(- woman_age_weight * (women[woman_name][0] - 30) / 5 + woman_edu_weight * (
                women[woman_name][1] - 10) / 2 + woman_random_weight * np.random.normal(0, 1, 1))

    score = [(man_name, float(- woman_age_weight * (men[man_name][0] - 30) / 5 + woman_edu_weight * (
                men[man_name][1] - 12) / 3 + woman_random_weight * np.random.normal(0, 1, 1)))
             for man_name in men]

    score = [item for item in score if item[1] + woman_patient >= self_evaluation]
    preference_list = [item[0] for item in sorted(score, key=lambda x: x[1], reverse=True)]
    all_women.append(Female(woman_name, preference_list, age=women[woman_name][0], edu=women[woman_name][1]))

for man in all_men:
    print(man.name, man.preferences)

for woman in all_women:
    print(woman.name, woman.preferences)

## 3. 匹配
matcher = StableMatcher(men=all_men, women=all_women)
matcher.match()

## 4. 打印结果


