# coding = UTF-8

"""
=========================================
Econpaper网站爬虫“：国外经济学文献爬虫
=========================================

:Author: glen
:Date: 2018.04.01
:Tags: asyncio scraper
:abstract: 基于协程的国外经济学文献爬虫

**类**
==================

    基于协程的静态网页爬虫

**使用方法**
==================


**示范代码**
==================
::

"""

import time
import re
from bs4 import BeautifulSoup
from lib.base.webscraper.class_async_static_scraper import AsyncStaticScraper
from lib.base.database.class_mongodb import MongoDB, MonCollection


class EconPapersCrawler:
    def __init__(self, journals_webs=None):
        self._journal_websites = journals_webs

        self._pre_conn = MonCollection(mongodb=MongoDB(), database='papers', collection_name='econpaperwebsites')
        self._paper_conn = MonCollection(mongodb=MongoDB(), database='papers', collection_name='econpapers')

    def precrawler(self):
        """ 抓取issue的网页地址，并存入数据库

        :return:
        """
        for web in self._journal_websites:
            record = {'url':web, 'type':'issue', 'status':0}
            found = self._pre_conn.collection.find_one(record)
            if found is None:
                self._pre_conn.collection.insert_one(record)

        scraper = AsyncStaticScraper(urls=self._journal_websites)
        scraper.start()
        for result, url in scraper.result:
            bsobj = BeautifulSoup(result, "lxml")
            for item in bsobj.find_all("a"):
                if 'href' in str(item):
                    if re.match('^default\d*\.htm$',str(item['href'])):
                        issue_website = ''.join([url,item['href']])
                        record = {'url':issue_website, 'type':'issue', 'status':0}
                        found = self._pre_conn.collection.find_one(record)
                        if found is None:
                            self._pre_conn.collection.insert_one(record)

    def paper_web_crawler(self):

        while True:
            found = self._pre_conn.collection.find({'type':'issue','status':0},projection={'_id':1,'url':1},limit=5)
            paper_webs = {item['url']:item['_id'] for item in found}
            if len(paper_webs) < 1:
                print('break out!')
                break

            scraper = AsyncStaticScraper(urls=paper_webs.keys())
            scraper.start()

            for result, url in scraper.result:
                bsobj = BeautifulSoup(result, "lxml")
                for item in bsobj.find_all("a"):
                    if 'href' in str(item):
                        if re.match('^v_', str(item['href'])):
                            article_website = '/'.join(['/'.join(re.split('/',url)[:-1]), item['href']])
                            record = {'url': article_website, 'type': 'article', 'status': 0}

                            found = self._pre_conn.collection.find_one(record)
                            if found is None:
                                self._pre_conn.collection.insert_one(record)
                print(url,paper_webs[url])
                self._pre_conn.collection.find_one_and_update({'_id':paper_webs[url]},{'$set': {'status': 1}})

            time.sleep(10)


    def paper_crawler(self):

        while True:
            start_time = time.time()
            found = self._pre_conn.collection.find({'type':'article','status':0},projection={'_id':1,'url':1},limit=20)
            paper_webs = {item['url']:item['_id'] for item in found}
            if len(paper_webs) < 1:
                print('break out!')
                break

            scraper = AsyncStaticScraper(urls=paper_webs.keys())
            scraper.start()

            for result, url in scraper.result:
                bsobj = BeautifulSoup(result, "lxml")
                title = bsobj.select('.colored')[0].string

                content = bsobj.select('.bodytext p')

                authors = []
                for item in content[0].select('i'):
                    authors.append(item.string.strip())

                journal = content[1].contents[0].string.strip()
                rowdata = [item for item in re.split(',',re.sub('\s+','',content[1].contents[1].string))[1:] if len(item) > 0]
                if len(rowdata) == 4:
                    year, vol, issue, pages = rowdata
                    year = int(year)
                    vol = int(re.search('\d+',vol).group())
                    if re.search('\d+', issue) is not None:
                        issue = int(re.search('\d+', issue).group())
                    else:
                        issue = None
                elif len(rowdata) == 3:
                    year = [item for item in rowdata if re.match('^\d{4}$', item)]
                    if len(year) > 0:
                        year = int(year[0])
                    else:
                        year = None

                    vol = [item for item in rowdata if re.search('vol', item)]
                    if len(vol) > 0:
                        vol = int(re.search('\d+', vol[0]).group())
                    else:
                        vol = None

                    issue = [item for item in rowdata if re.search('issue', item)]
                    if len(issue) > 0:
                        issue = int(re.search('\d+', issue[0]).group())
                    else:
                        issue = None
                    if len([item for item in rowdata if re.match('^[\dvxi]+-[vxi\d]+$',item)]) > 0:
                        pages = [item for item in rowdata if re.match('^[\dvxi]+-[vxi\d]+$',item)][0]
                    else:
                        pages = None
                elif len(rowdata) == 5:
                    year = int([item for item in rowdata if re.match('^\d{4}$',item)][0])
                    vol = [item for item in rowdata if re.search('vol',item)][0]
                    vol = int(re.search('\d+', vol).group())
                    issue = [item for item in rowdata if re.search('issue',item)][0]
                    issue = int(re.search('\d+', issue).group())
                    if len([item for item in rowdata if re.match('^[\dvxi]+-[vxi\d]+$',item)]) > 0:
                        pages = [item for item in rowdata if re.match('^[\dvxi]+-[vxi\d]+$',item)][0]
                    else:
                        pages = None
                else:
                    print('Wrong!',rowdata)
                    raise Exception

                abstract = content[2].contents[1].string.strip()

                record = {'url':url, 'title':title, 'authors':authors, 'journal':journal, 'year':year, 'vol':vol,
                          'issue':issue, 'pages':pages, 'abstract':abstract}

                found = self._paper_conn.collection.find_one({'url':record['url']})
                if found is None:
                    self._paper_conn.collection.insert_one(record)
                    print('insert: ', record['title'])
                else:
                    print('Already exist!!!')

                print(url,paper_webs[url])
                self._pre_conn.collection.find_one_and_update({'_id':paper_webs[url]},{'$set': {'status': 1}})

            print('*****Total time*****: ',time.time()-start_time)
            time.sleep(10)



