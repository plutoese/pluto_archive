# coding=UTF-8

"""
=========================================
大学所在地级市爬虫
=========================================

:Author: glen
:Date: 2018.10.24
:Tags: asyncio scraper
:abstract: 大学所在地级市爬虫

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
import pandas as pd
from bs4 import BeautifulSoup
from lib.base.database.class_mongodb import MongoDB, MonCollection


class CollegeCityScraper():
    def __init__(self, college_filepath):
        self._colleges = pd.read_excel(college_filepath)
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def start(self):
        web_fmt = 'http://api.map.baidu.com/place/v2/suggestion?query={}&region={}&city_limit=False&output=json&ak=VtjTxtTZWUq5yB9PvEuKtOkI'
        colleges_copy = copy.deepcopy(self._colleges)
        for ind in colleges_copy.index:
            college = colleges_copy.loc[ind,'学校']
            region = colleges_copy.loc[ind,'高校所在地']
            url = web_fmt.format(college, region)
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                print(college, r.json())
                result = r.json()['result'][0]
                self._colleges.loc[ind, 'name'] = result['name']
                self._colleges.loc[ind, 'province'] = result['province']
                self._colleges.loc[ind, 'city'] = result['city']
            time.sleep(2)

    @property
    def colleges(self):
        return self._colleges

    def export(self, file_path):
        self._colleges.to_excel(file_path)

if __name__ == '__main__':
    scraper = CollegeCityScraper(r'E:\cyberspace\worklot\college\colleges.xlsx')
    scraper.start()
    print(scraper.colleges)
    scraper.export(r'E:\cyberspace\worklot\college\colleges_with_city.xlsx')
    #scraper.init_first_stage()
    #scraper.init_introduction()
