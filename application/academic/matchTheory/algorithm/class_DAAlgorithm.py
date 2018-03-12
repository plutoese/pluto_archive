# coding = UTF-8

"""
=========================================
匹配理论的DA(deferred acceptance)算法
=========================================

:Author: glen
:Date: 2018.03.12
:Tags: deferred acceptance match algorithm
:abstract: DA algorithm of Gale and Shapley(1962)
:source: Roth, A.E. and Sotomayor, M.A.O. (1990). Two-sided matching: a study in game-theoretic modeling and analysis, Econometric Society Monographs, Vol. 18 (Cambridge University Press).

**类**
==================
Individual
    个体基类
Male
    男性类
Female
    女性类
StableMatcher
    匹配类

**使用方法**
==================
无
"""

from collections import deque

class Individual:
    """个体基类
    :param str name: 名称
    :param list preferences: 偏好
    """
    def __init__(self, name, preferences):
        #名称
        self.name = name
        #偏好
        self.preferences = preferences
        #匹配结果
        self.matched = None

    def __repr__(self):
        fmt = '{type} {name} matched {someone}'
        return fmt.format(type=self.__class__.__name__, name=self.name, someone=self.matched.__repr__())


class Male(Individual):
    """男性类
    :param str name: 名称
    :param list preferences: 偏好
    """
    def __init__(self, name, preferences):
        super().__init__(name=name, preferences=preferences)
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


class Female(Individual):
    """女性类
    :param str name: 名称
    :param list preferences: 偏好
    """
    def __init__(self, name, preferences):
        super().__init__(name=name, preferences=preferences)
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
        proposal_dict = {self.preferences.index(man.name):man.name for man in self._be_prosoed_by}
        # 获得求婚者的姓名
        accepted = proposal_dict[sorted(proposal_dict)[0]]
        return accepted

    def __repr__(self):
        fmt = '{type} {name} matched {someone}'
        if self._accept is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone=self._accept.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name, someone='None')


class StableMatcher:
    def __init__(self, men=None, women=None):
        self._men = men
        self._women = women

        self._men_mapping = {man.name:man for man in self._men}
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

if __name__ == '__main__':

    men = [Male('m1', ['w2', 'w1', 'w3']),
           Male('m2', ['w1', 'w3', 'w2']),
           Male('m3', ['w1', 'w2', 'w3'])]
    women = [Female('w1', ['m1', 'm3', 'm2']),
             Female('w2', ['m3', 'm1', 'm2']),
             Female('w3', ['m1', 'm3', 'm2']),]

    '''
    men = [Male('m1', ['w1', 'w2', 'w3', 'w4']),
           Male('m2', ['w4', 'w2', 'w3', 'w1']),
           Male('m3', ['w4', 'w3', 'w1', 'w2']),
           Male('m4', ['w1', 'w4', 'w3', 'w2']),
           Male('m5', ['w1', 'w2', 'w4'])]
    women = [Female('w1', ['m2', 'm3', 'm1', 'm4', 'm5']),
             Female('w2', ['m3', 'm1', 'm2', 'm4', 'm5']),
             Female('w3', ['m5', 'm4', 'm1', 'm2', 'm3']),
             Female('w4', ['m1', 'm4', 'm5', 'm2', 'm3'])]'''

    matcher = StableMatcher(men=men, women=women)
    matcher.match()