# coding=UTF-8

from sklearn import datasets
from sklearn import tree

def f1(name,age):
    print(name,age)

def f2(**args):
    x = args
    f1(**x)

f2(name='24',age=24)

X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
print(clf.predict([[0.5, 0.4]]))







