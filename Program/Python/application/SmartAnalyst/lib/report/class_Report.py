# coding=UTF-8

#-----------------------------------------------------------------------------------
# class_Report文件
# @class: Report类
# @introduction: Report类是用来处理和生成报告
# @dependency: pylatex包，datatime包，collections包，matplotlib包
# @author: plutoese
# @date: 2015.10.18
#-----------------------------------------------------------------------------------

'''
.. code-block:: python

    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]
    plt.plot(x, y)
    report = Report(title='数据分析报表',author='冥王星人')
    report.create_section('地球和月球')
    report.create_subsection('地球往事')
    report.create_section('地球和月球2')
    report.add_text('这是为你写的歌。')
    report.create_subsection('地球往事2')
    report.add_matplotlib_graph(plt,caption='有趣的图形2')
    report.create_section('冥王星')
    report.add_text('欢迎来到地球。')
    report.add_figure('D:/Temp/glen.jpg')
    report.add_list(['你们','我们'])
    tdata = [[1,2,3,4],[5,6,7,8]]
    report.add_table([['变量', '第一产业占GDP的比重\_全市', '第一产业占GDP的比重\_市辖区','我错了'],[1,2,3,4],[5,6,7,8]],3,4)
    tdata = {'data': [['变量', '第二产业占GDP的比重全市', '第二产业占GDP的比重市辖区'], ['count', '284.00', '284.00'], ['mean', '50.94', '51.15'], ['std', '9.90', '11.69'], ['min', '17.48', '15.72'], ['25%', '45.27', '44.12'], ['50\%', '51.44', '51.05'], ['75\%', '56.61', '58.94'], ['max', '79.36', '82.23']], 'nrow': 9, 'ncol': 3}
    report.add_table(tdata['data'],tdata['nrow'],tdata['ncol'])
    report.create_section('结束语')
    report.add_text('')
    report.flush()
    report.generate_pdf('e:/Report/first_report.pdf')
'''

from pylatex.command import Command
from pylatex import Document, Section, Subsection, Subsubsection, Package
from pylatex.graphics import Figure
from pylatex.lists import Itemize, Enumerate, Description
from pylatex.table import Tabular, MultiColumn
from pylatex.utils import escape_latex
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt

