import xlwt

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
这里是操作excel的工具类,以后也可以直接复用
方法调用SpiderUtils.create_excel(...) 
'''


class ExcelUtils(object):

    @staticmethod
    def create_excel(sheet_name, row_titles):
        '''
        创建excel文件与sheet表，并创建他们的第一行标题
        :param sheet_name: excel中sheet_name文件的名称
        :param row_titles: excel文件的标题行
        :return: excel_file,excel_sheet
        '''

        f = xlwt.Workbook()
        sheet_info = f.add_sheet(sheet_name, cell_overwrite_ok=True)
        for i in range(0, len(row_titles)):
            sheet_info.write(0, i, row_titles[i])

        return f, sheet_info

    @staticmethod
    def write_excel(excel_file, excel_sheet, count, data, excel_name):
        '''
        把数据写入到excel中.这是一个静态方法
        注意：这里所有的数据都不要写死，方便复用.
        :param excel_file:  传入一个excel文件
        :param excel_sheet:  传入一个excel_sheet表
        :param count:  excel文件的行数
        :param data:  要传入的一条数据
        :param excel_name: excel文件名
        :return: None
        '''
        for j in range(len(data)):
            excel_sheet.write(count, j, data[j])

        excel_file.save(excel_name)