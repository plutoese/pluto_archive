# coding = UTF-8

import sys
sys.path.append(r'E:\cyberspace\R\reticulate')

import random
from fun_sum import sumxy

def randomsum(x=random.randint(1,10),y=random.randint(1,10)):
    return sumxy(x,y)