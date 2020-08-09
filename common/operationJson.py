# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-5-08
# update time：2020-5-08
# input： file_name, sheet_id
# description:
#class：OperationExcel(),OperationExcel('testdata1.xlsx', 0)
#function：get_data(), get_line(), get_cell_value(row, col), write_value(row, col, value), get_cols_data(cols_id), get_row_num(case_id), get_row_value(row), get_row_data(case_id)

import os
import json
from common import configPath
from common.logger import Logger

log = Logger().file_log()

class OperationJson:

    def get_data(self, json_file_name):
        with open(os.path.join(configPath.testData_path, json_file_name), 'r') as fp:
            data_json = json.load(fp)
        return data_json


    def get_header(self, token_file_name):
        header_dict = {}
        token = self.get_data("token.json")["access_token"]
        header_dict['token'] = token
        header_dict['Authorization'] = "Bearer__" + token
        return header_dict

    def write_token_json(self, response, token_file_name):
        with open(os.path.join(configPath.testData_path, token_file_name), 'w') as fp:
            fp.write(response)



if __name__ == '__main__':
    test = OperationExcel('allTestdata.xls', 'Sheet1').get_xls_list(1,2)
