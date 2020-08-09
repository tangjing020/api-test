# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-28
# input： None
# description: 用于配置基本的接口方法
#class： ConfigHttp
#function：

import re
import os
import json
from common.logger import Logger
from common import configPath

log = Logger().file_log()
class HandleUrlAndBody:

    def handle_url(self, baseUrl, url, var_dict):
        if '.com' in url:
            url = baseUrl + url.split('.com')[1:]
        elif url.startswith('/'):
            url = baseUrl + url
        else:
            log.error("url错误：" + url)

        if '${' and '}' in url:
            var_list = re.findall("(?<=\\$\\{)(.+?)(?=\\})", url)
            for i in range(len(var_list)):
                try:
                    url = url.replace("${" + var_list[i] + "}", var_dict[var_list[i]])
                except NameError:
                    log.error("请求url的参数:" + var_list[i] + "没有值," + "无法获取完整url")
        return url

    def handle_body(self, body, var_dict):
        if '${' and '}' in body:
            var_list = re.findall("(?<=\\$\\{)(.+?)(?=\\})", body)
            for i in range(len(var_list)):
                try:
                    body = body.replace("${" + var_list[i] + "}", var_dict[var_list[i]])
                except NameError:
                    log.error("请求body的参数:" + var_list[i] + "没有值," + "无法获取完整body")
        return body

    def handle_header(self, header):
        if '=' in header:
            headr = key_values_to_dic
            for i in range(len(var_list)):
                try:
                    body = body.replace("${" + var_list[i] + "}", var_dict[var_list[i]])
                except NameError:
                    log.error("请求body的参数:" + var_list[i] + "没有值," + "无法获取完整body")
        return body

if __name__ == '__main__':
    header = {}
    header = HandleUrlAndBody().get_header(header)
    log.info(header)