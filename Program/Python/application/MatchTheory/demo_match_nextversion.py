# coding=UTF-8

import random
import numpy as np
from application.MatchTheory.class_Proposal import *
from library.imexport.class_Excel import *
from application.MatchTheory.class_SampleGenerator import *

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

    RUN = 10
    result1 = []
    result2 = []
    for n in range(RUN):

        generator = SampleGenerator(N1,N2)
        sample = generator.toSample(preference='wealth',ratio=0)

        # 男性求婚
        proposeds = sample['men2women']['proposeds']
        proposals = sample['men2women']['proposals']

        match = Propose(proposals,proposeds)
        match.topropose()
        result1.append(match.stat)

        # 男性求婚
        proposeds = sample['women2men']['proposeds']
        proposals = sample['women2men']['proposals']

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

outfile = u'c:\\down\\demo3.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(mdata)
moutexcel.close()