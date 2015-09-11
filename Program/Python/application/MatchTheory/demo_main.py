# coding=UTF-8

import random
import numpy as np
from application.MatchTheory.class_Proposal import *

# 1. to set up number
# 男性数量
N1 = 20
# 女性数量
N2 = 40

RUN = 100
result1 = []
result2 = []
for n in range(RUN):

    person1 = list(range(N1))
    person2 = list(range(N2))

    # 随机生成男性的偏好
    preference_male = {}
    for i in range(N1):
        random.shuffle(person2)
        preference_male[i] = person2[:]

    # 随机生成女性偏好
    preference_female = {}
    for i in range(N2):
        random.shuffle(person1)
        preference_female[i] = person1[:]

    print(preference_male,preference_female)

    # 男性求婚
    proposeds = {key:Proposed(name=key,preference=preference_female[key]) for key in sorted(preference_female)}
    proposals = {key:Proposal(name=key,preference=preference_male[key],roll=proposeds) for key in sorted(preference_male)}

    match = Propose(proposals,proposeds)
    match.topropose()
    result1.append(match.stat)

    # 女性求婚
    proposeds = {key:Proposed(name=key,preference=preference_male[key]) for key in sorted(preference_male)}
    proposals = {key:Proposal(name=key,preference=preference_female[key],roll=proposeds) for key in sorted(preference_female)}

    match = Propose(proposals,proposeds)
    match.topropose()
    result2.append(match.stat)

# 当男性求婚时
positionofproposal = np.array([item['positionofproposal'] for item in result1])
mean_positionofproposal = positionofproposal.mean()
# 男性求婚者选择的女性在偏好中的平均次序
print(mean_positionofproposal)
positionofproposed = np.array([item['positionofproposed'] for item in result1])
mean_positionofproposed = positionofproposed.mean()
print(mean_positionofproposed)

# 当女性求婚时
positionofproposal = np.array([item['positionofproposal'] for item in result2])
mean_positionofproposal = positionofproposal.mean()
print(mean_positionofproposal)
# 男性被求婚者的女性在偏好中的平均次序
positionofproposed = np.array([item['positionofproposed'] for item in result2])
mean_positionofproposed = positionofproposed.mean()
print(mean_positionofproposed)
