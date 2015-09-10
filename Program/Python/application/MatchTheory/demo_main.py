# coding=UTF-8

import random
from application.MatchTheory.class_Match import *

# 1. to set up number
N = 10
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

proposals = proposalList(preference_female)
proposeds = proposedList(preference_male)

match = Propose(proposals,proposeds)
match.topropose()
match.print()

match.printTest()