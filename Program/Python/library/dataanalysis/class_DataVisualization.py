# coding=UTF-8

from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 类DataVisualization用来数据可视化
class DataVisualization:
    # 构造函数
    def __init__(self):
        pass

    # 通用作图函数
    def plot(self,data,**kargs):
        data.plot(**kargs)
        plt.show()

if __name__ == '__main__':
    pass
    #print(rdata.data)
    #rdata.data.plot(x = rdata.data['region'],kind='barh')
    #plt.show()