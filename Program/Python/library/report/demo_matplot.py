# coding=UTF-8

import matplotlib
matplotlib.use('Agg')  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt

from pylatex import Document, Package, Section, Figure
from pylatex.graphics import Plt


def main(fname, width, *args, **kwargs):
    doc = Document(fname)
    doc.packages.append(Package('geometry', options=['left=2cm', 'right=2cm']))

    doc.append('Introduction.')

    with doc.create(Section('I am a section')):
        doc.append('Take a look at this beautiful plot:')


        with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image('C:/Users/ADMINI~1/AppData/Local/Temp/pylatex/d7aa2846-c8aa-4a76-89f0-f873002b8408.pdf',width='120px')

        doc.append('Created using matplotlib.')

    doc.append('Conclusion.')

    doc.generate_pdf()


if __name__ == '__main__':
    main('matplotlib_ex-dpi', r'1\textwidth', dpi=300)
    main('matplotlib_ex-facecolor', r'0.5\textwidth', facecolor='b')