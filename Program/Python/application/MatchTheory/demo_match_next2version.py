# coding=UTF-8

import random
import numpy as np
from application.MatchTheory.class_Proposal import *
from library.imexport.class_Excel import *
from application.MatchTheory.class_SampleGenerator import *

# 1. to set up number
ratio_gini = []

for ratio in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
    # 男性数量
    N1 = 100
    # 女性数量
    N2 = 100

    RUN = 100
    result1 = []
    result2 = []
    for n in range(RUN):

        generator = SampleGenerator(N1,N2)
        sample = generator.toSample(preference='wealth',ratio=ratio)

        # 男性求婚
        proposeds = sample['men2women']['proposeds']
        proposals = sample['men2women']['proposals']

        match = Propose(proposals,proposeds)
        match.topropose()
        result1.append(match.stat)

    gini = np.array([item['gini'] for item in result1])
    mean_gini = gini.mean()
    ratio_gini.append([ratio,mean_gini])
    print(ratio_gini)

outfile = u'c:\\down\\demo4.xlsx'
moutexcel = Excel(outfile)
moutexcel.new()
moutexcel.append(ratio_gini)
moutexcel.close()