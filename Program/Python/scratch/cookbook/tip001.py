# coding=UTF-8

from functools import reduce

# 递归编程
def mysum(L):
    first, *rest = L
    return first if not rest else first + mysum(rest)

print(mysum([1,2,3,4,5]))

def sumtree(L):
    tot = 0
    for x in L:
        if not isinstance(x,list):
            tot += x
        else:
            tot += sumtree(x)
    return tot

print(sumtree([1,[2,3,4],[5,[6,7]]]))

# Indirect Function Calls
def indirect(func, arg):
    func(arg)

indirect(print,'hello')

# 函数注释
def func(a: 'spam' = 4, b: (1, 10) = 5, c: float = 6) -> int:
    return a + b + c
print(func())

# 多重选择的lambda应用
key = 'got'
choice = {'already': (lambda: 2 + 2), 'got': (lambda: 2 * 4), 'one': (lambda: 2 ** 6)}[key]()
print(choice)

lower = (lambda x, y: x if x < y else y)
print(lower('bb', 'aa'))

# Selecting Items in Iterables: filter
print(list(filter((lambda x: x > 0), range(-5, 5))))

# Combining Items in Iterables: reduce
print(reduce((lambda x, y: x * y), [1, 2, 3, 4]))

# Coding Properties with Decorators
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self): # name = property(name)
        "name property docs"
        print('fetch...')
        return self._name

    @name.setter
    def name(self, value): # name = name.setter(name)
        print('change...')
        self._name = value

    @name.deleter
    def name(self): # name = name.deleter(name)
        print('remove...')
        del self._name

bob = Person('Bob Smith') # bob has a managed attribute
print(bob.name) # Runs name getter (name 1)
bob.name = 'Robert Smith' # Runs name setter (name 2)
print(bob.name)
del bob.name # Runs name deleter (name 3)
print('-'*20)
sue = Person('Sue Jones') # sue inherits property too
print(sue.name)
print(Person.name.__doc__) # Or help(Person.name)

# Decorators
# In short, decorators provide a way to insert automatically run code at the end of function
# and class definition statements
class tracer:
    def __init__(self, func): # On @ decoration: save original func
        self.calls = 0
        self.func = func

    def __call__(self, *args): # On later calls: run original func
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        self.func(*args)
@tracer
def spam(a, b, c): # spam = tracer(spam)
    print(a + b + c) # Wraps spam in a decorator object

spam(1, 2, 3)






























