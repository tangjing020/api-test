# -*- coding: utf-8 -*-
# Author: tangjing
# create time: 2020-4-13
# update time：2020-6-9
# input： None
# description: 用于发送测试结果及其附件到邮箱
#              邮箱信息在 config.ini中配置
#              测试报告路径为configPath文件下的report_dir
#class： ConfigEmail
#function： ConfigEmail().send_email()

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from common import configPath
from common.readConfig import ReadConfig
from common.file import File
from common.logger import Logger
log = Logger().file_log()

#读取配置文件获取邮件参数
subject = ReadConfig().get_email('subject')
smtpserver = ReadConfig().get_email('smtpserver')
user = ReadConfig().get_email('user')
password = ReadConfig().get_email('password')
sender = ReadConfig().get_email('sender')
receiver = ReadConfig().get_email('receiver').split(',')
testMember = ReadConfig().get_email('testMember').split(',')
log = Logger().file_log()

class ConfigEmail():

    '''
    发送email
    :param self: None
    :return: None
    '''

    def send_email(self,startTime,timeTemp,allAccount,passAccount,failAccount,skipAccount):
        # 定义mixed实现构建一个带附件的邮件体，即定义后邮件可以带附件
        msg = MIMEMultipart()

        # 读取本地的测试报告
        file_list = File().sort_file_by_time(configPath.report_dir)
        file_path = os.path.join(configPath.report_dir,file_list[-1])
        with open(file_path, "rb") as fp:
            mail_att_body = fp.read()

        #定义邮件正文MIMEText()
        #发送正文
        mail_body = "本次接口测试用例执行结果如下: <br>" \
                    "<br>" \
                    "测试人员:  {0} <br>" \
                    "开始时间:  {1} <br>" \
                    "执行时间:  {2} <br>" \
                    "用例总数:  {3} <br>" \
                    "通过用例数: {4} <br>" \
                    "失败用例数: {5} <br>" \
                    "跳过用例数: {6} <br>" \
                    "测试通过率: {7:.2f}% <br>" \
                    "<br>" \
                    "具体结果分析和接口测试详情请下载附件后查看(需要先下载哦)。".format(testMember[0],startTime,timeTemp,allAccount,passAccount,failAccount,skipAccount,passAccount/allAccount*100)
        msg_html = MIMEText(mail_body,_subtype="html",_charset="utf-8")
        msg.attach(msg_html)

        #发送附件
        msg_file = MIMEText(mail_att_body, _subtype="base64", _charset="utf-8")
        msg_file["Content-Type"] = "application/octet-stream"
        msg_file["Content-Disposition"] = 'attachment; filename="{}"'.format(file_list[-1])
        msg.attach(msg_file)

        #定义邮件基本信息
        msg['From'] = sender
        msg['To'] = ",".join(receiver)
        msg['Subject'] = Header(subject, 'utf-8')

        #登录账号发送邮件
        try:
            smtp = smtplib.SMTP_SSL(smtpserver, 465)
            smtp.login(user, password)
            smtp.sendmail(sender, receiver, msg.as_string())
        except exception as e:
            log.error("邮件发送失败！失败详情: "+e)
        finally:
            smtp.quit()

if __name__ == '__main__':
    ConfigEmail().send_email()