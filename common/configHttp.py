# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-28
# input： None
# description: 用于配置基本的接口方法
#class： ConfigHttp
#function： ConfigHttp().send_post()，ConfigHttp().send_get()，ConfigHttp().send_put()，ConfigHttp().send_delete()

import json
import requests
from common.logger import Logger

log = Logger().file_log()

#禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class RunMethod():

    def post_main(self, url, data, header=None):
        """
        定义post方法
        :param url:
        :param data:
        :param header:
        :return:
        """
        try:
            if header != None:
                result = requests.post(url=url, data=data, headers=header, verify=False)
            else:
                result = requests.post(url=url, params=data, verify=False)

            http_code = result.status_code
            result = result.json()
            #以字符串形式输出，ensure_ascii设置是否ascii编码，sort_keys设置a-z排序，indent设置缩进格式
            res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            log.info('methond: post, httpCode: %s, url: %s,headers: %s' % (http_code, url,header))
            log.info('content={%s}' % data)
            log.info('response: %s' % res)
            return res,http_code
        except TimeoutError:
            log.error("Time out!")
            return None


    def get_main(self, url, data=None, header=None):
        """
        定义get方法
        :param url:
        :param data:
        :param header:
        :return:
        """
        try:
            if header != None:
                result = requests.get(url=url, params=data, headers=header, verify=False)
            else:
                result = requests.get(url=url, params=data, verify=False)

            http_code = result.status_code
            result = result.json()
            res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            log.info('methond: get, httpCode: %s, url: %s' % (http_code, url))
            log.info('data: %s' % data)
            log.info('response: %s' % res)
            return res,http_code
        except TimeoutError:
            log.error("Time out!")
            return None

    def delete_main(self, url, data, header):
        """
        定义delete方法
        :param url:
        :param data:
        :param header:
        :return:
        """
        try:
            if header != None:
                result = requests.delete(url=url, data=data, headers=header, verify=False)
            else:
                result = requests.delete(url=url, params=data, verify=False)

            http_code = result.status_code
            result = result.json()
            #以字符串形式输出，ensure_ascii设置是否ascii编码，sort_keys设置a-z排序，indent设置缩进格式
            res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            log.info('methond: delete, httpCode: %s, url: %s' % (http_code, url))
            log.info('data: %s' % data)
            log.info('response: %s' % res)
            return res,http_code
        except TimeoutError:
            log.error("Time out!")
            return None


    def put_main(self, url, data, header):
        """
        定义put方法
        :param url:
        :param data:
        :param header:
        :return:
        """
        try:
            if header != None:
                result = requests.put(url=url, data=data, headers=header, verify=False)
            else:
                result = requests.put(url=url, params=data, verify=False)

            http_code = result.status_code
            result = result.json()
            #以字符串形式输出，ensure_ascii设置是否ascii编码，sort_keys设置a-z排序，indent设置缩进格式
            res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            log.info('methond: put, httpCode: %s, url: %s' % (http_code, url))
            log.info('data: %s' % data)
            log.info('response: %s' % res)
            return res,http_code
        except TimeoutError:
            log.error("Time out!")
            return None



    def run_main(self, method, url=None, data=None, header=None):
        '''
        根据method执行对应的方法
        '''
        result = None
        if method == 'post':
            result = self.post_main(url, data, header)
        elif method == 'get':
            result = self.get_main(url, data, header)
        elif method == 'put':
            result = self.put_main(url, data, header)
        elif method == 'delete':
            result = self.delete_main(url, data, header)
        else:
            log.error("method值错误")
        return result
