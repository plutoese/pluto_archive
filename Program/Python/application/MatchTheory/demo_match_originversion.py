# coding=UTF-8

import random
import numpy as np
from application.MatchTheory.class_Proposal import *
from library.imexport.class_Excel import *

# 1. to set up number
man_rank_woman_pbyman = []
woman_rank_man_pbyman = []
man_rank_woman_pbywoman = []
woman_rank_man_pbywoman = []

for NUM in range(20,61):
    # 男性数量
    N1 = NUM
    # 女性数量
    N2 = 40

    RUN = 1000
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

    positionofproposal = np.array([item['positionofproposal'] for item in result1])
    mean_positionofproposal = positionofproposal.mean()
    man_rank_woman_pbyman.append([NUM,mean_positionofproposal])
    print(mean_positionofproposal)

    positionofproposed = np.array([item['positionofproposed'] for item in result1])
    mean_positionofproposed = positionofproposed.mean()
    woman_rank_man_pbyman.append([NUM,mean_positionofproposed])
    print(mean_positionofproposed)

    positionofproposal = np.array([item['positionofproposal'] for item in result2])
    mean_positionofproposal = positionofproposal.mean()
    woman_rank_man_pbywoman.append([NUM,mean_positionofproposal])
    print(mean_positionofproposal)

    positionofproposed = np.array([item['positionofproposed'] for item in result2])
    mean_positionofproposed = positionofproposed.mean()
    man_rank_woman_pbywoman.append([NUM,mean_positionofproposed])
    print(mean_positionofproposed)

mdata = man_rank_woman_pbyman
for i in range(len(mdata)):
    mdata[i].append(woman_rank_man_pbyman[i][1])
    mdata[i].append(man_rank_woman_pbywoman[i][1])
    mdata[i].append(woman_rank_man_pbywoman[i][1])
print(man_rank_woman_pbyman)
print(man_rank_woman_pbywoman)
print(mdata)

outfile = u'c:\\down\\demo.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(mdata)
moutexcel.close()