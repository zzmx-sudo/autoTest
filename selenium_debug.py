#-*- coding:utf-8 -*-
import sys
import os
import datetime
sys.path.append(os.getcwd())
# sys.path.append(sys.path[0])
import unittest
from basic.myReqClient import MyReqClient
from cases.Zd.comm import Comm
from cases.Zd.commApp import CommApp
from cases.Zd.commDaping import CommDaping
from cases.Zd.commApi import CommApi
suite = unittest.TestSuite()
myReqClient = MyReqClient()
LocalPath = os.getcwd()
reportPath = '{}\\report'.format(LocalPath)
# 删除目录中所有文件
Filelist = os.listdir(reportPath)
for i in range(0, len(Filelist)):
    path = os.path.join(reportPath, Filelist[i])
    if os.path.isfile(path):
        os.remove(path)

def myAddTest(casename):
    AllPirParams = {'taskId': "1",
                    'caseId': "1",
                    'sheetName': '',
                    'browserType': 'chrome',  # chrome,android,firefox,api
                    'params_in': {},
                    'checkPoint': {},
                    'proPath': '{}/cases/Zd/'.format(LocalPath),
                    'closeProxyAndJsLog': True  # True None
                    }
    if "testIpadApi" in casename:
        AllPirParams['url'] = "https://test3.c.cn"  # api

        AllPirParams['browserType'] = 'api'
        suite.addTest(Comm(casename, AllPirParams))
    elif "testIpad" in casename:
        AllPirParams['url'] = "https://test2.c.cn"  # app

        AllPirParams['browserType'] = 'chrome'
        suite.addTest(CommApp(casename, AllPirParams))
    elif "testApp" in casename:
        AllPirParams['url'] = "https://test2.c.cn"  # app

        AllPirParams['browserType'] = 'chrome'
        suite.addTest(CommApp(casename, AllPirParams))
    elif "testDaping" in casename:
        AllPirParams['url'] = "https://test1.c.cn"  # 大屏

        AllPirParams['browserType'] = 'chrome'
        suite.addTest(CommDaping(casename, AllPirParams))

if __name__ == '__main__':
    for x in range(0, 1):
        myAddTest("testIpadShengXiaOK")
        # yAddTest("testDapingYouXianShiYeOK")

    runner = unittest.TextTestRunner()  # 将在测试的数用TextTestRunner运行
    runner.run(suite)

