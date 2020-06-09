# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-4-28
# input： None
# description: 路径定义文件： 如文件路径，测试报告文件路径等

import os

# 脚本绝对路径
base_dir = os.path.split(os.path.realpath(__file__))[0].replace('common','')
# 配置文件及路径
config_path = base_dir + 'testData' + '\\config.ini'
# excel文件及路径：
excel_path = base_dir + 'testCase'
# 测试数据路径：
testData_path = base_dir + 'testData'
# 日志路径：
log_dir = base_dir + 'Logs/'
# 测试报告路径：
report_dir = base_dir + 'HtmlReport'
# 测试文件路径：
file_dir = base_dir + 'testFile'