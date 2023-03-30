# -*- coding:utf-8 -*-
from multiprocessing import Process
import os,sys
import time
import traceback
import platform
platformSystem = platform.system()
import gc


# 创建log和report/pic等目录
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


def runJob():
    cmd = None
    if platformSystem == "Windows":
        cmd = 'python runner.py'
    else:
        cmd = '/usr/bin/python3 runner.py'
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
    # os.popen("adb kill-server")
    # os.popen("adb start-server")
    # os.popen("adb shell rm -f /sdcard/test*.mp4")

    loaclPath = os.getcwd() + '/'
    retryCaseFile = '{}log/retryCase.txt'.format(loaclPath)
    if os.path.exists(retryCaseFile):
        os.remove(retryCaseFile)

    runJob()


if __name__ == '__main__':
    # delPathFile(picPath)
    # delPathFile(reportPath)
    delPathFile(logPath, 'log')

    main()

    gc.collect()
