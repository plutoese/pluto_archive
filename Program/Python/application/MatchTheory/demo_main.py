# coding=UTF-8

import random
from application.MatchTheory.class_Proposal import *

# 1. to set up number
N = 100
person = list(range(N))

preference_male = {}
for i in range(N):
    random.shuffle(person)
    preference_male[i] = person[:]

preference_female = {}
for i in range(N):
    random.shuffle(person)
    preference_female[i] = person[:]

print(preference_male,preference_female)

proposeds = {key:Proposed(name=key,preference=preference_female[key]) for key in sorted(preference_female)}
proposals = {key:Proposal(name=key,preference=preference_male[key],roll=proposeds) for key in sorted(preference_male)}

match = Propose(proposals,proposeds)
match.topropose()
match.print()

