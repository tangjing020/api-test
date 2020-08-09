# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-5-08
# update time：2020-5-08
# input： file_name, sheet_id
# description:
#class：OperationExcel(),OperationExcel('testdata1.xlsx', 0)
#function：get_data(), get_line(), get_cell_value(row, col), write_value(row, col, value), get_cols_data(cols_id), get_row_num(case_id), get_row_value(row), get_row_data(case_id)

import os
import xlrd
from xlutils.copy import copy
from common import configPath
from common.logger import Logger

log = Logger().file_log()

class OperationExcel:

    def __init__(self, file_name=None, sheet_name=None):
        if file_name:
            self.file_name = file_name
            self.sheet_name = sheet_name
        else:
            self.file_name = '../testData/testdata.xls'
            self.sheet_name = 'Sheet1'
        self.data = self.get_data()

    def get_data(self):
        """
        获取文件的表格sheets的内容
        :return: table
        """
        data = xlrd.open_workbook(os.path.join(configPath.excel_path, self.file_name))
        table = data.sheet_by_name(self.sheet_name)
        return table

    def get_line(self):
        """
        获取sheets行数
        :return: tables.nrows
        """
        table = self.data
        return table.nrows

    def get_cell_value(self, row, col):
        """
        获取单元格数据
        :param row: 行
        :param col: 列
        :return: cell
        """
        table = self.data
        cell = table.cell_value(row, col)
        log.info(cell)
        return cell

    def write_value(self, row, col, value):
        """
        写入数据到指定单元格
        :param row: 行
        :param col: 列
        :param value: 值
        :return:
        """
        file = os.path.join(configPath.excel_path, self.file_name)
        read_data = xlrd.open_workbook(file)
        write_data = copy(read_data)
        log.info(write_data)
        sheet_data = write_data.get_sheet(self.sheet_id)
        sheet_data.write(row, col, value)
        write_data.save(file)
        log.info(file)

    def get_cols_data(self, cols_id=None):
        """
        获取某一列的内容
        :param cols_id: 列id
        :return: cols 列值
        """

        if cols_id != None:
            cols = self.data.col_values(cols_id)
        else:
            cols = self.data.col_values(0)
        return cols

    def get_row_num(self, case_id):
        """
        根据caseId获取对应行号
        :param case_id: 用例id
        :return: num 行号
        """
        num = 0
        cols_data = self.get_cols_data()
        for col_data in cols_data:
            if case_id in col_data:
                return num
            num = num + 1

    def get_row_value(self, row):
        """
        根据行号获取行内容
        :param row: 行
        :return:
        """
        row_value = self.data.row_values(row)
        return row_value

    def get_row_data(self,case_id):
        """
        根据caseId获取行内容
        :param case_id: 用例id
        :return:
        """
        row_num = self.get_row_num(case_id)
        row_data = self.get_row_value(row_num)
        return row_data

    def get_is_run(self, row):
        """
        获取用例是否执行
        :param row: 行
        :return: flag
        """
        flag = None
        col = int(configExcel.get_is_run())
        run_flag = self.opera_excel.get_cell_value(row, col)
        if run_flag == 'yes':
            flag = True
        else:
            flag = false
        return flag
        
    def get_xls_list(self, xls_name_col=None, sheet_name_col=None, is_run_col=None):
        
        if xls_name_col == None and sheet_name_col == None and is_run_col == None:
            xls_name_list = [self.file_name]
            sheet_name_list = [self.sheet_name]
        else:

            xls_name_list = self.get_cols_data(xls_name_col)
            sheet_name_list = self.get_cols_data(sheet_name_col)
            is_run_list = self.get_cols_data(is_run_col)
        
        cls = []
        #run_case = []
        #skip_case = []
        #block_case = []
        for k in range(len(xls_name_list)):
            if '.xls' not in xls_name_list[k]:
                continue
            else:            
                xlsPath = os.path.join(configPath.excel_path, xls_name_list[k])
                xls_file =  xlrd.open_workbook(xlsPath)
                sheet_name = str(sheet_name_list[k]).split(',')
                is_run = is_run_list[k]
                if is_run == 'yes':
                    for j in range(len(sheet_name)):
                        table = xls_file.sheet_by_name(sheet_name[j])
                        log.info("'test_xls':" + xls_name_list[k] + ",'test_sheet:'" + sheet_name[j] )
                        nrows = table.nrows
                        for i in range(nrows):
                            if table.row_values(i)[0] != u'case_id' and table.row_values(i)[0]:
                                cls.append(table.row_values(i))
        return cls


    """
                                if table.row_values(i)[8] == u'no':
                                    skip_case.append(table.row_values(i)[0])
                                elif table.row_values(i)[8] == u'block':
                                    block_case.append(table.row_values(i)[0])
                                elif table.row_values(i)[8] == u'yes' or table.row_values(i)[8] == '':
                                    cls.append(table.row_values(i))
                                    run_case.append(table.row_values(i)[0])
                                else:
                                    log.warning(table.row_values(i)[0] + "的is_run值错误")

        log.info("run_case: " + str(run_case))
        log.info("skip_case: " + str(skip_case))
        log.info("block_case: " + str(block_case))
        return cls,run_case,skip_case,block_case
    """

if __name__ == '__main__':
    test = OperationExcel('allTestdata.xls', 'Sheet1').get_xls_list(1,2)
    #test = OperationExcel('testdata.xls', 'Sheet1').get_xls_list()
    #test = OperationExcel('testdata1.xls', 0).get_row_data('login')