import os
import time
import common.HTMLTestRunner as HTMLTestRunner
#from common.HTMLTestReportCN import HTMLTestRunner
from BeautifulReport import BeautifulReport as bf
import unittest
import configPath
from common.configEmail import ConfigEmail
from common.readConfig import ReadConfig
from common.file import File
from common.logger import Logger
#from apscheduler.schedulers.blocking import BlockingScheduler
#import pythoncom


log.info(configPath.base_dir)

class AllTest:#

    def __init__(self):
        global resultPath,log
        # 日志文件
        log = Logger().file_log()
        # 测试报告
        #resultPath = configPath.report_dir + 'report_' + str(time.strftime("%Y-%m-%d_%H-%M",time.localtime()))
        # 测试用例集
        self.caseListFile = os.path.join(configPath.file_dir, "caselist.txt")
        # 测试用例
        self.caseFilePath = os.path.join(configPath.base_dir, "testCase")
        self.caseList = []
        # 测试报告
        self.reportPath = os.path.join(configPath.base_dir, "HtmlReport")
        # 邮件开关
        self.email_on = ReadConfig().get_email('email_on')

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，获取需要执行的测试用例,#号开头则不用执行
        :return:
        """
        log.info(configPath.base_dir)
        log.info(self.caseListFile)
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """

        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:
            case_name = case.split("/")[-1]
            log.info("testFile：" + case_name + ".py")
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFilePath, pattern = case_name + '.py', top_level_dir=None)
            # 将discover存入suite_module元素组
            suite_module.append(discover)
            #log.info('suite_module:'+str(suite_module))
        # 判断suite_module元素组是否存在元素, 存在则循环使用discover中取出test_name，添加到测试集
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTests(test_name)
        else:
            return None
        return test_suite

    def run(self):
        """
        run test
        :return:
        """

        try:
            log.info("*********TEST START*********")
            # 调用set_case_suite获取test_suite
            suit = self.set_case_suite()
            if suit is not None:
                #fp = open(resultPath, 'wb')
                #调用HTMLTestRunner
#                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,verbosity=2,title='Test Report',description='Test Description')
#                runner.run(suit)
                run = bf(suit)  # 实例化BeautifulReport模块
                run.report(filename='report_' + str(time.strftime("%Y-%m-%d_%H-%M",time.localtime())), description='烟草项目接口测试报告',report_dir=self.reportPath)
                log.info(self.reportPath)
                begin_time = run.begin_time
                end_time = run.end_time
                all_count = int(run.testsRun)
                success_count = int(run.success_count)
                failure_count = int(run.failure_count)
                skipped_count = int(run.skipped)


            else:
                log.info("No testcase.")
        except Exception as ex:
            log.error(str(ex))

        finally:
            #清理环境, 发送测试邮件
            File().delete_file_backup(self.reportPath, 5)
            if self.email_on == 'on':
                ConfigEmail().send_email(begin_time,end_time,all_count,success_count,failure_count,skipped_count)
                log.info("邮件发送成功")
            else:
                log.info("邮件开关配置关闭，如需发送邮箱，请在配置文件配置打开")
            log.info("*********TEST END*********")
            if failure_count != 0:
                raise ValueError("failure_count = " + str(failure_count))           
            #fp.close()

# pythoncom.CoInitialize()
# scheduler = BlockingScheduler()
# scheduler.add_job(AllTest().run, 'cron', day_of_week='1-5', hour=14, minute=59)
# scheduler.start()

if __name__ == '__main__':
    AllTest().run()


