# coding=UTF-8

"""
=========================================
高考分数线爬虫
=========================================

:Author: glen
:Date: 2018.10.18
:Tags: asyncio scraper
:abstract: 高考分数爬虫

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


class GaoKaoWebScraper():
    def __init__(self):
        mongo = MongoDB(conn_str='localhost:27017')
        self._web_conn = MonCollection(mongo, database='cache', collection_name='gaokaoweb').collection
        self._data_web_conn = MonCollection(mongo, database='cache', collection_name='gaokaodataweb').collection
        self._university_web_conn = MonCollection(mongo, database='cache', collection_name='gaokaouniversityweb').collection
        self._data_conn = MonCollection(mongo, database='webdata', collection_name='gaokao_entrancescore').collection
        self._copy_data_web_conn = MonCollection(mongo, database='webdata', collection_name='gaokaouniversityweb').collection

    def init_first_stage(self):
        web_fmt = "http://college.gaokao.com/schpoint/{}/{}/{}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        for i in range(1,32):
            for j in range(1,32):
                url = web_fmt.format(''.join(['a',str(i)]), ''.join(['b',str(j)]),'p1')
                raw_result = requests.get(url, headers=headers).text
                bs_obj = BeautifulSoup(raw_result, "lxml")
                for string in bs_obj.select('#qx')[0].strings:
                    total_pages = re.split('页',re.split('/',string)[1])[0]
                    break

                if len(total_pages) > 0:
                    for m in range(1,int(total_pages)+1):
                        web = web_fmt.format(''.join(['a',str(i)]), ''.join(['b',str(j)]), ''.join(['p',str(m)]))
                        record = {'type':'search', 'url':web}
                        print(record)
                        self._web_conn.insert_one(record)

    def init_second_stage(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        item = self._web_conn.find({'type':'search'})
        for aitem in item:
            raw_result = requests.get(aitem['url'], headers=headers).text
            bs_obj = BeautifulSoup(raw_result, "lxml")
            for obj in bs_obj.select('.blue'):
                found = obj.find_all(href=re.compile("result"))
                if len(found) > 0:
                    url = found[0]['href']
                    record = {'type': 'data', 'url': url}
                    print(record)
                    self._data_web_conn.insert_one(record)

    def init_three_stage(self):
        university_urls = self._data_web_conn.find().distinct('url')
        for url in university_urls:
            self._university_web_conn.insert_one({'url':url})

    def scrape(self, using_proxy=False):
        vars = ['年份',	'最低', '最高', '平均', '录取人数', '录取批次']
        nums = self._copy_data_web_conn.count()
        while nums > 0:
            urls = [item['url'] for item in self._copy_data_web_conn.find(limit=5)]
            print(urls)
            start = time.time()
            scraper = StaticWebScraper(urls=urls, using_proxy=using_proxy)
            scraper.start()

            for html in scraper.result:
                url = html[1]
                bs_obj = BeautifulSoup(html[0], "lxml")
                record = dict(zip(['university', 'region', 'type'],[item.contents[0] for item in bs_obj.select('.btnFsxBox > font')]))

                htmlparser = HtmlParser(html_content=bs_obj)
                table = htmlparser.table('#pointbyarea > table')
                if len(table) > 0:
                    for item in table:
                        copy_record = copy.copy(record)
                        if len(item) == 0:
                            continue
                        if len(item) == 6:
                            for i in range(len(item)):
                                if i in [0, 1, 2, 3, 4]:
                                    if item[i] == '------':
                                        copy_record[vars[i]] = None
                                    else:
                                        copy_record[vars[i]] = int(float(item[i]))
                                else:
                                    if item[i] == '------':
                                        copy_record[vars[i]] = None
                                    else:
                                        copy_record[vars[i]] = item[i]
                        else:
                            raise Exception

                        found = self._data_conn.find_one(copy_record)
                        if found is None:
                            print('Insert..', copy_record)
                            self._data_conn.insert_one(copy_record)
                self._copy_data_web_conn.delete_one({'url':url})

            print('Total: {}'.format(time.time() - start))
            nums = self._copy_data_web_conn.count()

if __name__ == '__main__':
    scraper = GaoKaoWebScraper()
    #scraper.init_three_stage()
    scraper.scrape(using_proxy=False)
