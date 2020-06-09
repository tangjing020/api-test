# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-11
# update time：2020-4-22
# input： None
# description:  读取配置文件
#class： ReadConfig
#function： ReadConfig().get_email()；ReadConfig().get_http()

import configparser
from common import configPath


class ReadConfig():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(configPath.config_path, encoding='utf-8')

    def get_email(self,name):
        value = self.config.get('EMAIL', name)
        return value
    def get_http(self,name):
        value = self.config.get('HTTP', name)
        return value
    def get_account(self,name):
        value = self.config.get('ACCOUNT', name)
        return value

