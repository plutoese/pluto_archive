# coding=UTF-8

# --------------------------------------------------------------
# class_htmlparser文件
# @class: HtmlParser类
# @introduction: HtmlParser类用来解析html对象
# @dependency: bs4及re包
# @author: plutoese
# @date: 2016.06.24
# --------------------------------------------------------------

from bs4 import BeautifulSoup
import re


class HtmlParser:
    """HtmlParser类用来解析html对象

    :param str htmlcontent: html的字符串
    :return: 无返回值
    """
    def __init__(self,html_content=None):
        if isinstance(html_content,BeautifulSoup):
            self.bs_obj = html_content
        else:
            self.html_content = html_content
            self.bs_obj = BeautifulSoup(self.html_content, "lxml")

    def table(self,css=None):
        """ 返回表格的数据

        :param css: table的css选择器
        :return: 表格的列表
        """
        table = []
        if css is not None:
            tds = self.bs_obj.select(''.join([css,' > tr']))

        for item in tds:
            table.append([re.sub('\s+','',unit.text) for unit in item.select('td')])

        return table

if __name__ == '__main__':
    pass

