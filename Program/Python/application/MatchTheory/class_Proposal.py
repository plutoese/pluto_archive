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
        self.denied = [self.proposal_list[key] for key in sorted(self.proposal_list)]

    def topropose(self):
        i = 0
        while len(self.denied) > 0:
            proposal = self.denied
            self.denied = []
            for person in proposal:
                if person is None:
                    continue
                person.next()
                if person.cursor is None:
                    continue
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
        for key in proposeds:
            if proposeds[key].accepted is not None:
                print(proposeds[key].name,' accept  ',proposeds[key].accepted.name)
            else:
                print(proposeds[key].name,' accept  ','None')
        print('--------------------------------')
        for key in proposals:
            if proposals[key].beAccepted is not None:
                print(proposals[key].name,' accepted by  ',proposals[key].beAccepted)
            else:
                print(proposals[key].name,' accepted by  ','None')
        print('--------------------------------')

    # assist function to find a proposed object
    def findInProposed(self,obj):
        #result = [item for item in self.proposed_list if obj.name==item.name]
        if obj.name in self.proposed_list:
            result = self.proposed_list[obj.name]
            return result
        else:
            return None
        #if len(result) < 1:
        #    return None
        #else:
        #    return result[0]

# 类Person代表个体
class Person:
    ''' 
    类Person表示个体，个体有两个属性：name和preference
    属性name表示个体的姓名，类型str
    属性preference表示个体的偏好，类型list，偏好的元素是对象的名字，即name

    方法index，输入参数为对象名字，返回该对象的偏好次序
    '''
    def __init__(self,name=None,preference=None):
        self.preference = preference
        self.preference_order = dict(zip(self.preference,range(len(self.preference))))
        self.name = name

    # index函数返回某个对象的偏好次序
    # 参数为对象的名字
    def index(self,objname):
        if objname in self.preference:
            return self.preference_order[objname]
        else:
            return None

# 类Proposal代表求婚者
class Proposal(Person):
    '''
    类Proposal是求婚者，它是Person的子类。

    属性：
    rest_object：表示剩余的偏好集，类型list
    self.preference_order: 偏好次序，类型字典
    self.denied：表示是否被拒绝的指示变量，类型布尔值
    self.beAccepted：表示被哪个对象接受，类型Person类
    self.cursor：表示当前求婚的对象，类型Person类

    方法：
    next(self)：弹出下一个求婚对象（也就是偏好次序中下一个对象），如果偏好集中还有对象，返回下一个求婚对象，类型Person类，不然返回None。
    toPropose(self,proposed)：对某个对象proposed求婚，如果求婚被接受，设置状态denied为False，beAccepted为被求婚对象；否则设置denied状态为True。
    '''
    '''A proposal'''
    def __init__(self,name=None,preference=None,roll=None):
        super().__init__(name,preference)

        # 余下的偏好集
        self.roll = roll
        self.preferenceobj = [self.roll[name] for name in self.preference]
        self.rest_object = self.preferenceobj
        self.denied = True
        self.beAccepted = None
        self.cursor = None

    # next函数用来弹出一个下一个偏好
    def next(self):
        # 如果余下的偏好集中没有任何个体，那么返回None；不然设置当前的游标self.cursor为弹出的偏好（即对象），并返回当前偏好
        if len(self.rest_object) > 0:
            self.cursor = self.rest_object.pop(0)
            return self.cursor
        else:
            self.cursor = None
            return None

    # toPropose函数用来求婚
    # 参数proposed代表被求婚的对象
    def toPropose(self,proposed):
        # 如果求婚成功，那么设置状态self.denied为False，self.beAccepted为求婚对象（Person类）；如果求婚失败，那么设置self.denied为True
        if proposed.isAccepted(self) is True:
            self.denied = False
            self.beAccepted = proposed
        else:
            self.denied = True

    def __repr__(self):
        pattern = '{0}:current({1});acceptedby({2}).'
        return pattern.format(self.name,self.cursor.name,self.beAccepted.name)

# 类Proposed表示被求婚对象，它同样是Person的子类
class Proposed(Person):
    '''
    类Proposed表示被求婚对象。

    属性：
    accept：表示接受的求婚者。
    '''
    def __init__(self,name=None,preference=None):
        super().__init__(name,preference)
        self.accepted = None

    # 检验是否接受某个对象的求婚
    # 流程：首先看求婚者是否在自己的偏好中，如果没有，则拒绝。如果有，进行下一步。
    #       如果之前没有成功的求婚者，那么接受当前求婚者。
    #       如果之前有成功的求婚者，那么比较当前求婚者和已接受的求婚者两者在自己偏好集中的顺序，如果当前者更靠前，接受当前者；否则，维持原状。
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
            proposal.beAccepted = self
        else:
            proposal.beAccepted = None
            rejected = proposal
        return rejected

    def __repr__(self):
        pattern = "{0} accept {1}"
        return pattern.format(self.name,self.accepted)

if __name__ == '__main__':
    preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    #preference_male = {0: [1, 2, 4, 0, 3], 1: [4, 1, 3, 0, 2], 2: [2, 3, 4, 0, 1], 3: [2, 3, 0, 1, 4], 4: [3, 0, 1, 4, 2]}
    #preference_female = {0: [2, 4, 1, 3, 0], 1: [4, 1, 3, 0, 2], 2: [1, 4, 0, 3, 2], 3: [0, 4, 1, 2, 3], 4: [2, 3, 1, 4, 0]}

    #preference_female = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    #preference_male = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    #preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    #preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}
    proposeds = {key:Proposed(name=key,preference=preference_female[key]) for key in sorted(preference_female)}
    proposals = {key:Proposal(name=key,preference=preference_male[key],roll=proposeds) for key in sorted(preference_male)}

    match = Propose(proposals,proposeds)
    match.topropose()
    match.print()

    match.printTest()

