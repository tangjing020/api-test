# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-06-09
# update time：2020-06-09
# input： file_path，backup
# description: 文件处理, 文件排序，获取最新文件，定义目录最多保留文件(默认20)
# class： File()
# function：sort_file_by_time，get_newest_file，delete_file_backup

import os
from common import configPath
from common.logger import Logger

log = Logger().file_log()

class File():

    def sort_file_by_time(self, file_path):

        lists = os.listdir(file_path)
        lists.sort(key=lambda fn: os.path.getmtime(file_path + os.sep + fn))  # lambda匿名函数
        # key=lambda fn: os.path.getmtime(report + os.sep + fn)
        # 相当于
        # def key(fn):
        #	return os.path.getmtime(report+os.sep+fn)
        return lists


    def get_newest_file(self, file_path):

        file_lists = self.sort_file_by_time(file_path)
        file_with_path = os.path.join(file_path, file_lists[-1])
        return file_with_path


    def delete_file_backup(self, file_path, backup=20):

        file_lists = self.sort_file_by_time(file_path)
        if len(file_lists) <= backup:
            pass
        else:
            for i in range(len(file_lists) - backup):
                os.remove(os.path.join(file_path, file_lists[i]))

if __name__ == '__main__':
    data = File().delete_file_backup(configPath.report_dir, 8)