# -*- coding:utf-8 -*-
from multiprocessing import Process
import os,sys
import time
import traceback
import platform
platformSystem = platform.system()
import schedule
from basic.mySysCommon import MySysCommon
import gc

# 创建log和report/pich录
LocalPath = os.getcwd()
logPath = '{}/log'.format(LocalPath)
reportPath = '{}/report'.format(LocalPath)
picPath = '{}/pic'.format(reportPath)

if not os.path.exists(logPath):
    os.makedirs(logPath)
if not os.path.exists(picPath):
    os.makedirs(picPath)

import basic.myGlobal


logger = basic.myGlobal.getLogger()


def runJob(name):
    cmd = None
    if platformSystem == "Windows":
        cmd = '{}.bat'.format(name)
    else:
        cmd = '/usr/bin/python3 {}.py'.format(name)
    logger.debug('执行：{}'.format(cmd))
    os.system(cmd)


def delPathFile(dirPath, ept=''):
    # 删除目录中所有文件
    try:
        fileList = os.listdir(dirPath)
        # logger.debug(fileList)
        for i in range(0, len(fileList)):
            path = os.path.join(dirPath, fileList[i])
            if os.path.isfile(path):
                if ept == '':
                    os.remove(path)
                elif 'log' in fileList[i]:
                    os.remove(path)
    except:
        # logger.error(traceback.format_exc())
        return None

def main():
    global logger

    runJob('main')


def retry():
    global logger

    runJob('retry')


def notice():
    global logger

    mySysCommon = MySysCommon()
    loaclPath = os.getcwd() + '/'
    retryCaseFile = '{}log/retryCase.txt'.format(loaclPath)
    lines = mySysCommon.mySysReadFileLines(retryCaseFile)
    if lines is not None and lines != "" and len(lines) != 0:
        token = mySysCommon.mySysGetEpWeChatToken('ww01834534fbe26ae', '3Tyx5435675ATf3Vk')
        if token is not None:
            result = '用例执行失败数：{}\n{}'.format(len(lines), lines).replace("\\\\\\", "")
            mySysCommon.mySysSendPerMessageEpWeChat(token, 1000009, result)
    else:
        logger.debug("不用通知")


if __name__ == '__main__':
    # delPathFile(picPath)
    # delPathFile(reportPath)
    delPathFile(logPath, 'log')

    # schedule.every().day.at("05:00").do(main)
    # schedule.every().day.at("05:00").do(retry)
    # schedule.every().day.at("05:00").do(retry)
    # schedule.every().day.at("05:00").do(notice)
    # schedule.every().day.at("20:00").do(main)
    # schedule.every().day.at("20:00").do(retry)
    # schedule.every().day.at("20:00").do(retry)
    # schedule.every().day.at("20:00").do(notice)
    schedule.every(1).minutes.do(main)
    schedule.every(1).minutes.do(retry)
    schedule.every(1).minutes.do(retry)
    schedule.every(1).minutes.do(notice)

    while 1:
        schedule.run_pending()
        gc.collect()
        time.sleep(5)
