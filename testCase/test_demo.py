# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-28
# input： None
# description: 用于配置基本的接口方法
# class： ConfigHttp
# function：

import unittest
from common.ddt import ddt,data,unpack
import json
import re
import time
import paramunittest
from common.readConfig import ReadConfig
from common.configHttp import RunMethod
from common.base import Base
from common.operationExcel import OperationExcel
from common.operationJson import OperationJson
from common.handleUrlAndBody import HandleUrlAndBody
from common.logger import Logger

log = Logger().file_log()
global_var = OperationJson().get_data("data.json")

xls_name = global_var['xls_name']
sheet_name = global_var['sheet_name']
xls_name_col = int(global_var['xls_name_col'])
sheet_name_col = int(global_var['sheet_name_col'])
is_run_col = int(global_var['is_run_col'])
opera_excel = OperationExcel(xls_name, sheet_name)
test_xls = OperationExcel(xls_name, sheet_name).get_xls_list(xls_name_col, sheet_name_col, is_run_col)


"""
@paramunittest.parametrized(*test_xls)
class test(unittest.TestCase):

    def setParameters(self, case_id, case_description, url, method, is_header, depand_case, depand_key, body, is_run, httpCode, expect_res):
        self.case_id = str(case_id)
        self.case_description = str(case_description)
        self.url = str(url)
        self.method = str(method)
        self.is_header = str(is_header)
        self.depand_case = str(depand_case)
        self.depand_key = str(depand_key)
        self.body = str(body)
        self.is_run = str(is_run)
        self.httpCode = httpCode
        self.expect_res = str(expect_res)
"""
@ddt
class api_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        test start
        """
        self.run_method = RunMethod()
        self.read_config = ReadConfig()
        self.base_url = self.read_config.get_http('baseUrl')
        self.base = Base()
        self.fail_case = []
        self.skip_case = []


    @data(*test_xls)
    @unpack
    def test(self, case_id, case_description, url, method, is_header, depand_case, depand_key, body, is_run, httpCode, expect_res):
        if is_run == 'yes' and depand_case not in self.fail_case and depand_case not in self.skip_case:
            self.apiTest(case_id, case_description, url, method, is_header, depand_case, depand_key, body, is_run, httpCode, expect_res)

        elif is_run != 'yes':
            self.skip_case.append(case_id)
            log.info(case_id + ": is_run参数不为yes，用例不执行，跳过")
            raise self.skipTest(case_id + ": is_run参数不为yes，用例不执行，跳过")

        elif depand_case in self.fail_case or depand_case in self.skip_case:
            self.skip_case.append(case_id)
            log.info(case_id + ": 依赖的用例（depand_case）" + depand_case + "运行失败或者未运行，导致用例不执行，跳过")
            raise self.skipTest(case_id + ": 依赖的用例（depand_case）" + depand_case + "运行失败或者未运行，导致用例不执行，跳过")
        else:
            log.info("未知错误: is_run,depand_case参数有误")

    """
    def test(self):
        self.apiTest(self.case_id, self.case_description,self.url, self.method, self.is_header, self.depand_case, self.depand_key,self.body, self.is_run, self.httpCode, self.expect_res)
    """

    @classmethod
    def tearDownClass(self):
        """
        """


    def apiTest(self, case_id, case_description, url, method, is_header, depand_case, depand_key, body, is_run, httpCode, expect_res):

        log.info("**************" + case_id + ": " + case_description + ": Test Start**************")
        # 获取当前时间
        global_var['currentTime'] = "-" + str(time.strftime("%Y%m%d%H%M%S", time.localtime()))

        # 获取url和body
        url = HandleUrlAndBody().handle_url(self.base_url, url, global_var)
        body = HandleUrlAndBody().handle_body(body, global_var)
        body = self.base.key_values_to_dic(body)

        # 是否要写入header,需要则获取header，并执行用例
        if is_header == 'write':
            res = self.run_method.run_main(method, url, body)
            OperationJson().write_token_json(res[0], "token.json")

        # 接口是否需要header，需要则从token文件中获取token，并执行用例
        elif is_header == 'yes':
            header = OperationJson().get_header("token.json")
            res = self.run_method.run_main(method, url, body, header)

        # 接口不需要header，执行用例
        else:
            res = self.run_method.run_main(method, url, body)


        # 校验执行结果
        try:
            self.assertEqual(httpCode, res[1])
            if ',' not in expect_res:
                if '${' and '}' not in expect_res:
                    self.assertIn(expect_res, res[0])
                else:
                    expect_res_key = re.findall("(?<=\\$\\{)(.+?)(?=\\})", expect_res)
                    self.assertIn(global_var[expect_res_key[0]], res[0])
            else:
                check_list = str(expect_res).split(',')
                for i in range(len(check_list)):
                    if '${' and '}' not in check_list[i]:
                        self.assertIn(check_list[i], res[0])
                    else:
                        expect_res_key = re.findall("(?<=\\$\\{)(.+?)(?=\\})", check_list[i])
                        self.assertIn(global_var[expect_res_key[0]], res[0])
        except AssertionError as e:
            log.error(e)
            log.error("fail_case:" + case_id)
            self.fail_case.append(case_id)
            log.info(self.fail_case)
            raise e


        if depand_key:
            # 获取需要保存的参数和值,并保存
            param_value_list = re.findall("(?<=\\$\\{)(.+?)(?=\\})", depand_key)
            param_key_list = re.findall("(.+?)(?=\\=)", depand_key)
            for i in range(len(param_value_list)):
                var_value = json.loads(res[0])[param_value_list[i]]
                global_var[param_key_list[i]] = var_value
        log.info("**************" + case_id + ": " + case_description + ": Test End**************")




if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

