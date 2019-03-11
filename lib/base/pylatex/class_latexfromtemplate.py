# coding=UTF-8

# --------------------------------------------------------------
# class_latexfromtemplate文件
# @class: LatexFromTemplate
# @introduction: LatexFromTemplate类用来从模板中生成latex文件
# @dependency: pylatex模块
# @author: plutoese
# @date: 2016.02.18
# --------------------------------------------------------------

import re
from lib.base.pylatex.class_latexdoc import LatexDoc


class LatexFromTemplate:
    """ LatexDoc类用来创建、操作latex文档，生成pdf文档

    """
    def __init__(self,tex_template,replace_word=None):
        self.__doc = None
        self._read_from_file(tex_template,replace_word)

    def _read_from_file(self,tex_file,replace_word=None):
        """ 从latex模板中读取，然后打包到self.doc中

        :param str tex_file: .tex文件
        :return: 无返回值
        """
        if replace_word is None:
            replace_word = dict()
        begin_document_sign = False
        with open(tex_file,'r',encoding='utf8') as fp:
            for line in fp:
                line_no_space = re.sub('\n','',line)
                if re.match('^\s+$',line_no_space) is None:
                    #print('line: ',line_no_space)
                    if replace_word is not None:
                        for keyword in replace_word:
                            if re.search(keyword,line_no_space) is not None:
                                line_no_space = re.sub(keyword,replace_word[keyword],line_no_space)
                    if re.match('^\\\\documentclass',line_no_space) is not None:
                        self.__doc = LatexDoc(documentclass=self.parse_brackets(line_no_space,'\{','\}')[0],
                                            options=self.parse_brackets(line_no_space))
                        #print(self.parse_brackets(line_no_space,'\{','\}')[0])
                        #print(self.parse_brackets(line_no_space))
                        continue
                    if re.match('\\\\begin\{document\}',line_no_space) is not None:
                        begin_document_sign = True
                        continue
                    if re.match('\\\\end\{document\}',line_no_space) is not None:
                        continue
                    if begin_document_sign:
                        self.__doc.append(line_no_space)
                    else:
                        self.__doc.preamble_append(line_no_space)

    @property
    def document(self):
        return self.__doc

    @classmethod
    def parse_brackets(cls,string,first_special_character='\[',second_special_character='\]'):
        if re.search(''.join([first_special_character,'*',second_special_character]),string) is not None:
            return re.split(',',re.split(second_special_character,
                                         re.split(first_special_character,string)[1])[0])
        else:
            return None

if __name__ == '__main__':
    #doc = LatexFromTemplate(r'E:\latex\article_1.tex')

    doc = LatexFromTemplate(r'E:\github\latexdoc\latexdoc\template\academicjournal\wlscirep\main.tex')
    doc.document.generate_tex(r'E:\github\latexdoc\latexdoc\template\academicjournal\wlscirep\plutopaper.tex')
    doc.document.generate_pdf(r'E:\github\latexdoc\latexdoc\template\academicjournal\wlscirep\plutopaper.pdf')


