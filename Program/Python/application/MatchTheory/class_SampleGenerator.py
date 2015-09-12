# coding=UTF-8

import random
import re
from application.MatchTheory.class_Proposal import *

# 类PersonGenerator用来产生求婚者及被求婚者
class SampleGenerator:
    '''
    类SampleGenerator用来生成随机样本。
    
    属性：

    '''
    # 构造函数
    def __init__(self,numberofmale=0,numberofFemale=0):
        self.numberOfMale = numberofmale
        self.numberOfFemale = numberofFemale

        self.maleName = list(range(self.numberOfMale))
        self.femaleName = list(range(self.numberOfFemale))

        self.wealthOfMale = 0
        self.wealthOfFemale = 0

    # 生成样本集合
    def toSample(self,preference='random',ratio=0):
        sample = {}

        if re.match('^random$',preference) is not None:
            self._randomPreference()

        if re.match('^wealth$',preference) is not None:
            self._wealthPreference(ratio)

        proposeds = {key:Proposed(name=key,preference=self.preferenceOfFemale[key],wealth=self.wealthOfFemale[key]) for key in sorted(self.preferenceOfFemale)}
        proposals = {key:Proposal(name=key,preference=self.preferenceOfMale[key],wealth=self.wealthOfMale[key],roll=proposeds) for key in sorted(self.preferenceOfMale)}
        sample['men2women'] = {'proposeds':proposeds,'proposals':proposals}
        proposeds = {key:Proposed(name=key,preference=self.preferenceOfMale[key],wealth=self.wealthOfMale[key]) for key in sorted(self.preferenceOfMale)}
        proposals = {key:Proposal(name=key,preference=self.preferenceOfFemale[key],wealth=self.wealthOfFemale[key],roll=proposeds) for key in sorted(self.preferenceOfFemale)}
        sample['women2men'] = {'proposeds':proposeds,'proposals':proposals}

        return sample

    # 随机偏好生成器
    def _randomPreference(self):
        maleName = self.maleName[:]
        femaleName = self.femaleName[:]

        # 随机生成男性的偏好
        self.preferenceOfMale = {}
        for i in range(self.numberOfMale):
            random.shuffle(femaleName)
            self.preferenceOfMale[i] = femaleName[:]

        # 随机生成女性偏好
        self.preferenceOfFemale = {}
        for i in range(self.numberOfFemale):
            random.shuffle(maleName)
            self.preferenceOfFemale[i] = maleName[:]

    # 根据财富和随机偏好生成器，ratio表示随机偏好的人口比例
    def _wealthPreference(self,ratio=0):
        maleName = self.maleName[:]
        femaleName = self.femaleName[:]
        numOfMale = self.numberOfMale
        numOfFemale = self.numberOfFemale

        self.wealthOfMale = self.maleName[::-1]
        self.wealthOfFemale = self.femaleName[::-1]
        # random wealth distribution
        #wealthOfMale = random.shuffle(self.maleName)
        #wealthOfFemale = random.shuffle(self.femaleName)

        # 生成男性女性的初始偏好
        self.preferenceOfMale = {i:self.femaleName[:] for i in maleName}
        self.preferenceOfFemale = {i:self.maleName[:] for i in femaleName}

        if ratio > 0:
            radomNumOfMale = math.floor(ratio * numOfMale)
            radomNumOfFemale = math.floor(ratio * numOfFemale)
            #print('hello',maleName,numOfMale,radomNumOfMale)
            males = random.sample(maleName,radomNumOfMale)
            females = random.sample(femaleName,radomNumOfFemale)

            for i in males:
                random.shuffle(femaleName)
                self.preferenceOfMale[i] = femaleName[:]

            for i in females:
                random.shuffle(maleName)
                self.preferenceOfFemale[i] = maleName[:]


if __name__ == '__main__':
    generator = SampleGenerator(10,20)
    sample = generator.toSample()

    #print(sample)
    generator._wealthPreference(ratio=0.5)
    print(generator.preferenceOfMale)
    print(generator.preferenceOfFemale)
