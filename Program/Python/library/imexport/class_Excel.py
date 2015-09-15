# coding=UTF-8

import xlrd
import xlsxwriter

# 处理Excel文件的类
class Excel:
    '''
    类Excel用来导入和导出Excel文件。
    
    属性：
    self.filename: 文件名
    self.data: 读入的数据
    
    方法：
    __init__(self, filename:str=None)：构造函数，参数filename表示文件名。
    read(self, sheetnum:int=0)->list: 读取Excel表的数据，参数sheetnum表示Excel文件表单号。返回值为Excel表中所有数据。
    new(self): 新建一个Excel文件，文件名为self.filename。无返回值。
    append(self, data:list=None): 把数据写入Excel文件，参数data表示要写入Excel文件的数据，默认值None表示用self.data。无返回值。
    close(self): 关闭Excel文件，无参数。无返回值。

    Demo：
    1. 读取Excel文件的数据
    filename = r'C:\Down\student.xls'    # 设定文件名
    mexcel = Excel(filename)    # 建立Excel对象
    mdata = mexcel.read()    # 读取Excel文件的数据

    2. 写入Excel文件的数据
    outfile = r'c:\down\demo.xlsx'    # 设定文件名
    moutexcel = Excel(outfile)    # 建立Excel对象
    moutexcel.new()    # 新建Excel文件和页面
    moutexcel.append(mexcel.data)    # 往新建的Excel文件里添加数据
    moutexcel.close()    # 关闭Excel文件
    '''
    def __init__(self, filename:str=None):
        # 设定文件名
        self.filename = filename

    # 读取excel表的数据
    def read(self, sheetnum:int=0)->list:
        # 连接文件
        self.file = xlrd.open_workbook(self.filename)
        # 设定页
        self.table = self.file.sheet_by_index(sheetnum)
        # excel表的行和列
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols
        # 读取数据
        self.data = [self.table.row_values(i) for i in range(self.nrows)]
        return self.data

    # 新建Excel文件和页面
    def new(self):
        self.workbook = xlsxwriter.Workbook(self.filename)
        self.worksheet = self.workbook.add_worksheet()

    # 把数据写入excel文件
    def append(self, data:list=None):
        if data is None:
            data = self.data
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.worksheet.write(i, j, data[i][j])

    # 关闭Excel文件
    def close(self):
        self.workbook.close()


if __name__ == '__main__':
    filename = r'C:\Down\student.xls'
    mexcel = Excel(filename)
    mdata = mexcel.read()
    print(mdata)
    

    '''outfile = u'c:\\down\\demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new()
    moutexcel.append(mexcel.data)
    moutexcel.close()'''