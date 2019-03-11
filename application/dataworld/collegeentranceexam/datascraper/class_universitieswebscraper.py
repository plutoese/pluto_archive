# coding=UTF-8

"""
=========================================
大学信息爬虫
=========================================

:Author: glen
:Date: 2018.10.22
:Tags: asyncio scraper
:abstract: 大学信息爬虫

**类**
==================
StaticWebScraper
    基于协程的静态网页爬虫

**使用方法**
==================


**示范代码**
==================
::

"""

import re
import time
import copy
import requests
from bs4 import BeautifulSoup
from lib.base.webscraper.class_static_web_scraper import StaticWebScraper
from lib.base.database.class_mongodb import MongoDB, MonCollection
from lib.base.webscraper.class_htmlparser import HtmlParser


class CollegeInfo():
    def __init__(self):
        mongo = MongoDB(conn_str='localhost:27017')
        self._college_info = MonCollection(mongo, database='webdata', collection_name='college_info').collection
        self._college_intro = MonCollection(mongo, database='webdata', collection_name='college_introduction').collection

        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def init_first_stage(self):
        web_fmt = "http://college.gaokao.com/schlist/a{}/p{}"

        for i in range(1,32):
            url = web_fmt.format(str(i), '1')
            raw_result = requests.get(url, headers=self._headers).text
            bs_obj = BeautifulSoup(raw_result, "lxml")
            for string in bs_obj.select('#qx')[0].strings:
                total_pages = re.split('页',re.split('/',string)[1])[0]
                break

            for j in range(1,int(total_pages)+1):
                surf_url = web_fmt.format(str(i), str(j))
                print(surf_url)
                surf_result = requests.get(surf_url, headers=self._headers).text
                surf_obj = BeautifulSoup(surf_result, "lxml")
                surf_content =  surf_obj.select('.scores_List')[0]

                colleges = [item.attrs['title'] for item in surf_content.select('.blue')]

                college_info = []
                for ul_item in surf_content.select('ul'):
                    one_college_info = dict()
                    for n in range(len(ul_item.select('li'))):
                        if n == 1:
                            college_type = (ul_item.select('li')[n]).contents
                            if len(college_type) == 1:
                                one_college_info['985'] = False
                                one_college_info['211'] = False
                            elif len(college_type) == 2:
                                if college_type[1].string == '211':
                                    one_college_info['985'] = False
                                    one_college_info['211'] = True
                                elif college_type[1].string == '985':
                                    one_college_info['985'] = True
                                    one_college_info['211'] = False
                                else:
                                    raise Exception
                            else:
                                one_college_info['985'] = True
                                one_college_info['211'] = True
                        else:
                            key, value = re.split('：',(ul_item.select('li')[n]).string)
                            if value == '——' or value == '------':
                                value = None
                            one_college_info[key] = value
                    college_info.append(one_college_info)

                for m in range(len(colleges)):
                    college_info[m]['学校'] = colleges[m]

                for college in college_info:
                    found = self._college_info.find_one(college)
                    if found is None:
                        print('Insert..', college)
                        self._college_info.insert_one(college)

if __name__ == '__main__':
    scraper = CollegeInfo()
    #scraper.init_first_stage()
    scraper.init_introduction()
