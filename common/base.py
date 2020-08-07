# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-15
# input： None
# description: 用于自动化运行需要的基础方法
# 1.参数键值对转换为字典格式
#class： Base
#function： Base().key_values_to_dic()


from common import configPath
from common.operationJson import OperationJson
from common.logger import Logger
log = Logger().file_log()

class Base():

    def key_values_to_dic(self,key_values_):
        """
        将键值对转换为字典形式
        :param : key_values_
        :return: key_values_dic_
        """
        key_values_dic_ = {}
        for line in key_values_.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                key, value = line.split("=", 1)
                key = key.strip()
                key_values_dic_[key] = value
            except ValueError:
                log.error("键值对错误，转换失败....错误键值对信息：%s" % line)
        return key_values_dic_

    def get_uploadfile_abspath(self,fileName):
        """
        将键值对转换为字典形式
        :param : key_values_
        :return: key_values_dic_
        """

        uploadfile_var = OperationJson().get_data(fileName)
        for j in uploadfile_var.keys():
            uploadfile_var[j] = configPath.base_dir + uploadfile_var[j]
        return uploadfile_var




if __name__ == '__main__':
    data = Base().get_uploadfile_abspath("uploadFile.json")
    log.info(data)

