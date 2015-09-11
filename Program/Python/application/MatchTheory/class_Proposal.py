# coding=UTF-8

import math

# 类Propose表示求婚
class Propose:
    '''
    类Propose用来模拟求婚过程。
    
    属性：
    self.proposal_dict：求婚者的集合，类型Person对象的字典
    self.proposed_dict：被求婚者的集合，类型Person对象的字典
    self.denied：被拒绝的求婚者的列表，初始值为所有的求婚者的列表
    '''
    def __init__(self,proposaldict=None,proposeddict=None):
        # who propose
        self.proposal_dict = proposaldict
        # who to be proposed
        self.proposed_dict = proposeddict

        # number of proposal
        self.numberofproposal = len(self.proposal_dict)
        # number of proposed
        self.numberofproposed = len(self.proposed_dict)

        # initial denied list
        self.denied = [self.proposal_dict[key] for key in sorted(self.proposal_dict)]

    # 方法topropose用来模拟求婚过程
    def topropose(self):
        # 变量i记录求婚过程进行了多少轮
        i = 0
        # 如果被拒绝的名单里还有人，就继续进行求婚过程
        while len(self.denied) > 0:
            # 赋值求婚者就是上轮被拒绝的Proposal对象
            proposal = self.denied
            # 清空上一轮的被拒绝者，等待新一轮加入新的被拒绝者
            self.denied = []
            # 依次对每个求婚者进行求婚过程
            for person in proposal:
                # 如果求婚者是None，那么下一个求婚者继续
                if person is None:
                    continue
                # 当前求婚者弹出一个求婚对象，即赋值求婚对象给person.cursor
                person.next()
                # 如果该求婚者没有求婚对象了，那么下一个求婚者继续
                if person.cursor is None:
                    continue
                beproposed = person.cursor
                self.denied.append(beproposed.update(person))
                #print(self.proposed_list)
            i = i + 1
            #print(i)

    # 输出最终的结果
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
        #print('hello',self.proposal_dict)
        #print('hello',self.proposed_dict)
        for key in self.proposed_dict:
            if self.proposed_dict[key].accepted is not None:
                print(self.proposed_dict[key].name,' accept  ',self.proposed_dict[key].accepted.name)
            else:
                print(self.proposed_dict[key].name,' accept  ','None')
        print('--------------------------------')
        for key in self.proposal_dict:
            if self.proposal_dict[key].beAccepted is not None:
                print(self.proposal_dict[key].name,' accepted by  ',self.proposal_dict[key].beAccepted.name)
            else:
                print(self.proposal_dict[key].name,' accepted by  ','None')
        print('--------------------------------')

    # assist function to find a proposed object
    def findInProposed(self,obj):
        #result = [item for item in self.proposed_list if obj.name==item.name]
        if obj.name in self.proposed_dict:
            result = self.proposed_dict[obj.name]
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
    self.preferenceobj：偏好集合，类型是Person对象的列表
    self.denied：表示是否被拒绝的指示变量，类型布尔值
    self.beAccepted：表示被哪个对象接受，类型Person类
    self.cursor：表示当前求婚的对象，类型Person类

    方法：
    构造函数：初始化求婚者的偏好集，以及状态。和被求婚者不同的在于，它包含一个属性preferenceobj。
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
        pattern = "{0} is accepted by {1}"
        return pattern.format(self.name,self.beAccepted.name)
        #pattern = '{0}:current({1});acceptedby({2}).'
        #return pattern.format(self.name,self.cursor.name,self.beAccepted.name)

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

    # 方法update是被求婚者对求婚者的一次更新，并且返回被拒绝者
    def update(self,proposal):
        rejected = None
        # 如果被求婚者接受了当前求婚者
        if self.isAccepted(proposal):
            # 那么拒绝者就成了之前被接受的人
            rejected = self.accepted
            # 被接受的人就是当前的求婚者
            self.accepted = proposal
            # 同时更新求婚者的状态，即他的属性beAccepted变成了当前被求婚者
            proposal.beAccepted = self
        else:
            # 如果被求婚者拒绝了当前求婚者，设置当前求婚者的属性beAccepted为None
            proposal.beAccepted = None
            # 被拒绝者就是当前的求婚者
            rejected = proposal
        return rejected

    # 打印当前对象
    def __repr__(self):
        pattern = "{0} accept {1}"
        return pattern.format(self.name,self.accepted.name)

if __name__ == '__main__':
    preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    preference_male = {0: [1, 2, 4, 0, 3], 1: [4, 1, 3, 0, 2], 2: [2, 3, 4, 0, 1], 3: [2, 3, 0, 1, 4], 4: [3, 0, 1, 4, 2]}
    preference_female = {0: [2, 4, 1, 3, 0], 1: [4, 1, 3, 0, 2], 2: [1, 4, 0, 3, 2], 3: [0, 4, 1, 2, 3], 4: [2, 3, 1, 4, 0]}

    preference_female = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_male = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    preference_male = {0:[0,1,2,3],1:[3,1,2,0],2:[3,2,0,1],3:[0,3,2,1],4:[0,1,3]}
    preference_female = {0:[1,2,0,3,4],1:[2,0,1,3,4],2:[4,3,0,1,2],3:[0,3,4,1,2]}

    proposeds = {key:Proposed(name=key,preference=preference_female[key]) for key in sorted(preference_female)}
    proposals = {key:Proposal(name=key,preference=preference_male[key],roll=proposeds) for key in sorted(preference_male)}

    match = Propose(proposals,proposeds)
    match.topropose()
    match.print()

    #match.printTest()

