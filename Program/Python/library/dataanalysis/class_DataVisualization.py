# coding=UTF-8

import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 类DataVisualization用来数据可视化
class DataVisualization:
    # 构造函数
    def __init__(self,data=None):
        self.data = data

    # 通用作图函数
    def plot(self,kargs):
        '''
        if sort is not None:
            self.data.sort(sort).plot(args)
        else:
            self.data.plot(args)'''
        print(kargs)
        self.data.plot(kargs)
        #self.data.plot(kind='barh')
        plt.show()

if __name__ == '__main__':
    pass