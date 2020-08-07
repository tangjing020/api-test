# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-6-20
# input： None
# description: 用于执行测试用例，使用unittest+ddt解读excel用例并执行
# class：
# function：

import unittest
from common.ddt import ddt,data,unpack
import json
import re
import time
import random
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
global_var.update(Base().get_uploadfile_abspath("uploadFile.json"))

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
    def test(self, case_id, case_description, url, method, is_header, header_uri, depand_case, depand_param, depand_key, body, is_run, httpCode, expect_res, uploadFile):

        if depand_param:
            expect_param_key_list = re.findall("(.+?)(?=\\=)", depand_param)
            expect_param_value_list = re.findall("(?<=\\=)(.+?)", depand_param)
            for i in range(len(expect_param_key_list)):
                if not expect_param_value_list and not global_var[expect_param_key_list[i]]:
                    log.info("参数%s期望的值和接口返回的值都为空,满足条件执行用例" % expect_param_key_list[i])
                    continue
                if not expect_param_value_list and global_var[expect_param_key_list[i]]:
                    log.info("参数 %s 期望的值为空, 接口返回的值为 %s,不满足条件跳过用例" % (expect_param_key_list[i],global_var[expect_param_key_list[i]]))
                    raise self.skipTest("%s: 参数%s期望的值为空, 接口返回的值为%s,不满足条件跳过用例" % (
                    case_id, expect_param_key_list[i], global_var[expect_param_key_list[i]]))

                elif str(global_var[expect_param_key_list[i]]) == str(expect_param_value_list[i]):
                    log.info("参数%s期望的值和接口返回的值一致，值为:%s, 满足条件执行用例" % (expect_param_key_list[i],expect_param_value_list[i]))
                    continue

                else:
                    log.info("参数%s期望的值和接口返回的值不一致，不满足条件跳过用例" % expect_param_key_list[i])
                    raise self.skipTest("%s: 参数%s期望的值和接口返回的值不一致，不满足条件跳过用例" % (case_id, expect_param_key_list[i]))

        depand_case_list = str(depand_case).split(';')
        depand_fail_case_list = list(set(depand_case_list).intersection(set(self.fail_case)))
        depand_skip_case_list = list(set(depand_case_list).intersection(set(self.skip_case)))

        if is_run == 'yes' and depand_fail_case_list == [] and depand_skip_case_list == []:
            self.apiTest(case_id, case_description, url, method, is_header, header_uri, depand_key, body, httpCode, expect_res, uploadFile)

        elif is_run != 'yes':
            self.skip_case.append(case_id)
            log.info(case_id + ": is_run参数不为yes，用例不执行，跳过")
            raise self.skipTest(case_id + ": is_run参数不为yes，用例不执行，跳过")

        elif depand_fail_case_list != []:
            self.skip_case.append(case_id)
            log.info("%s: 依赖的用例（depand_case）%s运行失败, 导致用例不执行，跳过" % (case_id, depand_fail_case_list))
            raise self.skipTest("%s: 依赖的用例（depand_case）%s运行失败, 导致用例不执行，跳过" % (case_id, depand_fail_case_list))

        elif depand_skip_case_list != []:
            self.skip_case.append(case_id)
            log.info("%s: 依赖的用例（depand_case）%s未运行, 导致用例不执行，跳过" % (case_id, depand_skip_case_list))
            raise self.skipTest("%s: 依赖的用例（depand_case）%s未运行, 导致用例不执行，跳过" % (case_id, depand_skip_case_list))

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


    def apiTest(self, case_id, case_description, url, method, is_header, header_uri, depand_key, body, httpCode, expect_res,uploadFile):

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
            #校验是否需要改密码
            if 'access_token' not in res[0] and 'firstUpdatePassword' in res[0]:
                url = self.base_url + '/oauth/api/v1/update-person-pwd-auth'
                body_str = '{"pword": "%s", "userId": "%s"}' % (global_var['passWord'], res[0]['userId'])
                body = json.loads(body_str)
                res_modfify = self.run_method.run_main('post', url, body)
                if res_modfify[1] == '200':
                    res = self.run_method.run_main(method, url, body)
            OperationJson().write_token_json(res[0], "token.json")


        # 接口是否需要header，需要则从token文件中获取token，并执行用例
        elif is_header == 'yes':
            header = OperationJson().get_header("token.json")
            log.info(header)
            if header_uri:
                header.update(Base().key_values_to_dic(header_uri))
            res = self.run_method.run_main(method, url, body, header)

        # 接口不需要header，执行用例
        else:
            res = self.run_method.run_main(method, url, body)


        # 校验执行结果
        try:
            self.assertEqual(httpCode, res[1])
            if ';' not in expect_res:
                if '${' and '}' not in expect_res:
                    self.assertIn(expect_res, res[0])
                else:
                    expect_res_key = re.findall("(?<=\\$\\{)(.+?)(?=\\})", expect_res)
                    self.assertIn(global_var[expect_res_key[0]], res[0])
            else:
                check_list = str(expect_res).split(';')
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
                var_value = json.loads(res[0])
                if var_value != []:
                    if '[' and ']' in param_value_list[i]:
                        json_key_list = re.findall("(?<=\\[)(.+?)(?=\\])", param_value_list[i])
                        var_value = json.loads(res[0])
                        for j in range(len(json_key_list)):
                            if json_key_list[j].isdigit():
                                if global_var['res_indenx'] != 'digit':
                                    var_value = var_value[global_var['res_indenx']]
                                else:
                                    index = random.randint(0, len(var_value) - 1)
                                    global_var['res_indenx'] = index
                                    var_value = var_value[global_var['res_indenx']]
                            else:
                                var_value = var_value[json_key_list[j]]
                    else:
                        var_value = var_value[param_value_list[i]]
                    log.info("获取" + param_key_list[i] + "的值: " + str(var_value))
                    global_var[param_key_list[i]] = var_value
                else:
                    global_var[param_key_list[i]] = ""

        global_var['res_indenx'] = 'digit'
        log.info("**************" + case_id + ": " + case_description + ": Test End**************")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

