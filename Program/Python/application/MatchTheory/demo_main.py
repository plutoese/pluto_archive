# coding=UTF-8

import random
from application.MatchTheory.class_Proposal import *

# 1. to set up number
N1 = 100
N2 = 100
person1 = list(range(N1))
person2 = list(range(N2))

# 随机生成男性的偏好
preference_male = {}
for i in range(N1):
    random.shuffle(person2)
    preference_male[i] = person2[:]

preference_female = {}
for i in range(N2):
    random.shuffle(person1)
    preference_female[i] = person1[:]

print(preference_male,preference_female)

proposeds = {key:Proposed(name=key,preference=preference_female[key]) for key in sorted(preference_female)}
proposals = {key:Proposal(name=key,preference=preference_male[key],roll=proposeds) for key in sorted(preference_male)}

match = Propose(proposals,proposeds)
match.topropose()
match.print()
print(match.stat)

