# coding=UTF-8

# --------------------------------------------------------------
# class_literaturereport文件
# @class: LiteratureReport类
# @introduction: LiteratureReport类生成初步文献报告
# @dependency: urllib包，bs4包
# @author: plutoese
# @date: 2016.04.08
# --------------------------------------------------------------

import re
from lib.base.database.class_mongodb import MongoDB, MonCollection
from pymongo import ASCENDING, DESCENDING
from lib.base.pylatex.class_article import Article
from pylatex.utils import escape_latex


class LiteratureReport:
    def __init__(self,database='papers',collection='econpapers'):
        self.literatures = None
        self._paper_conn = MonCollection(mongodb=MongoDB(), database=database, collection_name=collection)

    def load_record_from_db(self,query=None,sort=None):
        if query is None:
            self.literatures = self._paper_conn.collection.find()
        else:
            if sort is None:
                self.literatures = self._paper_conn.collection.find(query)
            else:
                self.literatures = self._paper_conn.collection.find(query).sort(sort)

    def to_report(self,file_name):
        replace_word = {'articleTitle':'Literature Report',
                    'arcticleabstract':'Abstract'}
        doc = Article(r'D:\github\pluto\lib\base\pylatex\template\article_template_02.tex',replace_word)
        for item in self.literatures:
            title = escape_latex(item['title'])
            doc.document.add_section(title,3)
            doc.document.add_list(['---'.join([item['journal'],str(item['year']),','.join(item['authors'])])],type=1)
            abstract = item.get('abstract')
            if abstract is not None:
                abstract = escape_latex(abstract)
                doc.document.append(abstract)
        #doc.document.generate_tex(r'E:\github\latexdoc\latexdoc\template\academicjournal\wlscirep\plutopaper.tex')
        doc.document.generate_pdf(r'D:\github\pluto\lib\base\pylatex\template\output\{}'.format(file_name))


if __name__ == '__main__':
    report = LiteratureReport()

    conn = MonCollection(mongodb=MongoDB(), database='papers', collection_name='econpapers')
    journals = conn.collection.find().distinct('journal')

    for journal in journals:
        print(journal)
        if journal == 'Econometrica':
            report.load_record_from_db(query={'journal': journal, 'year': {'$gte': 2012}},
                                       sort=[('journal', ASCENDING), ('year', DESCENDING)])
            report.to_report(file_name=journal)
            continue
        report.load_record_from_db(query={'journal':journal,'year':{'$gte':2010}},
                                   sort=[('journal',ASCENDING),('year',DESCENDING)])
        journal = re.sub(':', '', journal)
        report.to_report(file_name=journal)
