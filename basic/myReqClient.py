# -*- coding:utf-8 -*-
import sys
import os
import requests
import traceback
import time
sys.path.append(os.getcwd())
import configparser
import basic.myGlobal as myGlobal
from basic.mySysCommon import MySysCommon


logger = myGlobal.getLogger()

requests.adapters.DEFAULT_RETRIES = 5  #增加重试连接次数
s = requests.session()
s.keep_alive = False  #关闭多余的连接


class MyReqClient(object):
    """客户端接口"""
    def __init__(self):
#        global logger
        self.maxNumberTimes = 3 #网络出错最大重试次数

        self.__ServerIP__ = 'http://127.0.0.1:8008'
        self.mySysCommon = MySysCommon()

        self.__getIPConf()


    def __getIPConf(self):
        """读取客户端和服务端IP配置文件"""
        fileName = '{}/conf/config.ini'.format(os.getcwd())
        cf = configparser.ConfigParser()
        # logger.debug('读取客户端和服务端IP配置文件:{}'.format(fileName))
        cf.read(fileName)
        sections =  cf.sections()
        if 'LOCAL' in sections:
            self.__ServerIP__ = cf.get('LOCAL', 'ServerIP')
        else:
            logger.info('找不到客户端和服务端IP配置文件')


    def checkTimmingTask(self):
        """
            checkTimmingTask接口: 检查是否存在定时任务
            接口类型:GET
            参数：无
            返回：
            code说明:
            0   '成功'
            250 'error'
        """
        NumberTimes = 1
        while 1 == 1:
            try:
                url = self.__ServerIP__ + '/checkTimmingTask'
                logger.debug('{}发起请求:{}'.format(sys._getframe().f_code.co_name, url))
                r = requests.get(url)
                resultstr = r.text
                json_result = eval(resultstr)
                logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name, json_result))
                if json_result['code'] == 0:
                    logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
                    return json_result['data']
                else:
                    logger.debug(json_result['msg'])
                    return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def getTask(self, loaclPath=''):
        """
            getTask接口: 获取一条未执行的任务
            接口类型:GET
            参数：ip
            返回：taskID
            code说明:
            0   '成功'
            201 '未找到与IP对应的终端'
            203 '没有未执行的测试任务'
        """
        NumberTimes = 1
        while 1==1:
            try:
                filelist = self.mySysCommon.mySysGetPathEachFile('{}'.format(loaclPath))
                logger.debug(filelist)
                return filelist
                # url = self.__ServerIP__ + '/getTestTask'
                # logger.debug('{}发起请求:{}'.format(sys._getframe().f_code.co_name, url))
                # r = requests.get(url)
                # resultstr = r.text
                # json_result = eval(resultstr)
                # logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name, json_result))
                # if json_result['code'] == 0:
                #     logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
                #     return json_result['data']['taskId']
                # else:
                #     logger.debug(json_result['msg'])
                #     return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def startTask(self, taskId):
        """
            startTask接口: 通知服务端开始执行某个任务，并获取该任务下的所有测试用例信息
            接口类型:POST
            参数：taskId
            返回：caseNum, caseInfos, browsers
            code说明:
            0   '成功'
            201 '该任务不存在'
            202 '该任务正在执行或已经执行完成'
            250 '系统出错'
        """
        NumberTimes = 1
        while 1==1:
            try:
                row = self.mySysCommon.mySysReadExcelRow(taskId, 'config', 1)
                proName = row[0]
                fileName = row[1]
                moduleName = row[2]
                type = row[3]
                browserType = row[4]
                url = row[5]
                taskData = {
                    'caseInfos': [],
                    'url': url
                }
                sheetNameList = self.mySysCommon.mySysReadExcelSheetName(taskId)
                sheetNameList.remove('config')
                for sheetName in sheetNameList:
                    casenumlist = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 0)
                    modulelist = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 1)
                    statuslist = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 7)
                    for numt in range(1, len(casenumlist)):
                        if statuslist[numt] != '无效':
                            caseStatus = '0'
                            caseStatusTmp = str(statuslist[numt]).replace(" ", "")
                            if caseStatusTmp != "":
                                caseStatus = caseStatusTmp.split(';')
                            casenum = casenumlist[numt]
                            case = {
                                'sheetName': sheetName,
                                'caseId': casenum,
                                'caseName': '{}.{}.{}.{}'.format(proName, fileName, moduleName, modulelist[numt]),
                                'browser': browserType,
                                'taskId': taskId,
                                'url': url,
                                'proPath': taskId.split('caseexcel')[0] + '/cases/' + proName + '/',
                                'caseStatus': caseStatus
                            }
                            taskData['caseInfos'].append(case)
                # logger.debug(taskData)
                return taskData
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def getCfgUrl(self, caseInfoList, urlFileNamePath):
        """
            getCfgUrl接口: 取“#url.xls”文件的url列表并返回
            参数：caseInfoList,urlFileNamePath
            返回：url列表
        """
        NumberTimes = 1
        while 1==1:
            try:
                if len(caseInfoList) != 0:
                    caseName = caseInfoList[0]['caseName']
                    caseNameList = caseName.split(".")
                    lFileName = caseNameList[1]
                    lModuleName = caseNameList[2]

                    returnUrlList = []
                    fileNameList = self.mySysCommon.mySysReadExcelCol(urlFileNamePath, 'config', 0)
                    moduleNameList = self.mySysCommon.mySysReadExcelCol(urlFileNamePath, 'config', 1)
                    urlList =  self.mySysCommon.mySysReadExcelCol(urlFileNamePath, 'config', 2)
                    typeList = self.mySysCommon.mySysReadExcelCol(urlFileNamePath, 'config', 3)
                    ModuleNameNum = 1
                    for numt in range(1, len(fileNameList)):
                        if lFileName == fileNameList[numt] and lModuleName == moduleNameList[numt]:
                            if typeList[numt] != '无效':
                                tmp = [urlList[numt], str(ModuleNameNum)]
                                returnUrlList.append(tmp)
                            ModuleNameNum = ModuleNameNum + 1
                    # logger.debug(returnUrlList)
                    return returnUrlList
                return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次处理失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1


    # """
    #     endTask接口:通知服务端某个任务执行完成
    #     接口类型:POST
    #     参数：taskId
    #     返回：无
    #     code说明:
    #     0   '成功'
    #     201 '该任务不存在'
    #     202 '该任务未开始或已经完成'
    #     250 '系统出错'
    # """
    # def endTask(self, taskId):
    #     NumberTimes = 1
    #     while 1==1:
    #         try:
    #             url = self.__ServerIP__ + '/endTask'
    #             data = {'taskId':taskId}
    #             logger.debug('{}发起请求:{}  ,  data:{}'.format(sys._getframe().f_code.co_name, url, data))
    #             r = requests.post(url, data=data)
    #             resultstr = r.text
    #             json_result = eval(resultstr)
    #             logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name,json_result))
    #             if json_result['code'] == 0:
    #                 logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
    #                 # logger.debug(json_result['data'])
    #                 return json_result['data']
    #             else:
    #                 logger.info(json_result['msg'])
    #                 return None
    #         except:
    #             if NumberTimes >= self.maxNumberTimes:
    #                 logger.error(traceback.format_exc())
    #                 return None
    #             logger.error('第{}次发起请求失败'.format(NumberTimes))
    #             NumberTimes = NumberTimes + 1
    #             time.sleep(3)


    def getParams(self, taskId, sheetName, caseId):
        """
            getParams接口: 获取用例的输入参数和检查点
            接口类型:GET
            参数：caseId
            返回：paramsIn, checkPoint
            code说明:
            0   '成功'
            201 'caseId有误'

        """
        NumberTimes = 1
        while 1==1:
            try:
                casenumList = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 0)
                paramsInList = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 4)
                checkPointList = self.mySysCommon.mySysReadExcelCol(taskId, sheetName, 6)
                for numt in range(1, len(casenumList)):
                    casenum = casenumList[numt]
                    # logger.debug(casenum)
                    if casenum == caseId:
                        paramsIn = paramsInList[numt]
                        checkPoint = checkPointList[numt]
                        # logger.debug(paramsIn)
                        # logger.debug(checkPoint)
                        caseData = {
                            'paramsIn': paramsIn,
                            'checkPoint': checkPoint,
                        }
                        # logger.debug(caseData)
                        return caseData
                return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def startCase(self, taskId, caseId, browserType):
        """
            startCase接口:通知服务端某个测试用例开始执行
            接口类型:POST
            参数：taskId,caseId,browerType
            返回：params_in, checkPoint
            code说明:
            0   '成功'
            201 '该任务不存在'
            202 '该测试用例正在执行或已经执行完成'
            212 '该项目不存在'
            213 '该模块不存在'
            214 '该测试用例不存在'
            215 '测试结果表中不存在该条测试项'
            250 '系统出错'
        """
        NumberTimes = 1
        while 1==1:
            try:
                return None
                # url = self.__ServerIP__ + '/startCase'
                # data = {'taskId':taskId,
                #         'caseId':caseId,
                #         'browserType':browserType
                #     }
                # logger.debug('{}发起请求:{}  ,  data:{}'.format(sys._getframe().f_code.co_name, url, data))
                # r = requests.post(url, data=data)
                # resultstr = r.text
                # json_result = eval(resultstr)
                # logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name,json_result))
                # if json_result['code'] == 0:
                #     logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
                #     logger.debug(json_result['data'])
                #     return json_result['data']
                # else:
                #     logger.info(json_result['msg'])
                #     return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def endCase(self, taskId, caseId, browserType, status, info):
        """
            endCase接口:提交某个用例的测试结果到服务端
            接口类型:POST
            参数：taskId,caseId,browerType,status,info
            返回：params_in, checkPoint
            code说明:
            0   '成功'
            201 '该任务不存在'
            202 '该测试用例未开始执行或已经执行完成'
            210 '用例运行状态有误'(2成功 3失败 4运行出错)
            212 '该项目不存在'
            213 '该模块不存在'
            214 '该测试用例不存在'
            215 '测试结果表中不存在该条测试项'
            250 '系统出错'
        """
        NumberTimes = 1
        while 1==1:
            try:
                return None
                # url = self.__ServerIP__ + '/endCase'
                # data = {'taskId':taskId,
                #         'caseId':caseId,
                #         'browserType':browserType,
                #         'status':status,
                #         'info':info
                #     }
                # logger.debug('{}发起请求:{}  ,  data:{}'.format(sys._getframe().f_code.co_name, url, data))
                # r = requests.post(url, data=data)
                # resultstr = r.text
                # json_result = eval(resultstr)
                # logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name,json_result))
                # if json_result['code'] == 0:
                #     logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
                #     # logger.debug(json_result['data'])
                #     return json_result['data']
                # else:
                #     logger.info(json_result['msg'])
                #     return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def uploadImg(self, taskId, caseId, browserType, imgPath):
        """
            uploadImg: 上传图片接口,用于测试用例运行的截图上传
            接口类型:POST
            参数：taskId, caseId, browser, file(要上传的图片文件)
            返回：
            code说明:
            0   '成功'
            201 '没有获取到文件'
            211 '该任务不存在'
            214 '该测试用例不存在'
            215 '测试结果表中不存在该条测试'
            250 'error'
            测试代码如下：
        """
        return None
        NumberTimes = 1
        while 1==1:
            try:
                url = self.__ServerIP__ + '/uploadImg'
                data = {'taskId':taskId,
                        'caseId':caseId,
                        'browserType':browserType
                    }
                with open(imgPath, 'rb') as f:
                    files = {'file': f}
                    logger.debug('{}发起请求:{}  ,  data:{}'.format(sys._getframe().f_code.co_name, url, data))
                    r = requests.post(url, data=data, files=files)
                    resultstr = r.text
                    json_result = eval(resultstr)
                    logger.debug('{}返回码:{}'.format(sys._getframe().f_code.co_name,json_result))
                    if json_result['code'] == 0:
                        logger.debug('{}成功'.format(sys._getframe().f_code.co_name))
                        # logger.debug(json_result['data'])
                        return json_result['data']
                    else:
                        logger.info(json_result['msg'])
                        return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


# def main():
#     b = MyReqClient()
#    b.getTask()
#    b.checkTimmingTask()
#    b.startTask("b1a0909e-fda5-11e6-b91f-e4b31894f0ab")
#    b.endTask("b1a0909e-fda5-11e6-b91f-e4b31894f0ab")
#    b.getParams('UFOAdmin-1')
#    b.startCase("b1a0909e-fda5-11e6-b91f-e4b31894f0ab", 'UFOAdmin-1', 'chrome')
#    b.endCase('b1a0909e-fda5-11e6-b91f-e4b31894f0ab', 'UFOAdmin-1', 'chrome', '2', '成功')

# if __name__ == '__main__':
#     main()
