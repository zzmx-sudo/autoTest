# -*- coding:utf-8 -*-
import os, sys, os.path
import datetime
import time
import unittest
import traceback
from basic.myReqClient import MyReqClient
from HTMLTestRunner import HTMLTestRunner
from HTMLTestRunner import _TestResult
import basic.myGlobal
import subprocess
import platform
platformSystem = platform.system()
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
    """"""
    def __init__(self):
        super(CaseRunner, self).__init__()
        self.logger = logger
        self.myReqClient = MyReqClient()

        self.retryCaseFile = '{}/log/retryCase.txt'.format(os.getcwd())

    # Zd.commApp.CommApp.testAppLoginOK .../appWebCase.xls 用例  1    chrome   [输入参数]  [检查点]   [url]  .../cases/Zd/
    def __disposeTestCase(self, caseStr, taskId, sheetName, caseId, browser, paramsIn, checkPoint, url, proPath):
        """处理测试用例"""
        strBuf = str(caseStr)
        strBufSplit = strBuf.split('.')
        #projNameStr = strBufSplit[0].strip()
        fileName = strBufSplit[1].strip()       # commApp
        className = strBufSplit[2].strip()      # CommApp
        caseName = strBufSplit[3].strip()       # testAppLoginOK
        AllPirParams = {'taskId': taskId,
                        'sheetName': sheetName,
                        'caseId': caseId,
                        'browserType': browser,
                        'params_in': paramsIn,
                        'checkPoint': checkPoint,
                        'url': url,
                        'proPath': proPath
        }
        # commApp.CommApp("testAppLoginOK", {"taskId": ".../appWebCase.xls", "sheetName": 用例, "caseId":1, "browserType": chrome, "params_in": [输入参数]， "checkPoint": [检查点], "url": [url], "proPath": "../cases/Zd/"})
        case = '{}.{}("{}", {})'.format(fileName, className, caseName, AllPirParams)
        # logger.debug(case)
        return case


    def startAndroidServer(self):
        """启动appium Android"""
        try:
            output = os.popen('adb devices -l')
            osRetStr = output.read().strip()
            if osRetStr.find('device product') != -1:
                osRetStr = osRetStr.replace("List of devices attached", "").strip()
                sptres = osRetStr.split("\n")
                tmpstr = sptres[len(sptres) - 1]
                devicespl = tmpstr.split(" ")
                deviceId = devicespl[0].strip()
                # print(deviceId)

                # 杀进程node.exe
                os.popen("taskkill /f /im node.exe")

                subprocess.Popen('appium -a 127.0.0.1 -p 4723 -U {} --no-reset'.format(deviceId), shell=True)
                time.sleep(15)

                # 判断进程node.exe
                output = os.popen('tasklist|findstr "node.exe"')
                osRetStr = output.read().strip()
                if osRetStr == "":
                    logger.error('appium启动失败')
                    return False
                else:
                    logger.info('appium启动成功')
                    return True
            elif osRetStr.find('killing') != -1:
                logger.error('请先关闭360手机助手、豌豆荚或91助手等软件！')
                return False
            else:
                logger.error('没有找到任何手机设备！')
                return False
            # os.close()
        except:
            logger.error(traceback.format_exc())
            return False


    def startIOSServer(self):
        """启动appium ios"""



    def run(self):
        """"""
        startTime = datetime.datetime.now()

        timeStr = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        reportName = '{}/report/report{}.html'.format(os.getcwd(), timeStr)  # 测试报告名称

        result = _TestResult(0)

        urlFileName = "#url.xls"
        loaclPath = os.getcwd() + '/'
        caseexcelPath = '{}caseexcel/'.format(loaclPath)
        taskIdList = self.myReqClient.getTask(caseexcelPath)
        for taskId in taskIdList:
            if ".xls" not in taskId or urlFileName in taskId:
                continue
            taskId = '{}{}'.format(caseexcelPath, taskId)
            logger.info('---------------------开始运行task: {}'.format(taskId))

            # 开始执行Task
            TaskData = self.myReqClient.startTask(taskId)
            if TaskData is None:
                return False
            caseInfoList = TaskData['caseInfos']
            urlE = TaskData['url']
            # caseNum = TaskData['caseNum']

            urlFileNamePath = '{}{}'.format(caseexcelPath, urlFileName)
            urlList = self.myReqClient.getCfgUrl(caseInfoList, urlFileNamePath)

            browsertmp = None
            if len(caseInfoList) > 0:
                browsertmp = caseInfoList[0]['browser'].lower()
                if browsertmp == "android":
                    if self.startAndroidServer() is False:
                        return False
                    logger.debug('请启动Appium')
                elif browsertmp == "ios":
                    if self.startIOSServer() is False:
                        return False
            else:
                logger.error('任务id：{}不含任何用例，请检查任务对应用例列表!'.format(taskId))

            # 如果用例中没有正确的url，则使用"#url.xls"中的
            if "http" in urlE:
                urlList = []
                urlList.append([urlE, '0'])
            if (len(urlList) == 0 or urlList is None) and (browsertmp != "android" or browsertmp != "ios"):
                logger.warning("[{}]和[{}]中没有配置url地址".format(urlFileNamePath, taskId))
                continue
            for urlTmp in urlList:
                url = urlTmp[0]
                urlStatus = urlTmp[1]
                for caseInfo in caseInfoList:
                    startTimeCase = datetime.datetime.now()
                    #
                    caseId = int(str(caseInfo['caseId']).replace('.0', ''))
                    caseInfo['caseId'] = caseId
                    caseStr = caseInfo['caseName']
                    browserTmp = caseInfo['browser']
                    sheetName = caseInfo['sheetName']
                    browser = browserTmp.lower()
                    proPath = caseInfo['proPath']
                    caseStatus = caseInfo.get('caseStatus')

                    # url的状态不等于0且在用例状态中则不执行用例
                    if urlStatus != '0' and urlStatus in caseStatus:
                        continue
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
                    # Zd.commApp.CommApp.testAppLoginOK .../appWebCase.xls 用例  1    chrome   [输入参数]  [检查点]   [url]  .../cases/Zd/
                    case = self.__disposeTestCase(caseStr, taskId, sheetName, caseId, browser, paramsIn, checkPoint, url, proPath)
                    # case -> commApp.CommApp("testAppLoginOK", {"taskId": ".../appWebCase.xls", "sheetName": 用例, "caseId":1, "browserType": chrome, "params_in": [输入参数]， "checkPoint": [检查点], "url": [url], "proPath": "../cases/Zd/"})

                    caseInfo['taskId'] = taskId
                    caseInfo['url'] = url

                    # 创建测试套件
                    suite = unittest.TestSuite()
                    try:
                        # 添加测试集
                        logger.debug('--------------------------------------------------------------------------------------------')
                        logger.debug('--------用例：{} {} {} 添加测试集，浏览器：{}'.format(taskId.split('/')[-1], sheetName, caseId, browser))
                        # logger.debug(str(caseInfo))
                        suite.addTest(eval(case))

                        # 执行用例
                        # TODO
                        result.myRun(taskId, sheetName, caseId, browser, caseStr, caseInfo, self.retryCaseFile, startTimeCase)
                        suite.run(result)

                        # 判断是否重试
                        while result.retryNumLocal > 0:# and result.retryNumLocal < result.retryNumMax:
                            # 执行用例
                            suite.run(result)
                    except:
                        excstr = traceback.format_exc()
                        logger.error('--------用例：{} {} {} ，浏览器：{}  {}'.format(taskId, sheetName, caseId, browser, str(excstr)))
                    gc.collect()
                logger.info('---------------------结束运行task: {}'.format(taskId))
                logger.info('------------------------------------------------------------------------------------------------------------------')

        stopTime = datetime.datetime.now()
        totalTime = str(stopTime - startTime)
        logger.debug('合计耗时: {}'.format(totalTime))

        with open(reportName, 'wb') as f:
            runner = HTMLTestRunner(stream=f, title='测试用例', description='自动化测试用例执行报告')
            runner.run(result, totalTime)

        if platformSystem == "Windows":
            os.startfile(reportName)

        return True


def main():
    caseRunner = CaseRunner()
    caseRunner.run()


if __name__ == '__main__':
    main()
    gc.collect()