class Report:
    '''类Report是用来处理和生成报告

    :param str title: 标题
    :param str author: 作者
    :param str date: 日期
    '''
    def __init__(self,title=None,author=None,date=None):
        # 初始化
        self.doc = Document()

        # 载入中文ctex包
        self.doc.packages.append(Package('ctex',options=['UTF8','noindent']))
        self.doc.packages.append(Package('geometry', options=['tmargin=1cm','lmargin=2cm']))

        # 设置标题，作者和日期
        if title is not None:
            self.doc.preamble.append(Command('title', title))
        if author is not None:
            self.doc.preamble.append(Command('author', author))
        if date is not None:
            self.doc.preamble.append(Command('date', date))
        self.doc.append(r'\maketitle')

        # 设置现在的章节
        self.presentSection = deque()

        # 初始化章节内容
        self.content = []

    def flush(self,level=0):
        '''输出内容和章节

        :param int level: 输出层级
        :return: 无返回值
        '''
        if len(self.content) < 1:
            return
        if len(self.presentSection) < 1:
            if len(self.content) > 0:
                for item in self.content:
                    self.doc.append(item)
        else:
            last = self.presentSection.pop()
            if len(self.content) > 0:
                for item in self.content:
                    last.append(item)
                self.content = []

            if len(self.presentSection) > level:
                for item in range(level,len(self.presentSection)):
                    current = self.presentSection.pop()
                    current.append(last)
                    last = current

            if level == 0:
                self.doc.append(last)
            else:
                self.presentSection[level-1].append(last)

    def create_section(self,title):
        '''创建一级章节

        :param str title: 章节题目
        :return: 无返回值
        '''
        self.flush(0)
        self.section = Section(title)
        self.presentSection.append(self.section)

    def create_subsection(self,title):
        '''创建二级章节

        :param str title: 章节题目
        :return: 无返回值
        '''
        self.flush(1)
        self.subsection = Subsection(title)
        self.presentSection.append(self.subsection)

    def create_subsubsection(self,title):
        '''创建三级级章节

        :param str title: 章节题目
        :return: 无返回值
        '''
        self.flush(2)
        self.subsubsection = Subsubsection(title)
        self.presentSection.append(self.subsubsection)

    def add_text(self,text):
        '''添加文本内容

        :param str text: 文本
        :return: 无返回值
        '''
        self.content.append(text)

    def add_list(self,lists,type=1):
        '''添加列表

        :param list lists: 列表内容
        :param int type: 列表类型，取值分别为1,2,3
        :return: 无返回值
        '''
        if type == 1:
            items = Itemize()
        if type == 2:
            items = Enumerate()
        if type == 3:
            items = Description()
        for item in lists:
            items.add_item(item)

        self.content.append(items)

    def add_table(self, data=None,nrow=None,ncol=None):
        '''添加表格

        :param data: 表格数据
        :param nrow: 表格行数
        :param ncol: 表格列数
        :return: 无返回值
        '''
        tabsize = '|' + '|'.join(['c']*ncol) + '|'
        mtable = Tabular(tabsize)
        for i in range(nrow):
            mtable.add_hline()
            mtable.add_row(tuple([escape_latex(str(item)) for item in data[i]]))
        mtable.add_hline()
        self.content.append(Command('begin',arguments='center'))
        self.content.append(mtable)
        self.content.append(Command('end',arguments='center'))

    def add_figure(self,file=None,caption=None,width='240px'):
        '''添加图片

        :param str file: 图片文件
        :param str caption: 图片标题
        :param str width: 图片宽度
        :return: 无返回值
        '''
        graph = Figure(position='h!')
        #graph = Figure()
        graph.add_image(file, width=width)
        if caption is not None:
            graph.add_caption(caption)
        self.content.append(graph)

    def add_matplotlib_graph(self,plt,filepath='E:/Report/',caption=None):
        '''添加matplotlib图片

        :param matplotlib.pyplot plt: matplotlib.pyplot句柄
        :param filepath: 保存图片的地址
        :param caption: 图片标题
        :return: 无返回值
        '''
        x = str(int(datetime.now().timestamp()*1000))
        filename = filepath + 'graph/' + x + '.pdf'
        plt.savefig(filename)
        self.add_figure(filename)

    def generate_pdf(self,file=''):
        '''生成pdf文件

        :param str file: 文件名
        :return: 无返回值
        '''
        self.doc.generate_pdf(filepath=file)


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]
    plt.plot(x, y)
    report = Report(title='数据分析报表',author='冥王星人')
    report.create_section('地球和月球')
    report.create_subsection('地球往事')
    report.create_section('地球和月球2')
    report.add_text('这是为你写的歌。')
    report.create_subsection('地球往事2')
    report.add_matplotlib_graph(plt,caption='有趣的图形2')
    report.create_section('冥王星')
    report.add_text('欢迎来到地球。')
    report.add_figure('D:/Temp/glen.jpg')
    report.add_list(['你们','我们'])
    tdata = [[1,2,3,4],[5,6,7,8]]
    report.add_table([['变量', '第一产业占GDP的比重\_全市', '第一产业占GDP的比重\_市辖区','我错了'],[1,2,3,4],[5,6,7,8]],3,4)
    tdata = {'data': [['变量', '第二产业占GDP的比重全市', '第二产业占GDP的比重市辖区'], ['count', '284.00', '284.00'], ['mean', '50.94', '51.15'], ['std', '9.90', '11.69'], ['min', '17.48', '15.72'], ['25%', '45.27', '44.12'], ['50\%', '51.44', '51.05'], ['75\%', '56.61', '58.94'], ['max', '79.36', '82.23']], 'nrow': 9, 'ncol': 3}
    report.add_table(tdata['data'],tdata['nrow'],tdata['ncol'])
    report.create_section('结束语')
    report.add_text('')
    report.flush()
    report.generate_pdf('e:/Report/first_report.pdf')

















