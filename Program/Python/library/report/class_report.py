# coding=UTF-8

# -----------------------------------------------------------------------------------------
# @author: plutoese
# @date: 2015.10.12
# @class: Report
# @introduction: 类Report用来生成报告。
# @property:
# - period: 数据库覆盖的年份
# @method:
# - find(self,**conds)：查询数据，参数conds是一系列参数。返回值是pymongo.cursor。
# - version(year)：数据库行政区划的版本，参数year是年份，默认参数None，表示所有年份。返回值
#                  是版本的列表。
# -----------------------------------------------------------------------------------------

from pylatex.command import Command
from pylatex import Document, Section, Subsection, Subsubsection, Package
from pylatex.graphics import Figure
from pylatex.lists import Itemize, Enumerate, Description
from pylatex.table import Tabular, MultiColumn
from datetime import datetime
import matplotlib.pyplot as plt

# 类Report是用来生成报告
class Report:
    '''
    类Report用来生成报告
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
        self.presentSection = {}

        # 初始化章节内容
        self.content = []

    # 设置章节
    def createSection(self,title):
        self.section = Section(title)
        self.presentSection = {'section':self.section}

    # 设置分支章节
    def createSubSection(self,title):
        self.subsection = Subsection(title)
        if len(self.presentSection) > 2:
            del self.presentSection['subsubsection']
        self.presentSection['subsection'] = self.subsection

    # 设置分支分支章节
    def createSubSubSection(self,title):
        self.subsubsection = Subsubsection(title)
        self.presentSection['subsubsection'] = self.subsubsection

    # 添加文本内容
    def addText(self,text):
        self.content.append(text)

    # 添加列表
    def addList(self,lists,type=1):
        if type == 1:
            items = Itemize()
        if type == 2:
            items = Enumerate()
        if type == 3:
            items = Description()
        for item in lists:
            items.add_item(item)

        self.content.append(items)

    # 添加表格
    def addTable(self, nrow=0,ncol=0,data=None):
        # 初始化参数
        tabsize = '|' + '|'.join(['c']*ncol) + '|'
        mtable = Tabular(tabsize)
        for i in range(nrow):
            mtable.add_hline()
            mtable.add_row(tuple(data[i]))
        mtable.add_hline()
        self.content.append(Command('begin',arguments='center'))
        self.content.append('这是我们写的歌\par')
        self.content.append(mtable)
        self.content.append(Command('end',arguments='center'))

    # 添加图片
    def addFigure(self,file=None,caption=None,width='240px'):
        graph = Figure(position='h!')
        graph.add_image(file, width=width)
        if caption is not None:
            graph.add_caption(caption)
        self.content.append(graph)

    # 添加matplotlib的图形
    def addMatplot(self,plt,filepath='E:/Report/',caption=None):
        x = str(int(datetime.now().timestamp()*1000))
        filename = filepath + 'graph/' + x + '.pdf'
        plt.savefig(filename)
        self.addFigure(filename,caption)

    # 添加内容到报告
    def flush(self):
        if len(self.presentSection) > 2:
            for item in self.content:
                self.presentSection['subsubsection'].append(item)
            self.presentSection['subsection'].append(self.presentSection['subsubsection'])
            self.presentSection['section'].append(self.presentSection['subsection'])
            self.doc.append(self.presentSection['section'])
        elif len(self.presentSection) > 1:
            for item in self.content:
                self.presentSection['subsection'].append(item)
            self.presentSection['section'].append(self.presentSection['subsection'])
            self.doc.append(self.presentSection['section'])
        elif len(self.presentSection) > 0:
            for item in self.content:
                self.presentSection['section'].append(item)
            self.doc.append(self.presentSection['section'])
        else:
            for item in self.content:
                self.doc.append(item)

        # 重新清零
        self.content = []

    # 生成pdf文件
    def generate_pdf(self,filepath=''):
        self.doc.generate_pdf(filepath=filepath)


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]
    plt.plot(x, y)
    report = Report(title='数据分析报表',author='冥王星人')
    report.createSection('地球和月球')
    report.createSubSection('地球往事')
    report.addText('这是为你写的歌。')
    report.addMatplot(plt,caption='有趣的图形')
    report.flush()
    report.createSection('冥王星')
    report.addText('欢迎来到地球。')
    report.addFigure('D:/Temp/glen.jpg')
    report.addList(['你们','我们'])
    report.addTable(2,4,[[1,2,3,4],[5,6,7,8]])
    report.flush()
    report.generate_pdf('e:/Report/first_report.pdf')

















