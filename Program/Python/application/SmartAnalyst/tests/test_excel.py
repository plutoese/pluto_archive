# coding=UTF-8

from nose.tools import *
import sys
import os
sys.path.insert(0, os.path.abspath('E:\\Git\\Program\\Python\\application\\SmartAnalyst\\lib\\file'))

from class_Excel import Excel

def test_excel():
    filename = r'E:\Data\city\variable\m2012.xlsx'
    mexcel = Excel(filename)
    mdata1 = mexcel.read()

    outfile = r'd:\down\demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new().append(mdata1)
    moutexcel.close()

    filename = r'd:\down\demo.xlsx'
    mexcel = Excel(filename)
    mdata2 = mexcel.read()

    assert_equal(mdata1,mdata2)
