if __name__ == '__main__':
    journals = ['https://econpapers.repec.org/article/oupqjecon/',
                'https://econpapers.repec.org/article/aeajeclit/',
                'https://econpapers.repec.org/article/aeajecper/',
                'https://econpapers.repec.org/article/kapjeczfn/',
                'https://econpapers.repec.org/article/blarandje/',
                'https://econpapers.repec.org/article/rjerandje/',
                'https://econpapers.repec.org/article/ouprestud/',
                'https://econpapers.repec.org/article/wlyemetrp/',
                'https://econpapers.repec.org/article/ecmemetrp/',
                'https://econpapers.repec.org/article/aeaaejmac/',
                'https://econpapers.repec.org/article/aeaaejmic/',
                'https://econpapers.repec.org/article/aeaaejpol/',
                'https://econpapers.repec.org/article/aeaaejapp/',
                'https://econpapers.repec.org/article/aeaaecrev/',
                'https://econpapers.repec.org/article/eeeecosys/',
                'https://econpapers.repec.org/article/tafecsysr/',
                'https://econpapers.repec.org/article/binbpeajo/',
                'https://econpapers.repec.org/article/oupjeurec/',
                'https://econpapers.repec.org/article/blajeurec/',
                'https://econpapers.repec.org/article/tprjeurec/',
                'https://econpapers.repec.org/article/ouprenvpo/',
                'https://econpapers.repec.org/article/kapjecgro/',
                'https://econpapers.repec.org/article/eeetransa/',
                'https://econpapers.repec.org/article/eeetransb/',
                'https://econpapers.repec.org/article/eeetranse/',
                'https://econpapers.repec.org/article/eeetrapol/',
                'https://econpapers.repec.org/article/tprrestat/',
                'https://econpapers.repec.org/article/eeeecolec/',
                'https://econpapers.repec.org/article/eeeeneeco/',
                'https://econpapers.repec.org/article/eeejotrge/',
                'https://econpapers.repec.org/article/anrreveco/',
                'https://econpapers.repec.org/article/eeejhecon/',
                'https://econpapers.repec.org/article/oupjecgeo/',
                'https://econpapers.repec.org/article/eeejeeman/',
                'https://econpapers.repec.org/article/eeeinecon/',
                'https://econpapers.repec.org/article/wlyjpamgt/',
                'https://econpapers.repec.org/article/wlyhlthec/',
                'https://econpapers.repec.org/article/tafregstd/',
                'https://econpapers.repec.org/article/blajregsc/',
                'https://econpapers.repec.org/article/eeewdevel/',
                'https://econpapers.repec.org/article/ucpjlabec/',
                'https://econpapers.repec.org/article/tafrripxx/',
                'https://econpapers.repec.org/article/eeedeveco/',
                'https://econpapers.repec.org/article/wlyiecrev/',
                'https://econpapers.repec.org/article/blareviec/',
                'https://econpapers.repec.org/article/wlyjapmet/',
                'https://econpapers.repec.org/article/jaejapmet/',
                'https://econpapers.repec.org/article/eeejuecon/',
                'https://econpapers.repec.org/article/wlyemjrnl/',
                'https://econpapers.repec.org/article/ectemjrnl/',
                'https://econpapers.repec.org/article/eeeeconom/',
                'https://econpapers.repec.org/article/eeepubeco/',
                'https://econpapers.repec.org/article/blaobuest/',
                'https://econpapers.repec.org/article/kapjecinq/',
                'https://econpapers.repec.org/article/kapjculte/',
                'https://econpapers.repec.org/article/ucpecdecc/',
                'https://econpapers.repec.org/article/wlyeconjl/',
                'https://econpapers.repec.org/article/ecjeconjl/',
                'https://econpapers.repec.org/article/eeejeborg/',
                'https://econpapers.repec.org/article/blachinae/',
                'https://econpapers.repec.org/article/eeechieco/',
                'https://econpapers.repec.org/article/eeejcecon/',
                'https://econpapers.repec.org/article/eeeiepoli/',
                'https://econpapers.repec.org/article/eeeeecrev/',
                'https://econpapers.repec.org/article/sprjopoec/',
                'https://econpapers.repec.org/article/blapresci/',
                'https://econpapers.repec.org/article/sprpresci/',
                'https://econpapers.repec.org/article/eeeregeco/',
                'https://econpapers.repec.org/article/kapcompec/']

    STEP_ONE = False
    STEP_TWO = False
    STEP_THREE = True

    if STEP_ONE:
        for i in range(0,len(journals),5):
            ecrawler = EconPapersCrawler(journals_webs=journals[i:i+5])
            ecrawler.precrawler()

    if STEP_TWO:
        ncrawler = EconPapersCrawler()
        ncrawler.paper_web_crawler()

    if STEP_THREE:
        acrawler = EconPapersCrawler()
        acrawler.paper_crawler()





