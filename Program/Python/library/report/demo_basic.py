# coding=UTF-8

from pylatex.command import Command
from pylatex import Document, Section, Subsection, Package
from pylatex.utils import italic,escape_latex

def fill_document(doc):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    s = u'地区'

    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append(s)
            doc.append(escape_latex('Also some crazy characters: $&#{}'))


if __name__ == '__main__':

     # Document with `\maketitle` command activated
    doc = Document()
    doc.packages.append(Package('ctex',options=['UTF8','noindent']))
    doc.preamble.append(Command('title', 'Awesome Title'))
    doc.preamble.append(Command('author', 'Anonymous author'))
    doc.preamble.append(Command('date', r'\today'))
    doc.append(r'\maketitle')

    fill_document(doc)
    doc.generate_pdf('d:\\down\\basic_maketitle')




