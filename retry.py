# -*- coding:utf-8 -*-
import os, sys, os.path
import time
import datetime
import unittest
import traceback
import shutil
from HTMLTestRunner import _TestResult
from basic.myReqClient import MyReqClient
from basic.mySysCommon import MySysCommon
import basic.myGlobal
import subprocess
import gc


logger = basic.myGlobal.getLogger()

"""动态加载cases目录下的所有的caseFile"""
path = '{}/cases'.format(os.getcwd())
fileList = os.listdir(path)
for projName in fileList:
    dirPath = path + "/" + projName
    if os.path.isdir(dirPath) is not True:
        continue

    pyFileList = os.listdir(dirPath)
    for pyFlie in pyFileList:
        pyFilePath = dirPath + "/" + pyFlie
        if '.py' not in pyFlie:
            continue

        if os.path.isfile(pyFilePath) is not True:
            continue


        if '__init__' in pyFlie:
            continue

        if 'py' != pyFlie.split('.')[1]:
            continue

        import_string = 'from cases.{} import {}'.format(projName, pyFlie.split('.')[0])

        logger.debug('加载case文件{}'.format(import_string))
        exec(import_string)

"""加载所有case完成"""


class CaseRunner(object):
    """docstring for CaseRunner"""

    def __init__(self):
        super(CaseRunner, self).__init__()
        self.logger = logger
        self.myReqClient = MyReqClient()

        self.maxNumberTimes = 3

        self.retryCaseFile = '{}/log/retryCase.txt'.format(os.getcwd())

        self.mySysCommon = MySysCommon()


    def __disposeTestCase(self, caseStr, taskId, sheetName, caseId, browser, paramsIn, checkPoint, url, proPath):
        """处理测试用例"""
        strBuf = str(caseStr)
        strBufSplit = strBuf.split('.')
        #projNameStr = strBufSplit[0].strip()
        fileName = strBufSplit[1].strip()
        className = strBufSplit[2].strip()
        caseName = strBufSplit[3].strip()
        AllPirParams = {'taskId': taskId,
                        'sheetName': sheetName,
                        'caseId': caseId,
                        'browserType': browser,
                        'params_in': paramsIn,
                        'checkPoint': checkPoint,
                        'url': url,
                        'proPath': proPath
        }
        case = '{}.{}("{}", {})'.format(fileName, className, caseName, AllPirParams)
        #logger.debug(case)
        return case


    def run(self):
        """"""
        retryCaseFile = self.retryCaseFile
        if os.path.exists(retryCaseFile) is False:
            logger.debug('没有可执行的用例')
            return
        caseInfoList = self.mySysCommon.mySysReadFileLines(retryCaseFile)

        self.mySysCommon.mySysCopyFile(retryCaseFile, retryCaseFile + '.bak')

        self.mySysCommon.mySysRemoveFile(retryCaseFile)

        result = _TestResult(0)

        #
        for caseTmpInfo in caseInfoList:
            startTimeCase = datetime.datetime.now()
            #
            textStr = caseTmpInfo.replace("\r\n", "")
            textStr = textStr.replace("\r", "")
            textStr = textStr.replace("\n", "")
            if textStr == "":
                continue
            caseInfo = eval(caseTmpInfo)
            caseId = caseInfo['caseId']
            sheetName = caseInfo['sheetName']
            caseStr = caseInfo['caseName']
            browserTmp = caseInfo['browser']
            url = caseInfo['url']
            taskId = caseInfo['taskId']
            browser = browserTmp.lower()
            proPath = caseInfo['proPath']
            logger.debug(sheetName)

            # 取输入参数和检查点
            caseData = self.myReqClient.getParams(taskId, sheetName, caseId)
            if caseData is None:
                continue
            paramsIn = caseData['paramsIn']
            checkPoint = caseData['checkPoint']
            if paramsIn == "":
                paramsIn = {}
            else:
                paramsIn = eval(paramsIn)
            if checkPoint == "":
                checkPoint = {}
            else:
                checkPoint = eval(checkPoint)

            # 处理测试用例
            case = self.__disposeTestCase(caseStr, taskId, sheetName, caseId, browser, paramsIn, checkPoint, url, proPath)

            # 创建测试套件
            suite = unittest.TestSuite()
            try:
                # 添加测试集
                logger.debug('--------------------------------------------------------------------------------------------')
                logger.debug('--------用例：{} {} {} 添加测试集，浏览器：{}'.format(taskId.split('/')[-1], sheetName, caseId, browser))
                # logger.debug(str(caseInfo))
                suite.addTest(eval(case))

                # 执行用例
                result.myRun(taskId, sheetName, caseId, browser, caseStr, caseInfo, retryCaseFile, startTimeCase)
                suite.run(result)

                # 判断是否重试
                while result.retryNumLocal > 0:# and result.retryNumLocal < result.retryNumMax:
                    # 执行用例
                    suite.run(result)
            except:
                excstr = traceback.format_exc()
                logger.error('--------用例：{} {} {} ，浏览器：{}  {}'.format(taskId, sheetName, caseId, browser, str(excstr)))
                self.mySysCommon.mySysCopyFile(retryCaseFile + '.bak', retryCaseFile)
            gc.collect()
        return True

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

def runner():
    logger.info('---------------------开始运行task: 重试')
    caseRunner = CaseRunner()
    caseRunner.run()
    logger.info('---------------------结束运行task: 重试')
    logger.info('------------------------------------------------------------------------------------')


if __name__ == '__main__':
    LocalPath = os.getcwd()
    logPath = '{}/log'.format(LocalPath)
    reportPath = '{}/report'.format(LocalPath)
    picPath = '{}/pic'.format(reportPath)
    # delPathFile(picPath)
    # delPathFile(reportPath)
    delPathFile(logPath, 'log')

    runner()

    gc.collect()

