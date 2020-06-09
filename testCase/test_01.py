# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-28
# input： None
# description: 用于配置基本的接口方法
#class： ConfigHttp
#function：

import unittest
import paramunittest
import json
import re
import time
from common import readExcel
from common.readConfig import ReadConfig
from common.configHttp import RunMethod
from common.base import Base
from common.handleUrlAndBody import HandleUrlAndBody
from common.logger import Logger

log = Logger().file_log()

xls_name='小工具'+'/'+'testdata1.xls'
sheet_name1='Sheet1'
sheet_name2='Sheet3'
sheet_id=0
global_var = Base().get_data()
test_xls1 = readExcel.ReadExcel(xls_name,sheet_name1).get_xls()
test_xls2 = readExcel.ReadExcel(xls_name,sheet_name2).get_xls()

@paramunittest.parametrized(*test_xls1,*test_xls2)
class test(unittest.TestCase):
    
    def setParameters(self, case_id, case_name, url, method, header, depand_case, depand_field, depand_key, body, is_run, httpCode):
        self.case_id = str(case_id)
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.header = str(header)
        self.depand_case = str(depand_case)
        self.depand_field = str(depand_field)
        self.depand_key = str(depand_key)
        self.body = str(body)
        self.is_run = str(is_run)
        self.httpCode = httpCode


    @classmethod
    def setUpClass(self):
        """
        test start
        """
        self.get_data = readExcel.ReadExcel(xls_name, sheet_name1)
        self.run_method = RunMethod()
        self.read_config = ReadConfig()
        self.base_url = self.read_config.get_http('baseUrl')
        self.base = Base()

    def test(self):
        """
        """
        case_lines = self.get_data.get_case_lines()
        if case_lines > 1:
            self.apiTest(self.case_id, self.url, self.method, self.header, self.depand_case, self.depand_field, self.depand_key, self.body, self.is_run, self.httpCode)

    @classmethod
    def tearDownClass(self):
        """
        """

    def apiTest(self, case_id, url, method, is_header, depand_case, depand_field, depand_key, body, is_run, httpCode):
        # 判断用例是否需要运行
        if is_run == 'yes':

            log.info("**************" + case_id + ": Test Start**************")
            #获取当前时间
            global_var['currentTime'] = "-" + str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

            # 获取url和body
            urlAndBody = HandleUrlAndBody().handle_url_and_body(self.base_url, url, body, global_var)
            url = urlAndBody[0]
            body = urlAndBody[1]
            body = self.base.key_values_to_dic(body)

            # 是否要写入header,需要则获取header，并执行用例
            if is_header == 'write':
                res = self.run_method.run_main(method, url, body)
                HandleUrlAndBody().write_token_json(res[0])

            # 接口是否需要header，需要则从token文件中获取token，并执行用例
            elif is_header == 'yes':
                header = HandleUrlAndBody().get_header()
                res = self.run_method.run_main(method, url, body, header)

            # 接口不需要header，执行用例
            else:
                res = self.run_method.run_main(method, url, body)

            # 校验执行结果
            self.assertEqual(res[1], httpCode)

            if depand_key:
                # 获取需要保存的参数和值,并保存
                param_value_list = re.findall("(?<=\\$\\{)(.+?)(?=\\})", depand_key)
                param_key_list = re.findall("(.+?)(?=\\=)", depand_key)
                for i in range(len(param_value_list)):
                    var_value = json.loads(res[0])[param_value_list[i]]
                    global_var[param_key_list[i]] = var_value

            log.info("**************" + case_id + ": Test End**************")

        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'],exit=False)
        
        