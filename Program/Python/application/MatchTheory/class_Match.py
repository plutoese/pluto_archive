# coding=UTF-8

import math

class Propose:
    '''An algorithm to match'''
    def __init__(self,proposal_list=None,proposed_list=None):
        # who propose
        self.proposal_list = proposal_list
        # who to be proposed
        self.proposed_list = proposed_list

        # number of proposal
        self.numberofproposal = len(self.proposal_list)
        # number of proposed
        self.numberofproposed = len(self.proposed_list)

        # initial denied list
        self.denied = self.proposal_list

    def topropose(self):
        i = 0
        while len(self.denied) > 0:
            proposal = self.denied
            self.denied = []
            for person in proposal:
                if person is None:
                    continue
                person.next()
                beproposed = self.findInProposed(person.cursor)
                if beproposed is None:
                    continue
                #print('beprosed',beproposed)
                self.denied.append(beproposed.update(person))
                #print(self.proposed_list)
            i = i + 1
            #print(i)

    def printTest(self):
        proposalc = [item.index(item.beAccepted)+1 for item in proposals if item.beAccepted is not None]
        proposedc = [item.index(item.accepted.name)+1 for item in proposeds if item.accepted is not None]

        singleofproposal = len(proposalc)/self.numberofproposal
        singleofproposed = len(proposedc)/self.numberofproposed
        singleoftotal = (len(proposedc) + len(proposalc)) / (self.numberofproposal + self.numberofproposed)
        print(100*singleofproposal)
        print(100*singleofproposed)
        print(100*singleoftotal)

        positionofproposal = float(sum(proposalc)/len(proposalc))
        positionofproposed = float(sum(proposedc)/len(proposedc))
        positionoftotal = float((sum(proposalc) + sum(proposedc))/((len(proposalc) + len(proposedc))))
        print(positionofproposal)
        print(positionofproposed)
        print(positionoftotal)

    def print(self):
        print('result:--------------------------------')
        print('hello',proposeds)
        for item in proposeds:
            if item.accepted is not None:
                print(item.name,' accept  ',item.accepted.name)
            else:
                print(item.name,' accept  ','None')
        print('--------------------------------')
        for item in proposals:
            if item.beAccepted is not None:
                print(item.name,' accepted by  ',item.beAccepted)
            else:
                print(item.name,' accepted by  ','None')
        print('--------------------------------')

    # assist function to find a proposed object
    def findInProposed(self,name):
        result = [item for item in self.proposed_list if name==item.name]
        if len(result) < 1:
            return None
        else:
            return result[0]

class Person:
    ''' A person'''
    def __init__(self,name=None,preference=None):
        self.preference = preference
        self.name = name

class Proposal(Person):
    '''A proposal'''
    def __init__(self,name=None,preference=None):
        super().__init__(name,preference)
        self.rest_object = self.preference[:]
        self.preference_order = dict(zip(self.preference,range(len(self.preference))))
        self.denied = True
        self.beAccepted = None
        self.cursor = None

    # to pop a preference
    def next(self):
        if len(self.rest_object) > 0:
            self.cursor = self.rest_object.pop(0)
            return self.cursor
        else:
            self.cursor = None
            return None

    # to propose
    def toPropose(self,proposed):
        if proposed.isAccepted(self) is True:
            self.denied = False
            self.beAccepted = proposed
        else:
            self.denied = True

    # to find out the order of a object
    def index(self,obj):
        if obj in self.preference:
            return self.preference_order[obj]
        else:
            return None

    def __repr__(self):
        pattern = '{0}:current({1});acceptedby({2}).'
        return pattern.format(self.name,self.cursor,self.beAccepted)

class Proposed(Person):
    '''A proposed'''
    def __init__(self,name=None,preference=None):
        super().__init__(name,preference)
        self.preference_order = dict(zip(self.preference,range(len(self.preference))))
        self.accepted = None

    # to find out the order of a object
    def index(self,obj):
        if obj in self.preference:
            return self.preference_order[obj]
        else:
            return None

    # to accecpt a proposal
    def isAccepted(self,proposal):
        if self.index(proposal.name) is None:
            return False
        if self.accepted is None:
            return True
        else:
            if self.index(self.accepted.name) < self.index(proposal.name):
                return False
            else:
                return True

    # to accept who and reject who
    def update(self,proposal):
        rejected = None
        if self.isAccepted(proposal):
            rejected = self.accepted
            self.accepted = proposal
            proposal.beAccepted = self.name
        else:
            proposal.beAccepted = None
            rejected = proposal
        return rejected

    def __repr__(self):
        pattern = "{0} accept {1}"
        return pattern.format(self.name,self.accepted)

def proposalList(adict):
    personlist = []
    for key in sorted(adict):
        aperson = Proposal(name=key,preference=adict[key])
        personlist.append(aperson)
    return personlist

def proposedList(adict):
    personlist = []
    for key in sorted(adict):
        aperson = Proposed(name=key,preference=adict[key])
        personlist.append(aperson)
    return personlist

if __name__ == '__main__':




    preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    #preference_male = {0: [1, 2, 4, 0, 3], 1: [4, 1, 3, 0, 2], 2: [2, 3, 4, 0, 1], 3: [2, 3, 0, 1, 4], 4: [3, 0, 1, 4, 2]}
    #preference_female = {0: [2, 4, 1, 3, 0], 1: [4, 1, 3, 0, 2], 2: [1, 4, 0, 3, 2], 3: [0, 4, 1, 2, 3], 4: [2, 3, 1, 4, 0]}

    #preference_female = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    #preference_male = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    proposals = proposalList(preference_female)
    proposeds = proposedList(preference_male)

    match = Propose(proposals,proposeds)
    match.topropose()
    match.print()

    match.printTest()

























