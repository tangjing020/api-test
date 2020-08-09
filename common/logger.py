# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-22
# input： None
# description: 用于配置日志级别，日志打印格式，日志文件基本信息
#              日志路径为configPath文件下的log_dir
#class： Logger
#function： Logger().file_log()

import logging
from logging.handlers import TimedRotatingFileHandler
from common import configPath


#import time

class Logger(object):

    def __init__(self):

        '''初始化日志参数，并配置'''

        self.logger = logging.getLogger('Logs')
        logging.root.setLevel(logging.NOTSET)
        # 日志文件名称及格式_"+str(time.strftime("%Y-%m-%d_%H-%M",time.localtime()))+".log"
        self.logFileName = configPath.log_dir + "web_apiTest.log"
        # 日志文件日志级别
        self.file_level = 'INFO'
        # console日志级别
        self.console_level = 'INFO'
        # 日志格式
        self.formatter = logging.Formatter('%(asctime)s [%(filename)s][%(levelname)s][%(funcName)s][line:%(lineno)d][%(message)s]')
        # 日志文件最多存放数
        self.backupCount = 2



    def file_log(self):

        '''设置日志handler'''
        # 校验日志句柄
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_level)
            self.logger.addHandler(console_handler)

            file_handler = TimedRotatingFileHandler(filename=self.logFileName, when='D',
                                                    interval=1, backupCount=self.backupCount, delay=True,
                                                    encoding='utf-8')
            # when设置为D，则suffix的格式为%Y-%m-%d_%H-%M，设置M，则名称需到分，格式为%Y-%m-%d_%H-%M,否则无法生效
            file_handler.suffix = "%Y-%m-%d.log"
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_level)
            self.logger.addHandler(file_handler)
        return self.logger
