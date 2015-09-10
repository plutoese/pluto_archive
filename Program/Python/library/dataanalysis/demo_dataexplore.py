# coding=UTF-8

def f1(args):
    print(args)

def f2(**args):
    print(args)
    f1(args)

f2(name='24',age=24)



