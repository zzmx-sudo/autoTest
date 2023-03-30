# -*- coding:utf-8 -*-
import json
import os,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from appium.webdriver.common.touch_action import TouchAction
from basic.webTestCase import WebTestCase
import time
import datetime
from dateutil.relativedelta import relativedelta
import basic.myGlobal as myGlobal
import traceback
from basic.py_mybatis.mapper import PyMapper
import copy
import re


logger = myGlobal.getLogger()
# myFuncRunningTime = myGlobal.myFuncRunningTime


class PublicOperation(WebTestCase):
    """公共接口"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(PublicOperation, self).__init__(methodName, AllPirParams)
        logger.debug(AllPirParams)
        self.projectCasesPath = AllPirParams['proPath']
        # self.openDayDif = -150
        self.tabClickNumOfTimes = 1  # 1:点击列表第一个；  None：点击全部
        self.dateClickNumOfTimes = 1  # 1:点击日期第一个；  None：点击全部
        self.smokeCheck = None  # True:只做界面冒烟半自动测试（自动点击，人眼检查界面），不做界面和数据检查； None：不做界面冒烟测试，做界面和数据检查
        self.jsLogExclude = []
        # self.jsLogExclude = ['favicon.ico', '2.43241b8d504aab17c558.js', 'axios.min.map', ' 401', ' 403', ' 404', 'Error during WebSocket handshake']
        self.ipadLeftMenu = {
            0: '首页',
            1: '预警',
            2: '追踪',
            3: '我的'
        }
        self.ipadShouYeMenu = {
            0: '战区追踪',
            1: '新事业',
            2: '牛肉',
            3: '优鲜',
            4: '莲花',
            5: '虾',
            6: '榴莲',
            7: '馄饨',
            8: '肉鸡',
            9: '物流追踪',
            10: '山竹',
            11: '蛋鸡'
        }

        self.appBottomMenu = {
            0: '首页',
            1: '收藏',
            2: '我的'
        }
        self.appShouYeMenu = {
            0: '百人追踪:pad',
            1: '战区追踪:pad',
            2: '新零售:pad',
            3: '优鲜:pad',
            4: '榴莲:pad',
            5: '生虾:pad',
            6: '牛肉:pad',
            7: '馄饨:',
            8: '现代食品:',
            9: '蛋鸡:',
            10: '优鲜:',
            11: '猪产业链',
            12: '猪王:pad',
            13: '鸡王:pad',
            14: '新事业:pad',
            15: '水产:',
            16: '战房监控:'
        }

        logger.debug(AllPirParams)
        self.__getJsonConf()


    def __getJsonConf(self):
        """读取json配置文件"""
        fileName = '{}allData.json'.format(self.projectCasesPath)
        data = self.mySysJsonLoad(fileName)
        # logger.debug(data)
        self.params_in.update(data)

        fileName = '{}ipadApi.json'.format(self.projectCasesPath)
        data = self.mySysJsonLoad(fileName)
        # logger.debug(data)
        self.paramsApi.update(data)


    # def myFuncRunningTime(*args, **kwargs):
    #     """计算函数运行时间"""
    #     def handle_func(func):
    #         def inner(self, *args, **kwargs):
    #             startTime = time.perf_counter()  # datetime.datetime.now()
    #             func(self, *args, **kwargs)
    #             stopTime = time.perf_counter()  # datetime.datetime.now()
    #             totalTime = str(stopTime - startTime)
    #             logger.debug('{}函数运行用时间(秒): {} '.format(func, totalTime))
    #         return inner
    #     return handle_func


    ########################################################
    """ipad web"""
    ########################################################
    def ipadPbParameterDeal(self, paramsIn):
        """ipad 判断SIT、UAT、生产使用不同的用户名密码"""
        if ":15080/" in self.url or ":15443/" in self.url:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
            return userName, password
        else:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPasswordProd')
            return userName, password


    def ipadPbLoginOK(self, driver, userName, password, url):
        """ipad登录成功"""
        self.ipadPbwebLoginComm(driver, userName, password, url)

        time.sleep(1)

        cancel = "//span[text()='取消']/../.."
        if self.myWtEltNonexiContinue(driver, By.XPATH, cancel) is not None:
            self.myWtClickEx(driver, By.XPATH, cancel)

        self.ipadPbRefreshWaiting(driver)  # 判断等待

        self.myWtFindElement(driver, By.XPATH, "//span[text()='首页']")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        return True


    def ipadPbLoginPasswordError(self, driver, userName, password, url):
        """ipad登录失败"""
        password = '1'
        self.ipadPbwebLoginComm(driver, userName, password, url)

        self.myWtFindElement(driver, By.XPATH, "//p[text()='密码错误，请重新输入']")

        self.myWtGetJsLog(driver, self.jsLogExclude)


    def ipadPbwebLoginComm(self, driver, userName='', password='', url=''):
        """ipad登录"""
        logger.debug('打开网页{}'.format(url))
        driver.get(url)
        driver.maximize_window()  # 最大化窗口

        clientWidth = driver.execute_script("return document.body.clientWidth")
        clientHeight = driver.execute_script("return document.body.clientHeight")
        self.clientWidthProportion = round(1024/clientWidth, 1)
        logger.debug('width:{} height:{};  ipad横屏width 与 网页可见区域width比例：{}'.format(clientWidth, clientHeight, self.clientWidthProportion))
        # client_height = driver.execute_script("return document.body.clientHeight")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        self.ipadPbSwitchToFrame(driver)

        self.myWtSendKeysWebEx(driver, By.CLASS_NAME, "input-text", userName)
        self.myWtSendKeysWebEx(driver, By.CLASS_NAME, "psd", password)

        self.myWtClickEx(driver, By.CLASS_NAME, "login_button")


    def ipadPbSelectMainMenu(self, driver, menuStr1='', menuStr2='', menuStr3=''):
        """函数说明：选择主菜单
        输入参数：driver，menustr为菜单
        返回参数：无"""
        time.sleep(1)

        # self.ipadPbRefreshWaiting(driver)  # 判断界面
        # 左菜单
        if menuStr1 != '':
            menuLeft = self.myWtFindElement(driver, By.CLASS_NAME, 'cFoot')
            # self.ipadPbRefreshWaiting(driver)  # 判断界面
            self.myWtClickEx(menuLeft, By.XPATH, ".//span[text()='{}']".format(menuStr1))
            time.sleep(1)

        self.ipadPbRefreshWaiting(driver)  # 判断界面

        # 菜单
        if menuStr2 != '':
            contentTop = self.myWtFindElement(driver, By.CLASS_NAME, "content-top")
            self.myWtClickEx(contentTop, By.XPATH, ".//div[text()='{}']".format(menuStr2))
            time.sleep(1)

        self.ipadPbRefreshWaiting(driver)  # 判断等待

        logger.debug('单击菜单：{}-{}-{}'.format(menuStr1, menuStr2, menuStr3))


    def ipadPbRefreshWaiting(self, driver):
        """ipad判断界面是否在等待，加载中"""
        time.sleep(1)
        self.myWtJSRefreshWaiting(driver)

        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # CLASS_NAME   fistpageloading
                if driver.find_element(By.CLASS_NAME, "van-overlay").is_displayed():  # van-toast--loading
                    if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                        return None
                    continue
                else:
                    break
                    # return None
                # loading = self.myWtFindElement(driver, By.CLASS_NAME, "van-toast--loading", 1, 0, 1)
                # if loading is not None:
                #     styleStr = loading.get_attribute('style')
                #     # logger.debug(styleStr)
                #     if styleStr == 'display: none;':
                #         break
                # else:
                #     break
                # if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                #     return None
            except:
                break
                # return None
                # if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                #     logger.error('{}'.format(traceback.format_exc()))
                #     return None
                # time.sleep(0.1)
        performanceList = self.myPbPerformanceNetworkLog(driver, 0, 30)

        return performanceList


    def ipadPbLeftBack(self, driver, maxWaittime=None):
        """ 关闭窗口x 或 退回< """
        # self.myPbKeyboardListener()

        self.myWtGetJsLog(driver, self.jsLogExclude)
        arrowLeft = "//i[contains(@class, 'van-icon-arrow-left')]"
        if maxWaittime is None:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        else:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft, 0, maxWaittime):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        self.myWtGetJsLog(driver, self.jsLogExclude)


    def ipadPbCloseTopRight(self, driver, maxWaittime=None):
        """ 关闭窗口x 或 退回< """
        # time.sleep(1)
        self.myWtGetJsLog(driver, self.jsLogExclude)
        arrowLeft = "//i[contains(@class, 'van-popup__close-icon')]"
        if maxWaittime is None:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        else:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft, 0, maxWaittime):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        self.myWtGetJsLog(driver, self.jsLogExclude)


    def ipadPbSelectShowDate(self, driver, datetype, date, maxWaittime=-1):
        """ 日期控件
        datetype：类型，如：年、月、周、日
        date：日期，如'2021-10'、'2021-01-09'
        例：self.ipadSelectShowDate(driver, '月', '2021-10')
        例：self.ipadSelectShowDate(driver, '日', '2021-01-09')
        例：self.ipadSelectShowDate(driver, '', '2021-01-09')
        """
        logger.debug("def ipadPbSelectShowDate:{} {} {}".format(datetype, date, maxWaittime))
        showDate = "//div[contains(@class, 'showDate')]"
        shdate = "//div[contains(@class, 'date')]"
        # showDateElt = self.myWtFindElement(driver, By.XPATH, showDate)
        if self.myWtEltNonexiContinue(driver, By.XPATH, showDate, 0, 0):
            self.myWtClickEx(driver, By.XPATH, showDate)
        else:
            self.myWtClickEx(driver, By.XPATH, shdate)
        if '' == datetype:
            self.myWtFindElement(driver, By.CLASS_NAME, "calendar-info")  # 判断点击后控件显示出来
        else:
            self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '确定')]")  # 判断点击后控件显示出来
        dType = None
        if '日' in datetype:
            dType = '当日'
            if self.myWtEltNonexiContinue(driver, By.XPATH, "//p[text()='{}']".format(dType), 0, 0) is None:
                pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
                self.myWtClickEx(pickerdates, By.XPATH, ".//span[contains(text(), '{}')]".format(dType))
            else:
                self.myWtClickEx(driver, By.XPATH, "//p[text()='{}']".format(dType))
            if len(date) == 10 and date[4] == '-' and date[7] == '-':
                year = date[0:4]
                month = date[5:7]
                day = date[8:11]
                if day[0] == '0':
                    day = day[1]
                self.__ipadPbShowDate(driver, dType, year, month, day)
        elif '周' in datetype:
            dType = '周累计'
            if self.myWtEltNonexiContinue(driver, By.XPATH, "//p[text()='{}']".format(dType), 0, 0) is None:
                pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
                self.myWtClickEx(pickerdates, By.XPATH, ".//span[contains(text(), '{}')]".format(dType))
            else:
                self.myWtClickEx(driver, By.XPATH, "//p[text()='{}']".format(dType))
            if len(date) == 10 and date[4] == '-' and date[7] == '-':
                year = date[0:4]
                month = date[5:7]
                day = date[8:11]
                if day[0] == '0':
                    day = day[1]
                self.__ipadPbShowDate(driver, dType, year, month, day)
        elif '月' in datetype:
            dType = '月累计'
            if self.myWtEltNonexiContinue(driver, By.XPATH, "//p[text()='{}']".format(dType), 0, 0) is None:
                pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
                self.myWtClickEx(pickerdates, By.XPATH, ".//span[contains(text(), '{}')]".format(dType))
            else:
                self.myWtClickEx(driver, By.XPATH, "//p[text()='{}']".format(dType))
            if len(date) == 10 and date[4] == '-':
                year = date[0:4]
                month = date[5:7]
                if month[0] == '0':
                    month = month[1]
                self.__ipadPbShowDate(driver, dType, year, month)
        elif '年' in datetype:
            dType = '年累计'
            if self.myWtEltNonexiContinue(driver, By.XPATH, "//p[text()='{}']".format(dType), 0, 0) is None:
                pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
                self.myWtClickEx(pickerdates, By.XPATH, ".//span[contains(text(), '{}')]".format(dType))
            else:
                self.myWtClickEx(driver, By.XPATH, "//p[text()='{}']".format(dType))
            if len(date) == 10 and date[4] == '-':
                year = date[0:4]
                month = date[5:7]
                if month[0] == '0':
                    month = month[1]
                self.__ipadPbShowDate(driver, dType, year, month)
        elif '' == datetype:
            if len(date) == 10 and date[4] == '-' and date[7] == '-':
                year = date[0:4]
                month = date[5:7]
                day = date[8:11]
                if day[0] == '0':
                    day = day[1]
                self.__ipadPbShowDate(driver, datetype, year, month, day)
        else:
            err = '日期控件没有找到：{} {}'.format(dType, date)
            self.mySysAssert(err)
            return None


    def __ipadPbShowDate(self, driver, dType, year, month, day=None, maxWaittime=-1):
        """ 日期控件选择点击日期
        由def ipadPbSelectShowDate调用"""
        time.sleep(1)
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        d1 = datetime.datetime.now()
        logger.debug("def __ipadPbShowDate:{} {} {} {} {}".format(dType, year, month, day, maxWaittime))
        if '日' in dType or '周' in dType:
            pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
            showDate = "//div[contains(@class, 'calendar-info')]"
            while 1 == 1:
                dateElt = self.myWtFindElement(pickerdates, By.XPATH, showDate)
                text = self.mySysStringCleanup(dateElt.text)
                logger.debug(text)
                if text == '{}年{}月'.format(year, month):
                    self.myWtClickEx(driver, By.XPATH, "//span[text()='{}']".format(day))
                    self.myWtClickEx(driver, By.XPATH, "//div[text()='确定']")
                    logger.debug('日期控件点击选择：{} {}-{}-{}'.format(dType, year, month, day))
                    break
                else:
                    # 点击上个月
                    self.myWtClickEx(driver, By.XPATH, "//div[contains(@class, 'calendar-prev')]")
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    err = '日期控件没有找到：{} {}-{}'.format(dType, year, month)
                    self.mySysAssert(err)
                    break
        elif '' == dType:
            while 1 == 1:
                calendar = self.myWtFindElement(driver, By.CLASS_NAME, "calendar")
                calendarinfo = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'calendar-info')]")
                text = self.mySysStringCleanup(calendarinfo.text)
                logger.debug("当前状态为: {}".format(text))
                if text == '{}年{}月'.format(year, month):
                    xpathday = ".//span[text()='{}']/..".format(day)
                    logger.debug(xpathday)
                    father = self.myWtFindElement(calendar, By.XPATH, xpathday)
                    outerHTML = self.myPbStringCleanup(father.get_attribute("outerHTML"))
                    logger.debug(outerHTML)
                    fatherClass = father.get_attribute("class")
                    logger.debug(fatherClass)
                    # 判断如果日期无数据则选择往前一天，直到有数据
                    if "disabled" in fatherClass:
                        localDate = '{}-{}-{}'.format(year, month, day)
                        timelast = (datetime.datetime.strptime(localDate, '%Y-%m-%d').date() + relativedelta(days=-1)).strftime("%Y-%m-%d")
                        year = timelast[0:4]
                        month = timelast[5:7]
                        day = timelast[8:11]
                        if day[0] == '0':
                            day = day[1]
                        logger.debug('当前日期{}状态为disabled，取上一天{}-{}-{}'.format(localDate, year, month, day))
                        continue
                    else:
                        self.myWtClickEx(calendar, By.XPATH, xpathday)
                        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "showDate", 0, 0):
                            self.myWtClickEx(driver, By.CLASS_NAME, "showDate")
                        logger.debug('日期控件点击选择：{} {}-{}-{}'.format(dType, year, month, day))
                        break
                else:
                    # 点击上个月
                    self.myWtClickEx(driver, By.XPATH, "//div[contains(@class, 'calendar-prev')]")

                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    err = '日期控件没有找到：{} {}-{}'.format(dType, year, month)
                    self.mySysAssert(err)
                    break
        else:
            pickerdates = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'picker_dates')]")
            showDate = ".//span[contains(@class, 'showDate')]"
            while 1 == 1:
                dateElt = self.myWtFindElement(pickerdates, By.XPATH, showDate)
                text = dateElt.text
                logger.debug(text)
                logger.debug('{}年{}月'.format(year, month))
                if '{}年'.format(year) in text:
                    checkmonth = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}月')]".format(month))
                    if "none;" in checkmonth.get_attribute('style'):
                        self.myWtClickEx(driver, By.CLASS_NAME, "spanBGd")
                    else:
                        self.myWtClickEx(driver, By.XPATH, "//span[contains(text(), '{}月')]".format(month))
                    self.myWtClickEx(driver, By.XPATH, "//div[text()='确定']")
                    logger.debug('日期控件点击选择：{} {}-{}'.format(dType, year, month))
                    break
                self.myWtClickEx(driver, By.XPATH, "//div[contains(@class, 'left')]")
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    err = '日期控件没有找到：{} {}-{}'.format(dType, year, month)
                    self.mySysAssert(err)
                    break


    # @myFuncRunningTime()
    def ipadPbGetCheckTextSize(self, driver, paramsIn, checkPoint, uiPath, inputList=None, trby=None, trCtrlIdent=None, tdby=None, tdCtrlIdent=None, excludeTextList=[], tableWidth='N', tagList=['div', 'span', 'li', 'th', 'td', 'p'], tagType=By.TAG_NAME, onlynum=True, uiJsonRecord=None):
        """取和检查控件中文本大小
        uiPath为记录控件大小的文件名，一定要唯一，否则会与其它冲突覆盖，文件保存在当前项目autoTest/cases/Zd/uiJson目录中，表格和非表格中的非数字会保存文件，其它情况不会保存文件
        inputList为输入的要查找的控件列表，可选，默认为None
        trby为表中行的By.Class等, trCtrlIdent为表中行的Class名等，可选，默认为None
        tdby为表中列的By.Class等, tdCtrlIdent为表中列的Class名等，可选，默认为None
        excludeTextList为排除的文本名列表，查到对应的文本名则不处理不检查。也可填写控件宽和高，例excludeTextList=['width:590,height:66']，也不处理。可选，默认为空列表[]
        tableWidth为N记录width，但不对比；为其它则不记录width，手工记录width，软件对比width ，可选，默认为N
        tagList为要查的控件标识，即在inputList、trby和tdby之内部查控件标识名，可选，默认为['div', 'span', 'li', 'th', 'td', 'p'],如果为[]只适用表格情况
        tagType为By.ID、By.TAG_NAME等，与tagList一起使用，默认为By.TAG_NAME
        onlynum为True时，只检查数字长度，为None时，全部检查
        uiJsonRecord为True时记录uiJson目录相关文件内容并检查，为None不记录不检查"""
        if self.smokeCheck is True:
            return None

        # if self.tabClickNumOfTimes == 1:
        logger.debug('**开始检查界面控件:{}'.format(uiPath))
        uiPath = self.myPbStringCleanup(uiPath)
        logger.debug('uiPath:{}'.format(uiPath))
        clientWidthPro = self.clientWidthProportion
        data = {}
        fileName = '{}uiJson/P{}{}-{}.json'.format(self.projectCasesPath, clientWidthPro, self.browserHeadless, uiPath)
        if os.path.exists(fileName):
            data = self.mySysJsonLoad(fileName)

        logger.debug('开始计算控件数量')
        eltNum = 0
        eltList = []
        if inputList is None:
            if trby is None and trCtrlIdent is None:
                if tdby is None and tdCtrlIdent is None:
                    logger.warning('inputList、trby和tdby都是None')
                elif tdby is not None and tdCtrlIdent is not None:
                    tdList = self.myWtFindElements(driver, tdby, tdCtrlIdent)
                    tdNum = 1
                    for td in tdList:
                        eltTmpList = []
                        for tag in tagList:
                            tmpList = self.myWtFindElements(td, tagType, tag)
                            eltTmpList = eltTmpList + tmpList
                            eltNum = eltNum + len(tmpList)
                        eltList.append([eltTmpList, 0, tdNum])
                        tdNum = tdNum + 1
            elif trby is not None and trCtrlIdent is not None:
                if tdby is None and tdCtrlIdent is None:
                    trList = self.myWtFindElements(driver, trby, trCtrlIdent)
                    trNum = 1
                    for tr in trList:
                        eltTmpList = []
                        for tag in tagList:
                            tmpList = self.myWtFindElements(tr, tagType, tag)
                            eltTmpList = eltTmpList + tmpList
                            eltNum = eltNum + len(tmpList)
                        eltList.append([eltTmpList, trNum, 0])
                        trNum = trNum + 1
                elif tdby is not None and tdCtrlIdent is not None:
                    trList = self.myWtFindElements(driver, trby, trCtrlIdent)
                    trNum = 1
                    for tr in trList:
                        tdList = self.myWtFindElements(tr, tdby, tdCtrlIdent)
                        tdNum = 1
                        for td in tdList:
                            eltTmpList = []
                            if len(tagList) == 0:
                                tmpList = []
                                tmpList.append(td)
                                eltTmpList = eltTmpList + tmpList
                                eltNum = eltNum + 1
                            else:
                                for tag in tagList:
                                    tmpList = self.myWtFindElements(td, tagType, tag)
                                    eltTmpList = eltTmpList + tmpList
                                    eltNum = eltNum + len(tmpList)
                            eltList.append([eltTmpList, trNum, tdNum])
                            tdNum = tdNum + 1
                        trNum = trNum + 1
        # inputList is not None
        else:
            if trby is None and trCtrlIdent is None:
                if tdby is None and tdCtrlIdent is None:
                    for inpt in inputList:
                        eltTmpList = []
                        for tag in tagList:
                            tmpList = self.myWtFindElements(inpt, tagType, tag)
                            eltTmpList = eltTmpList + tmpList
                            eltNum = eltNum + len(tmpList)
                        eltList.append([eltTmpList, 0, 0])
                elif tdby is not None and tdCtrlIdent is not None:
                    for inpt in inputList:
                        tdList = self.myWtFindElements(inpt, tdby, tdCtrlIdent)
                        tdNum = 1
                        for td in tdList:
                            eltTmpList = []
                            for tag in tagList:
                                tmpList = self.myWtFindElements(td, tagType, tag)
                                eltTmpList = eltTmpList + tmpList
                                eltNum = eltNum + len(tmpList)
                            eltList.append([eltTmpList, 0, tdNum])
                            tdNum = tdNum + 1
            elif trby is not None and trCtrlIdent is not None:
                if tdby is None and tdCtrlIdent is None:
                    for inpt in inputList:
                        trList = self.myWtFindElements(inpt, trby, trCtrlIdent)
                        trNum = 1
                        for tr in trList:
                            eltTmpList = []
                            for tag in tagList:
                                tmpList = self.myWtFindElements(tr, tagType, tag)
                                eltTmpList = eltTmpList + tmpList
                                eltNum = eltNum + len(tmpList)
                            eltList.append([eltTmpList, trNum, 0])
                            trNum = trNum + 1
                elif tdby is not None and tdCtrlIdent is not None:
                    for inpt in inputList:
                        trList = self.myWtFindElements(inpt, trby, trCtrlIdent)
                        trNum = 1
                        for tr in trList:
                            tdList = self.myWtFindElements(tr, tdby, tdCtrlIdent)
                            tdNum = 1
                            for td in tdList:
                                eltTmpList = []
                                if len(tagList) == 0:
                                    tmpList = []
                                    tmpList.append(td)
                                    eltTmpList = eltTmpList + tmpList
                                    eltNum = eltNum + 1
                                else:
                                    for tag in tagList:
                                        tmpList = self.myWtFindElements(td, tagType, tag)
                                        eltTmpList = eltTmpList + tmpList
                                        eltNum = eltNum + len(tmpList)
                                eltList.append([eltTmpList, trNum, tdNum])
                                tdNum = tdNum + 1
                            trNum = trNum + 1
        logger.debug('结束计算控件数量：{}'.format(eltNum))

        if eltList:
            ifChanger = self.__ipadPbCheckTextSize(driver, paramsIn, checkPoint, data, eltList, trby, trCtrlIdent, tdby, tdCtrlIdent, excludeTextList, tableWidth, onlynum, uiJsonRecord)
            # 如果有变动则写文件
            if ifChanger == 1:
                if os.path.exists(fileName):
                    self.mySysCopyFile(fileName, '{}.bak'.format(fileName))
                self.mySysJsonWrite(data, fileName)
        else:
            logger.debug('没有可检查的控件')

        logger.debug('**结束检查界面控件:{}'.format(uiPath))


    # @myFuncRunningTime()
    def __ipadPbCheckTextSize(self, driver, paramsIn, checkPoint, data, eltList, trby=None, trCtrlIdent=None, tdby=None, tdCtrlIdent=None, excludeTextList=[], tableWidth='N', onlynum=True, uiJsonRecord=None):
        """def ipadPbGetCheckTextSize调用"""
        self.ifChangerCheckTextSize = 0
        n = 500000  # 50
        for eltL in eltList:
            # logger.debug(eltL)
            eltTList = eltL[0]
            RowNum = eltL[1]
            columnNum = eltL[2]

            if len(eltTList) > n:
                threadinglist = []
                for i in range(0, len(eltTList), n):
                    logger.debug('线程开始区间：{}'.format(i))
                    eltRan = eltTList[i:i + n]
                    pp = self.mySysThreading(self.__ipadPbCheckTextSizeTmp, driver, paramsIn, checkPoint, data, eltRan, RowNum, columnNum, trby, trCtrlIdent, tdby, tdCtrlIdent, excludeTextList, tableWidth, onlynum, uiJsonRecord)
                    threadinglist.append(pp)
                for p in threadinglist:
                    p.join()
                    if p.exit_code != 0:
                        self.mySysAssert(p.exception)
                threadinglist.clear()
            else:
                self.__ipadPbCheckTextSizeTmp(driver, paramsIn, checkPoint, data, eltTList, RowNum, columnNum, trby, trCtrlIdent, tdby, tdCtrlIdent, excludeTextList, tableWidth, onlynum, uiJsonRecord)
        return self.ifChangerCheckTextSize


    def __ipadPbCheckTextSizeTmp(self, driver, paramsIn, checkPoint, data, eltTList, RowNum, columnNum, trby=None, trCtrlIdent=None, tdby=None, tdCtrlIdent=None, excludeTextList=[], tableWidth='N', onlynum=True, uiJsonRecord=None):
        """def __ipadPbCheckTextSize调用"""
        clientWidthPro = self.clientWidthProportion
        for elt in eltTList:
            # outerHTML = self.myPbStringCleanup(elt.get_attribute("outerHTML"))
            # logger.debug(outerHTML)
            try:
                if not elt.is_displayed():
                    if len(elt.get_attribute("textContent")) == 0:
                        # logger.debug("控件not displayed，不用处理: {}".format(outerHTML))
                        continue
                if not elt.is_enabled():
                    # logger.debug("控件not enabled，不用处理: {}".format(outerHTML))
                    continue
                if 'display: none;' in elt.get_attribute('style'):
                    # logger.debug("控件display: none，不用处理: {}".format(outerHTML))
                    continue
            except:
                logger.debug("except")
                # logger.error('{}'.format(traceback.format_exc()))
                continue

            # fontfamily = str(elt.value_of_css_property('font-family'))
            # if onlynum is True and fontfamily not in ['childishAL', 'ChildishAL', 'Bebas', 'Arial']:
            #     continue

            innerHTML = self.myPbStringCleanup(elt.get_attribute("innerHTML"))
            # 判断为根节点
            if ('<' not in innerHTML) and ('>' not in innerHTML):
                # text = self.myPbStringCleanup(elt.text)
                text = self.myPbStringCleanup(elt.get_attribute("textContent"))
                # 为空
                if len(text) == 0 or text == '':
                    continue

                # if text == '/':
                #     continue

                fontfamily = str(elt.value_of_css_property('font-family'))
                if onlynum is True and fontfamily not in ['childishAL', 'ChildishAL', 'Bebas', 'Arial']:
                    continue

                # width = float(elt.size['width']) / clientWidthPro
                width = float(elt.size['width'])
                # 如果取width宽度为0则不处理
                if width == 0:
                    continue
                # fontSize = round(float(str(elt.value_of_css_property('font-size')).replace('px', '')) / clientWidthPro)
                fontSize = round(float(str(elt.value_of_css_property('font-size')).replace('px', '')))
                if fontSize == 0:
                    continue
                # height = float(elt.size['height']) / clientWidthPro
                height = float(elt.size['height'])

                # 排除
                if len(excludeTextList) != 0:
                    if text in excludeTextList:
                        continue
                    ifcon = None
                    for excludeText in excludeTextList:
                        if excludeText in text:
                            ifcon = True
                            break
                        elif "width:" in excludeText and ",height:" in excludeText:
                            exlist = excludeText.replace(" ", "").replace("width:", "").split(",height:")
                            if len(exlist) == 2:
                                widthex = int(exlist[0])
                                heightex = int(exlist[1])
                                logger.debug("[{}] widthex:{},heightex:{}".format(text, widthex, heightex))
                                if width == widthex and height == heightex:
                                    ifcon = True
                                    break
                            else:
                                logger.warning("参数excludeTextList错误：{}".format(excludeTextList))
                    if ifcon is True:
                        continue

                x = None
                y = None
                if self.browserHeadless == 'UI':
                    x = float(elt.location['x']) / clientWidthPro
                    y = float(elt.location['y']) / clientWidthPro
                else:
                    x = float(elt.location['x'])
                    y = float(elt.location['y'])

                rectangle = [x, y, width, height]

                textMaxNum = width / fontSize  # PingFang、Microsoft YaHei字体有时精度不准确
                logger.debug('x:{},y:{},width:{},height:{},fontSize:{},text:[{}],len:{},fontfamily:{}'.format(x, y, width, height, fontSize, text, len(text), fontfamily))

                chRst, quanJiaoNum, alpRst, numRst = self.mySysGetAllCharacterNum(text)

                logger.debug('[{}] 实际宽度:{}'.format(text, textMaxNum))
                logger.debug('[{}] trby:{} trCtrlIdent:{} ; tdby:{} tdCtrlIdent:{}'.format(text, trby, trCtrlIdent, tdby, tdCtrlIdent))

                # 不是表格
                if (trby is None and trCtrlIdent is None) and (tdby is None and tdCtrlIdent is None):
                    logger.debug('[{}] chRst:{} alpRst:{}'.format(text, chRst, alpRst))
                    # 有中文或英文
                    if chRst != 0 or alpRst != 0:
                        if onlynum is None:
                            self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "文字太长")

                        if uiJsonRecord is not None:
                            key = '{}'.format(text)
                            logger.debug("[{}] key:{}".format(text, key))
                            outerHTML = self.myPbStringCleanup(elt.get_attribute("outerHTML"))
                            # if data.get(key) is not None:
                            if key in data:
                                dataheight = data[key]['height']
                                datawidth = data[key]['width']
                                if dataheight != height or datawidth != width:
                                    picFilename = self.myWtScreenshotAsFile(driver, rectangle)
                                    err = '大小变动{}：\nx:{},y:{},width:{},height:{}  原始值：width:{},height:{}\n{}'.format(outerHTML, x, y, width, height, datawidth, dataheight, picFilename)
                                    self.mySysAssert(err)
                            else:
                                logger.debug('添加{}：x:{},y:{},width:{},height:{}'.format(outerHTML, x, y, width, height))
                                data[key] = {}
                                data[key]['outerHTML'] = outerHTML
                                data[key]['height'] = height
                                data[key]['width'] = width
                                data[key]['x'] = x
                                data[key]['y'] = y
                                self.ifChangerCheckTextSize = 1
                    # 没有中文和英文，只有数字
                    elif numRst != 0 and text.find('-') <= 0:
                        self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "数字太长")
                    # 没有中文、英文、数字
                    else:
                        if onlynum is None:
                            self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "字符太长")

                # 是表格
                elif (trby is not None and trCtrlIdent is not None) or (tdby is not None and tdCtrlIdent is not None):
                    # 有中文或英文
                    if chRst != 0 or alpRst != 0:
                        if height < (fontSize * 2):
                            if onlynum is None:
                                self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "表格 文字太长")
                    # 没有中文和英文，只有数字
                    elif numRst != 0 and text.find('-') <= 0:
                        self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "表格 数字太长")
                    # 没有中文、英文、数字
                    else:
                        if onlynum is None:
                            self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "表格 字符太长")

                    if uiJsonRecord is not None:
                        key = 'r{}c{}'.format(RowNum, columnNum)
                        logger.debug("[{}] key:{}".format(text, key))
                        outerHTML = self.myPbStringCleanup(elt.get_attribute("outerHTML"))
                        # if data.get(key) is not None:
                        if key in data:
                            # 为N记录width，但不对比；为其它则不记录width，手工记录width，软件对比width
                            if tableWidth == 'N':
                                # 判断高度不相同
                                if (height < (fontSize * 2)) and (data[key]['height'] != height):
                                # if data[key]['height'] != height:
                                    picFilename = self.myWtScreenshotAsFile(driver, rectangle)
                                    err = '表格 大小变动{}：\nheight:{}  原始值：height:{}\n{}'.format(outerHTML, height, data[key]['height'], picFilename)
                                    self.mySysAssert(err)
                            else:
                                if (height < (fontSize * 2)) and (data[key]['height'] != height):
                                # if data[key]['height'] != height:
                                    picFilename = self.myWtScreenshotAsFile(driver, rectangle)
                                    err = '表格 大小变动{}：\nheight:{}  原始值：height:{}\n{}'.format(outerHTML, height, data[key]['height'], picFilename)
                                    self.mySysAssert(err)
                                # 判断现在的宽大于记录
                                if data[key]['width'] > width:
                                    picFilename = self.myWtScreenshotAsFile(driver, rectangle)
                                    err = '表格 数字太长{}：\nwidth:{}  最大值：width:{}\n{}'.format(outerHTML, width, data[key]['width'], picFilename)
                                    self.mySysAssert(err)
                        else:
                            logger.debug('添加{}：x:{},y:{},height:{}'.format(outerHTML, x, y, height))
                            data[key] = {}
                            data[key]['height'] = height
                            if tableWidth == 'N':
                                data[key]['width'] = width
                            self.ifChangerCheckTextSize = 1
            # 非根节点
            else:
                fontfamily = str(elt.value_of_css_property('font-family'))
                if onlynum is True and fontfamily not in ['childishAL', 'ChildishAL', 'Bebas', 'Arial']:
                    continue

                # 如果是大屏
                if "inner-content" in elt.get_attribute("class"):
                    # text = self.myPbStringCleanup(elt.text)
                    text = self.myPbStringCleanup(elt.get_attribute("textContent"))
                    # 为空
                    if len(text) == 0 or text == '':
                        continue

                    if text == '/':
                        continue

                    # width = float(elt.size['width']) / clientWidthPro
                    width = float(elt.size['width'])
                    # 如果取width宽度为0则不处理
                    if width == 0:
                        continue
                    # fontSize = round(float(str(elt.value_of_css_property('font-size')).replace('px', '')) / clientWidthPro)
                    fontSize = round(float(str(elt.value_of_css_property('font-size')).replace('px', '')))
                    if fontSize == 0:
                        continue
                    # height = float(elt.size['height']) / clientWidthPro
                    height = float(elt.size['height'])

                    # 排除
                    if len(excludeTextList) != 0:
                        if text in excludeTextList:
                            continue
                        ifcon = None
                        for excludeText in excludeTextList:
                            if excludeText in text:
                                ifcon = True
                                break
                            elif "width:" in excludeText and ",height:" in excludeText:
                                exlist = excludeText.replace(" ", "").replace("width:", "").split(",height:")
                                if len(exlist) == 2:
                                    widthex = int(exlist[0])
                                    heightex = int(exlist[1])
                                    logger.debug("[{}] widthex:{},heightex:{}".format(text, widthex, heightex))
                                    if width == widthex and height == heightex:
                                        ifcon = True
                                        break
                                else:
                                    logger.warning("参数excludeTextList错误：{}".format(excludeTextList))
                        if ifcon is True:
                            continue

                    x = None
                    y = None
                    if self.browserHeadless == 'UI':
                        x = float(elt.location['x']) / clientWidthPro
                        y = float(elt.location['y']) / clientWidthPro
                    else:
                        x = float(elt.location['x'])
                        y = float(elt.location['y'])

                    rectangle = [x, y, width, height]

                    textMaxNum = width / fontSize
                    logger.debug('x:{},y:{},width:{},height:{},fontSize:{},text:[{}],len:{},fontfamily:{}'.format(x, y, width, height, fontSize, text, len(text), fontfamily))
                    logger.debug(innerHTML)

                    chRst, quanJiaoNum, alpRst, numRst = self.mySysGetAllCharacterNum(text)

                    logger.debug('[{}] 实际宽度:{}'.format(text, textMaxNum))
                    logger.debug('[{}] trby:{} trCtrlIdent:{} ; tdby:{} tdCtrlIdent:{}'.format(text, trby, trCtrlIdent, tdby, tdCtrlIdent))
                    logger.debug('[{}] chRst:{} alpRst:{}'.format(text, chRst, alpRst))
                    # 有中文或英文
                    if chRst != 0 or alpRst != 0:
                        if onlynum is None:
                            self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, "文字太长")
                    # 没有中文和英文，只有数字
                    elif numRst != 0 and text.find('-') <= 0:
                        self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, '数字太长')
                    # 没有中文、英文、数字
                    else:
                        if onlynum is None:
                            self.__ipadPbCheckTextLen(textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, '字符太长')


    def myPbStringCleanup(self, text):
        """处理字符串，并删除空格"""
        return self.mySysStringCleanup(str(text)).replace(' ', '').replace(u'\xa0', u' ')


    def __ipadPbCheckTextLen(self, textMaxNum, text, fontfamily, chRst, quanJiaoNum, alpRst, numRst, driver, rectangle, fontSize, textYpe):
        """判断字符串宽度"""
        x, y, width, height = rectangle
        textMaxNumDifStd = None
        if 'PingFang' in fontfamily:
            textMaxNumDifStd = 0.4
            # if numRst != 0 or alpRst != 0:
            #     if fontSize*2 <= height:
            #         picFilename = self.myWtScreenshotAsFile(driver, rectangle)
            #         err = '{}：[{}]\n{}'.format(textYpe, text, picFilename)
            #         self.mySysAssert(err)
            #     return None
            # else:
            #     textMaxNumDifStd = 0.16
        elif 'Bebas' in fontfamily:
            textMaxNumDifStd = 0.11  # 0.16 0.23 0.09
        elif 'childishAL' in fontfamily:
            textMaxNumDifStd = 0.2  # 0.1
        elif 'ChildishAL' in fontfamily:
            textMaxNumDifStd = 0.4
        elif 'Microsoft YaHei' in fontfamily:
            textMaxNumDifStd = 0.4  # 0.2 0.3
        elif 'Arial' in fontfamily:
            textMaxNumDifStd = 0.2  # 0.1
        else:
            textMaxNumDifStd = 0.34

        numLen = self.ipadPbGetStrStdWidth(text, chRst, quanJiaoNum, fontfamily)
        # logger.debug('textMaxNum:{}'.format(textMaxNum))
        textMaxNumDif = abs(textMaxNum - numLen)
        if (textMaxNum < numLen) and (textMaxNumDif > textMaxNumDifStd):  # and (round(textMaxNum) < round(numLen))
            picFilename = self.myWtScreenshotAsFile(driver, rectangle)
            err = '{}：{}      {}<{}\n{}'.format(textYpe, text, textMaxNum, numLen, picFilename)
            self.mySysAssert(err)
        else:
            logger.debug("[{}] 宽度正常".format(text))


    def ipadPbGetStrStdWidth(self, string, ChineseNum, quanJiaoNum, fontfamily='Bebas'):
        """计算字符串宽度"""
        text = str(string)
        logger.debug('[{}] 计算标准宽度'.format(text))

        # 计算半角字符
        # allCharwidthBebasList = (0.517901761475394, 0.3409658724663787, 0.5299750402544267, 0.5278934415602029, 0.5499584004240444, 0.5079100813905851, 0.49708577453315694, 0.4958368026115526, 0.5283097549465126, 0.49708577453315694, 0.22689425767038435, 1, 0.8197336039005073, 0.5370524631097171, 0.7102414998792701, 0.37926727573502483, 0.6194837841060462, 0.44462949379125455, 0.3588676339417728, 0.35803497540647805, 0.4900083516778665, 0.7789342567886525, 0.5499584004240444, 0.5499584004240444, 0.3809325610429389, 0.3809325610429389, 0.3184846002162276, 0.31765197344360824, 0.22023314820140358, 0.5732722676841395, 0.21690259346691318, 0.3759367368818721, 0.22689425767038435, 0.22731058693803172, 0.5732722676841395, 0.51623647616748, 0.22689425767038435, 0.5378850898823364, 0.22731058693803172, 0.5378850898823364, 0.5774354650725869, 0.5449625762629777, 0.517901761475394, 0.5141548774732563, 0.4746045022830058, 0.4746045022830058, 0.517901761475394, 0.5228975856364608, 0.22689425767038435, 0.3880100156609047, 0.5653622180562298, 0.4583680261155258, 0.7152373240403368, 0.5553705697340963, 0.517901761475394, 0.5141548774732563, 0.5403830337255452, 0.5424646324197689, 0.5362198363370978, 0.5112406520064132, 0.517901761475394, 0.5978351703911897, 0.7847627077223386, 0.5874271769200712, 0.5865945501474519, 0.4845961823678147, 0.5774354650725869, 0.5449625762629777, 0.517901761475394, 0.5141548774732563, 0.4746045022830058, 0.4746045022830058, 0.517901761475394, 0.5228975856364608, 0.22689425767038435, 0.3880100156609047, 0.5653622180562298, 0.4583680261155258, 0.7152373240403368, 0.5553705697340963, 0.517901761475394, 0.5141548774732563, 0.5403830337255452, 0.5424646324197689, 0.5362198363370978, 0.5112406520064132, 0.517901761475394, 0.5978351703911897, 0.7847627077223386, 0.5874271769200712, 0.5865945501474519, 0.4845961823678147, 0.092006687694)
        allCharwidthBebasList = (0.5179593961478397, 0.34096824570536177, 0.5299323269130661, 0.527850078084331, 0.5497136907860489, 0.5080687142113482, 0.4971369078604893, 0.4960957834461218, 0.5283706402915148, 0.4971369078604893, 0.22696512233211869, 1, 0.8198854763144195, 0.5372201978136387, 0.7105674128058302, 0.3794898490369599, 0.6194690265486725, 0.44456012493492975, 0.3586673607496096, 0.3581467985424258, 0.4903695991671005, 0.7792816241540864, 0.5497136907860489, 0.5497136907860489, 0.3810515356585112, 0.3810515356585112, 0.3185840707964602, 0.3175429463820927, 0.22019781363872984, 0.573138990109318, 0.2170744403956273, 0.37584591358667363, 0.22696512233211869, 0.22748568453930246, 0.573138990109318, 0.5163977095262884, 0.22696512233211869, 0.5377407600208225, 0.22748568453930246, 0.5377407600208225, 0.5778240499739719, 0.5450286309213951, 0.5179593961478397, 0.5143154606975534, 0.4747527329515877, 0.4747527329515877, 0.5179593961478397, 0.5226444560124935, 0.22696512233211869, 0.38781884435190006, 0.5653305570015617, 0.45809474232170744, 0.7152524726704841, 0.5554398750650703, 0.5179593961478397, 0.5143154606975534, 0.540864133263925, 0.5429463820926601, 0.5361790733992712, 0.5117126496616345, 0.5179593961478397, 0.5981259760541384, 0.7850078084331078, 0.5877147319104633, 0.5866736074960958, 0.4846434148880791, 0.5778240499739719, 0.5450286309213951, 0.5179593961478397, 0.5143154606975534, 0.4747527329515877, 0.4747527329515877, 0.5179593961478397, 0.5226444560124935, 0.22696512233211869, 0.38781884435190006, 0.5653305570015617, 0.45809474232170744, 0.7152524726704841, 0.5554398750650703, 0.5179593961478397, 0.5143154606975534, 0.540864133263925, 0.5429463820926601, 0.5361790733992712, 0.5117126496616345, 0.5179593961478397, 0.5981259760541384, 0.7850078084331078, 0.5877147319104633, 0.5866736074960958, 0.4846434148880791, 0.092139510)
        # allCharwidthPingFangSCList = (0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.6169326700931347, 0.3487161545565961, 1.0298404085331465, 0.6401804031412138, 0.6169326700931347, 0.9312976492994617, 0.7612768905702382, 0.9111727792532999, 0.48750865388260456, 0.38965995244679597, 0.38965995244679597, 0.43684939692312513, 0.4482997622339798, 0.7612768905702382, 0.7612768905702382, 0.38965995244679597, 0.38965995244679597, 0.38965995244679597, 0.38965995244679597, 0.34142955363649435, 0.46460792326089523, 0.308119359092766, 0.5211658243801343, 0.285912553906091, 0.285912553906091, 0.472935452042401, 0.4743233558576064, 0.285912553906091, 0.7612768905702382, 0.285912553906091, 0.7612768905702382, 0.57772377844451, 0.6662039967648403, 0.5166551105081484, 0.664816092949635, 0.5822345452616327, 0.4052741086209719, 0.664816092949635, 0.6457321242923089, 0.29597501540174026, 0.3018736860340683, 0.5964607976206032, 0.29597501540174026, 0.9819569327315095, 0.6481609824414867, 0.6575294655569648, 0.6662039967648403, 0.664816092949635, 0.4240111013244967, 0.4937543269413023, 0.4142956157826488, 0.6481609824414867, 0.577376828963277, 0.8518389646133766, 0.5850104058371801, 0.5742539659613598, 0.5138792499326008, 0.7522553569359929, 0.6839000616069612, 0.6734906241575105, 0.7918111980658507, 0.571825107812182, 0.5582928603059509, 0.7654406549609911, 0.8213046041726274, 0.33553088300416634, 0.4705065938932232, 0.6929215422960696, 0.5471894180037608, 1.0284523988276677, 0.8483691521302263, 0.8185287965422167, 0.6575294655569648, 0.8185287965422167, 0.6984732634471646, 0.6016655163453285, 0.6256072013010102, 0.7765440443180444, 0.715128373955313, 1.0763358746293046, 0.7002081696887398, 0.6485079848678563, 0.6505898405906644, 0.2973629)
        allCharwidthPingFangSCList = (0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.6215173596228033, 0.35662237462494645 , 1.0295756536648093, 0.64466352336048, 0.6215173596228033, 0.9322760394342049, 0.7642520360051436, 0.9121303043291898, 0.49335619374196316 , 0.39691384483497644 , 0.39691384483497644 , 0.44320617231033005 , 0.4547792541791685, 0.7642520360051436, 0.7642520360051436, 0.39691384483497644 , 0.39691384483497644 , 0.39691384483497644 , 0.39691384483497644 , 0.3493356193741963, 0.47063866266609516 , 0.3163309044149164, 0.5267895413630519, 0.2944706386626661, 0.2944706386626661, 0.47921131590227173 , 0.4804972138876982, 0.2944706386626661, 0.7642520360051436, 0.2944706386626661, 0.7642520360051436, 0.5829404200600086, 0.669952850407201 , 0.5225032147449635, 0.6686669524217745, 0.5872267466780968, 0.4123446206600943, 0.6686669524217745, 0.649807115302186 , 0.30432918988426916 , 0.3103300471495928, 0.6009429918559794, 0.30432918988426916 , 0.982426060865838 , 0.652378911273039 , 0.6613801971710245, 0.669952850407201 , 0.6686669524217745, 0.430775825117874 , 0.4997856836690956, 0.42134590655807974 , 0.652378911273039 , 0.5825117873981998, 0.8534076296613802, 0.5902271753107586, 0.5795113587655379, 0.5195027861123017, 0.7548221174453493, 0.687526789541363 , 0.6772396056579512, 0.7942563223317617, 0.576939562794685 , 0.5636519502786113, 0.768109729961423 , 0.8234033433347621, 0.3433347621088727, 0.4766395199314188, 0.6965280754393485, 0.5525075010715816, 1.0282897556793829, 0.8499785683669095, 0.8208315473639092, 0.6613801971710245, 0.8208315473639092, 0.7021003000428633, 0.6065152164594942, 0.6300900128589798, 0.7792541791684526, 0.7183883411915988, 1.075439348478354, 0.7038148306900985, 0.6528075439348479, 0.6545220745820831, 0.3056150878696956)
        allCharwidthChildishALList = (0.6802656650543213, 0.300057311852773, 0.6840278307596842, 0.703125, 0.5682864983876547, 0.7112274169921875, 0.6941545804341634, 0.5720486243565878, 0.6851857503255209, 0.6950225830078125, 0.2690972288449605, 0.6901041666666666, 0.6221059163411459, 0.6750573317209879, 0.7161458333333334, 0.6111111243565878, 0.6400468746821085, 0.4551510413487752, 0.3770260413487752, 0.3920712073644002, 0.432869831720988, 0.5902777910232544, 0.6290503740310669, 0.5830434163411459, 0.3770260413487752, 0.3920712073644002, 0.3952552080154419, 0.3961232503255208, 0.2731475830078125, 0.7170139153798422, 0.20225695768992105, 0.2971649169921875, 0.2902204791704814, 0.2682291666666667, 0.7170139153798422, 0.6200815836588541, 0.18113370736440024, 0.3920712073644002, 0.22800870736440024, 0.3770260413487752, 0.5541093746821085, 0.546006957689921, 0.5442708333333334, 0.585069457689921, 0.5422448317209879, 0.5052083333333334, 0.5931718746821085, 0.5590277910232544, 0.2682291666666667, 0.5512152910232544, 0.5752309163411459, 0.2650468746821086, 0.6660885413487753, 0.5622100830078125, 0.5422448317209879, 0.5870954990386963, 0.5442708333333334, 0.5590277910232544, 0.5512152910232544, 0.4800347487131755, 0.5590277910232544, 0.4800347487131755, 0.6660885413487753, 0.5740746657053629, 0.6070607503255209, 0.5720486243565878, 0.6932864983876547, 0.6232639153798422, 0.6892361640930176, 0.65625, 0.6901041666666666, 0.7120954990386963, 0.6840278307596842, 0.7071754137674967, 0.2731475830078125, 0.6970486640930176, 0.710069497426351, 0.5740746657053629, 0.8171302477518717, 0.710069497426351, 0.6840278307596842, 0.7002309163411459, 0.6872100830078125, 0.7002309163411459, 0.6840278307596842, 0.585069457689921, 0.6901041666666666, 0.5980902910232544, 0.7592587471008301, 0.7181719144185384, 0.5870954990386963, 0.7080434163411459, 0.2291683)
        allCharwidthMicrosoftYaHeiList = (0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.616899291674296, 0.3486701250076294, 1.0298021634419758, 0.640336791674296, 0.616899291674296, 0.9314236640930176, 0.7612847487131754, 0.9111701647440592, 0.4875590006510417, 0.3897569576899211, 0.3897569576899211, 0.4366319576899211, 0.4484965006510417, 0.7612847487131754, 0.7612847487131754, 0.3897569576899211, 0.3897569576899211, 0.3897569576899211, 0.3897569576899211, 0.3414340813954671, 0.4644097487131755, 0.3081597288449605, 0.5211215813954672, 0.2858784993489583, 0.2858784993489583, 0.4728020826975505, 0.4742465813954671, 0.2858784993489583, 0.7612847487131754, 0.2858784993489583, 0.7612847487131754, 0.577836791674296, 0.6660868326822916, 0.5167812903722128, 0.664642333984375, 0.5821770826975504, 0.4053819576899211, 0.664642333984375, 0.6455451250076294, 0.2960069576899211, 0.3017951250076294, 0.5963541666666666, 0.2960069576899211, 0.9820590813954672, 0.648149291674296, 0.6574062903722128, 0.6660868326822916, 0.664642333984375, 0.4238993326822917, 0.4939236243565877, 0.4140625, 0.648149291674296, 0.577256957689921, 0.8515625, 0.585069457689921, 0.5743645826975504, 0.5138889153798422, 0.7520243326822916, 0.6837395826975504, 0.6736111640930176, 0.7916666666666666, 0.5720486243565878, 0.5581597487131754, 0.765336831410726, 0.8214688301086426, 0.3356492916742961, 0.4704861243565877, 0.6929965813954672, 0.546875, 1.0283576647440593, 0.8483784993489584, 0.8185764153798422, 0.6574062903722128, 0.8185764153798422, 0.6984965006510416, 0.6015625, 0.625579833984375, 0.7766215006510416, 0.7149895826975504, 1.076388915379842, 0.7002326647440592, 0.6484375, 0.6504618326822916, 0.297451)
        allCharwidthArialList = (0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.2780316232477162, 1.0151917051056032, 0.5563062665679247, 0.5563062665679247, 0.8890772819328494, 0.4692562620139062, 0.666988825726056, 0.3891973613873591, 0.333011174273944, 0.333011174273944, 0.333011174273944, 0.5563062665679247, 0.5840362456957372, 0.5840362456957372, 0.33397762164832584, 0.33397762164832584, 0.2780316232477162, 0.2780316232477162, 0.25994623873834133, 0.2780316232477162, 0.19098161869369767, 0.35495665575768615, 0.2780316232477162, 0.2780316232477162, 0.2780316232477162, 0.5563062665679247, 0.2780316232477162, 0.5840362456957372, 0.2780316232477162, 0.5840362456957372, 0.5563062665679247, 0.5563062665679247, 0.5001201092582959, 0.5563062665679247, 0.5563062665679247, 0.2780316232477162, 0.5563062665679247, 0.5563062665679247, 0.222328659821492, 0.222328659821492, 0.5001201092582959, 0.222328659821492, 0.8331340850881406, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.5563062665679247, 0.333011174273944, 0.5001201092582959, 0.2780316232477162, 0.5563062665679247, 0.5001201092582959, 0.7222085654650893, 0.5001201092582959, 0.5001201092582959, 0.5001201092582959, 0.666988825726056, 0.666988825726056, 0.7222085654650893, 0.7222085654650893, 0.666988825726056, 0.6108026088088547, 0.7779115437932066, 0.7222085654650893, 0.2780316232477162, 0.5001201092582959, 0.666988825726056, 0.5563062665679247, 0.8331340850881406, 0.7222085654650893, 0.7779115437932066, 0.666988825726056, 0.7779115437932066, 0.7222085654650893, 0.666988825726056, 0.6108026088088547, 0.7222085654650893, 0.666988825726056, 0.9438166442462718, 0.666988825726056, 0.666988825726056, 0.6108026088088547, 0.2775477)
        allCharList = "0123456789!@#$%^&*()-_=+{}[]|\\'\";:/?.>,<abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

        width = 0
        noFontfamily = 0

        # num = 0
        # for char in allCharList:
        #     if 'Bebas' in fontfamily:
        #         width = width + (text.count(char) * allCharwidthBebasList[num])
        #     elif 'PingFang' in fontfamily:  # 'PingFang SC'
        #         width = width + (text.count(char) * allCharwidthPingFangSCList[num])
        #     elif 'childishAL' in fontfamily:
        #         width = width + (text.count(char) * allCharwidthChildishALList[num])
        #     elif 'Microsoft YaHei' in fontfamily:
        #         width = width + (text.count(char) * allCharwidthMicrosoftYaHeiList[num])
        #     else:
        #         noFontfamily = 1
        #         width = width + (text.count(char) * allCharwidthMicrosoftYaHeiList[num])
        #         # self.mySysAssert('没有找到数据:{}'.format(fontfamily))
        #     num = num + 1

        if 'Bebas' in fontfamily:
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthBebasList[weizhi]

            width = self.__ipadPbGetStrStdWidth(text, width, -0.01769911)
        elif 'PingFang' in fontfamily:  # 'PingFang SC'
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthPingFangSCList[weizhi]

            width = self.__ipadPbGetStrStdWidth(text, width, 0.0004286326)  # 0.0125007
        elif 'childishAL' in fontfamily or 'ChildishAL' in fontfamily:
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthChildishALList[weizhi]
        elif 'Microsoft YaHei' in fontfamily:
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthMicrosoftYaHeiList[weizhi]
        elif 'Arial' in fontfamily:
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthArialList[weizhi]

            width = self.__ipadPbGetStrStdWidth(text, width, 0.0745117220873465)
        else:
            # self.mySysAssert('没有找到数据:{}'.format(fontfamily))
            noFontfamily = 1
            for char in text:
                weizhi = allCharList.find(char)
                if weizhi != -1:
                    width = width + allCharwidthMicrosoftYaHeiList[weizhi]

        #
        allwidth = width + ChineseNum + quanJiaoNum
        if noFontfamily == 1:
            logger.warning('没有找到font-family数据:{}'.format(fontfamily))
        logger.debug('[{}] 标准宽度个数:{}'.format(text, allwidth))
        return allwidth


    def __ipadPbGetStrStdWidth(self, text, width, economize=0.0745117220873465):
        """处理11相连的情况"""
        if text.find('11') != -1:
            weizhi = -1
            economizeNum = 0
            while 1:
                weizhi = text.find('11', weizhi + 1)
                if weizhi == -1:
                    break
                else:
                    economizeNum = economizeNum + 1
            width = width - economizeNum * economize
            return width
        else:
            return width


    def ipadPbCheckTextColor(self, elt, color='red'):
        """ ipad检查控件颜色
        elt为控件
        color为颜色red，green，yellow，默认为red
        正确返回True，错误返回False并报错"""
        color = str(color).lower()
        classAttr = elt.get_attribute('class')
        text = self.mySysStringCleanup(elt.text)
        if 'red' in classAttr or 'green' in classAttr or 'yellow' in classAttr:
            if color in classAttr:
                logger.debug('{} 的颜色是{}'.format(text, color))
                return True
            else:
                self.mySysAssert('{} 的颜色预期为{}，实际为{}'.format(text, color, classAttr))
        else:
            styleAttr = elt.get_attribute('style')
            logger.debug(styleAttr)

            retcolor = self.pbJudgeRGBColor(styleAttr)
            if retcolor == color:
                logger.debug('{} 的颜色是{}'.format(text, color))
                return True
            # elif 'color: rgb(255, 255, 255)' in styleAttr:
            #     logger.debug('{}的颜色是原色'.format(text))
            #     return True
            else:
                self.mySysAssert('{} 的颜色预期为{}，实际为{}'.format(text, color, retcolor))


    def pbJudgeRGBColor(self, rgb):
        """ 计算rgb颜色
        例：self.pbDecideRGB('rgb(255, 255, 255)')或self.pbDecideRGB('background: rgb(240, 251, 245); color: rgb(0, 176, 79); border: 0.75px solid rgb(0, 176, 79);')
        正确返回True，错误返回False并报错"""
        rest = None
        findallrest = re.findall(r'color:(.*?);', rgb)
        if len(findallrest) == 0:
            rest = rgb
        else:
            rest = findallrest[0]
        tmpList = str(rest).replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
        logger.debug(tmpList)

        if len(tmpList) == 3:
            red = int(tmpList[0])
            green = int(tmpList[1])
            blue = int(tmpList[2])
            if (red == 255 and green == 255 and blue == 255):
                return 'white'
            if (red == 0 and green == 0 and blue == 0):
                return 'black'
            h, s, v = self.mySysRgb2Hsv(red, green, blue)
            if h < 30 or h > 330:
                color = 'red'
                logger.debug('当前颜色为{}'.format(color))
                return color
            elif h < 90 and h >= 30:
                color = 'yellow'
                logger.debug('当前颜色为{}'.format(color))
                return color
            elif h < 170 and h >= 90:
                color = 'green'
                logger.debug('当前颜色为{}'.format(color))
                return color
            else:
                return 'other'
        else:
            logger.error('参数错误：{}'.format(rgb))
            return False


    def ipadPbClickCNYexTHB(self, driver):
        """ 单击CNY和THB按键
        返回无"""
        self.myWtFindElement(driver, By.XPATH, "//div[text()='CNY']")
        time.sleep(1)
        self.myWtFindElement(driver, By.XPATH, "//div[text()='CNY']")


    def ipadPbSwitchToFrame(self, driver):
        """ 进入iframe"""
        iframe = self.myWtFindElement(driver, By.TAG_NAME, 'iframe')
        # iframe = self.myWtEltNonexiContinue(driver, By.TAG_NAME, 'iframe', 0, 1)
        if iframe is not None:
            driver.switch_to_frame(iframe)


    def ipadPbSwitchToDefault(self, driver):
        """ 退出iframe"""
        driver.switch_to_default_content()


    ########################################################
    """API接口"""
    ########################################################
    def myApi(self, url, requestMethod, datas, jsons):
        """接口"""
        header = {
            'imei': 'B8ABE16A-D303-4F4F-9B37-B2ECE7DF644V',
            'x-pd-auth-token': self.myApiToken
        }
        NumberTimes = 1
        while 1 == 1:
            text, login = self.mySysApi(url, requestMethod, header, datas, jsons)
            logger.debug(text)
            # soup = BeautifulSoup(text, "lxml")
            if text is not None:
                soup = json.loads(text)
                if "\"code\":\"000000\"" in text:
                    logger.debug("获取数据成功 {}".format(url))
                    # logger.debug(text)
                    return soup
                elif login.status_code in [401, 403]:
                    logger.error('login:{}:{}'.format(login.status_code, text))
                    if NumberTimes >= self.maxNumberTimes:
                        return None
                    NumberTimes = NumberTimes + 1
                    self.myGetWebApiToken()
                    continue
                else:
                    return soup


    def myGetWebToken(self):
        """登录网页ipad取token"""
        self.browserType = "chrome"

        self.setUp()

        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        self.mySysParameterValueReplaceJson(paramsIn, 'password')
        userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')

        self.ipadPbLoginOK(driver, userName, password, self.url)

        newRes = self.myWtGetProxyNewResult()
        res = self.myWtGetProxyNewAloneResult(newRes, '/login')
        if len(res) > 0:
            token = json.loads(res[0]['response']['content']['text'])['data']['token']
            logger.debug('成功获取token:{}'.format(token))
            self.myApiToken = token

        self.tearDown()

        self.browserType = "api"
        self.ifbrowserTypeRight = 6


    def myGetWebApiToken(self):
        """用api直接登录取token"""
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        self.mySysParameterValueReplaceJson(paramsIn, 'password')
        userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')

        # 获取加密的密码
        encryptUrl = paramsIn['IDMsm2EncryptUrl'] + password
        result = self.mySysApi(encryptUrl, 'get', {}, {}, {})
        logger.debug(result)
        # logger.debug(type(result))
        encryptUserPwd = eval(result[0])["data"]
        logger.debug(encryptUserPwd)

        # 登录取token
        apiname = "login"
        apiInfo = self.paramsApi[apiname]
        requestMethod = apiInfo["requestMethod"]
        queryString = apiInfo["queryString"]
        datas = apiInfo["datas"]
        logger.debug(datas)
        jsons = self.myPbEvalStr(self.myPbEvalStr(str(apiInfo["jsons"])).format(userName, encryptUserPwd))
        pathTmp = apiInfo["path"]
        url = '{}{}{}'.format(self.url, apiname, queryString)
        result = self.mySysApi(url, requestMethod, {}, datas, jsons)
        logger.debug(result)
        self.myApiToken = eval(result[0])[pathTmp]['token']
        logger.debug('成功获取token:{}'.format(self.myApiToken))


    def myPbEvalStr(self, es):
        """如果参数es第一个字符是‘{’，则删除第一个字符是‘{’和最后一个字符‘}’
        如果没有，则第一个字符前面加‘{’和最后一个字符后面加‘}，并转为字典’"""
        tmp = str(es)
        if tmp[0] == "{":
            return tmp.strip('}{')
        else:
            return eval("{" + tmp + "}")



    ########################################################
    """大屏"""
    ########################################################
    def dapingPbParameterDeal(self, paramsIn):
        """app 判断SIT、UAT、生产使用不同的用户名密码"""
        if ":13080/" in self.url or ":12443/" in self.url:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'DapingUserAdminID', 'DapingUserAdminPassword')
            return userName, password
        else:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'DapingUserAdminIDProd', 'DapingUserAdminPasswordProd')
            return userName, password


    def dapingPbLoginOK(self, driver, userName, password, url):
        """大屏登录成功"""
        self.dapingPbwebLoginComm(driver, userName, password, url)

        self.myWtFindElement(driver, By.XPATH, "//div[text()='大屏']")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        return True


    def dapingPbLoginPasswordError(self, driver, userName, password, url):
        """大屏登录失败"""
        password = '1'
        self.dapingPbwebLoginComm(driver, userName, password, url)

        self.myWtFindElement(driver, By.XPATH, "//p[text()='密码错误，请重新输入']")

        self.myWtGetJsLog(driver, self.jsLogExclude)


    def dapingPbwebLoginComm(self, driver, userName='', password='', url=''):
        """大屏登录"""
        logger.debug('打开网页{}'.format(url))
        driver.get(url)
        driver.maximize_window()  # 最大化窗口

        clientWidth = driver.execute_script("return document.body.clientWidth")
        clientHeight = driver.execute_script("return document.body.clientHeight")
        self.clientWidthProportion = self.screenScaling
        logger.debug('width:{} height:{};  实际横屏width 与 网页可见区域width比例：{}'.format(clientWidth, clientHeight, self.clientWidthProportion))
        # client_height = driver.execute_script("return document.body.clientHeight")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        self.myWtSendKeysWebEx(driver, By.XPATH, "//input[contains(@placeholder, '请输入账号')]", userName)
        self.myWtSendKeysWebEx(driver, By.XPATH, "//input[contains(@placeholder, '请输入密码')]", password)

        self.myWtClickEx(driver, By.XPATH, "//span[text()='登录']")


    def dapingPbRefreshWaiting(self, driver, beginWaitTime=0, endWaitTime=30):
        """大屏判断界面是否在等待，加载中"""
        logger.debug("大屏网页刷新等待开始")
        self.myWtJSRefreshWaiting(driver)

        self.myWtFindElement(driver, By.TAG_NAME, "body")
        self.myWtFindElement(driver, By.TAG_NAME, "div")
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "locating", 0, 0) is not None:
            self.myWtFindElement(driver, By.CLASS_NAME, "locating")
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "inner-content", 0, 0) is not None:
            self.myWtFindElement(driver, By.CLASS_NAME, "inner-content")
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "canvas", 0, 0) is not None:
            self.myWtFindElement(driver, By.CLASS_NAME, "canvas")

        performanceList = self.myPbPerformanceNetworkLog(driver, beginWaitTime, endWaitTime)
        logger.debug("大屏网页刷新等待结束")
        return performanceList


    def dapingPbCloseDialog(self, driver, actionbar=None):
        """大屏关闭弹出窗口"""
        if actionbar is None:
            self.myWtClickEx(driver, By.CLASS_NAME, 'close')
            logger.debug("关闭弹出窗口")
        elif actionbar == 'close-btn':
            self.myWtClickEx(driver, By.CLASS_NAME, 'close-btn')
            logger.debug("关闭弹出窗口")
        else:
            wwpopupList = self.myWtFindElements(driver, By.CLASS_NAME, 'ww-popup')
            for wwpopup in wwpopupList:
                if "open" in wwpopup.get_attribute("class"):
                    actionbar = self.myWtFindElement(wwpopup, By.CLASS_NAME, 'action-bar')
                    self.myWtClickEx(actionbar, By.TAG_NAME, "img")
                    logger.debug("关闭弹出窗口")
                    break


    def dapingPbActionMoveToElement(self, driver, eltList):
        """大屏，循环移动鼠标到多个控件上，目的是为了阻止轮播
        参数：
        driver
        eltList为控件列表
        全局变量self.dapingActionMoveToElement为非1则停止本功能"""
        self.dapingActionMoveToElement = 1
        while self.dapingActionMoveToElement == 1:
            for elt in eltList:
                self.myWtActionMoveToElement(driver, elt)
            time.sleep(1)


    def dapingPbActionMoveToElementStop(self, t1=None):
        """大屏，dapingPbActionMoveToElement的停止while功能
        参数：t1，线程
        """
        self.dapingActionMoveToElement = 0
        if t1 is not None:
            t1.join()


    def dapingPbCheckTextColor(self, elt, color='red'):
        """ 大屏检查控件颜色
        elt为控件
        color为颜色red，green，yellow，默认为red
        正确返回True，错误返回False并报错"""
        styleAttr = elt.find_element(By.XPATH, './/..').get_attribute('style')  # 取当前控件父节点
        text = self.mySysStringCleanup(elt.text)
        if color == 'green' and 'color: rgb(13, 246, 183)' in styleAttr:
            logger.debug('{} 的颜色是green'.format(text))
            return True
        elif color == 'yellow' and 'color: rgb(254, 187, 8)' in styleAttr:
            logger.debug('{} 的颜色是yellow'.format(text))
            return True
        elif color == 'red' and 'color: rgb(252, 77, 52)' in styleAttr:
            logger.debug('{} 的颜色是red'.format(text))
            return True
        else:
            retcolor = self.pbJudgeRGBColor(styleAttr)
            if retcolor == color:
                logger.debug('{} 的颜色是{}'.format(text, color))
                return True
            else:
                self.mySysAssert('{} 的颜色预期为{}，实际为{}'.format(text, color, retcolor))


    def dapingPbGuanliMaoyangBegin(self, driver, paramsIn, checkPoint):
        """大屏管理菜单中大屏冒烟"""
        #        caseName = sys._getframe().f_code.co_name  #获取本函数名
        articlecontentList = self.myWtFindElements(driver, By.CLASS_NAME, "article-content")
        logger.debug('大屏个数：{}'.format(len(articlecontentList)))
        for articlecontent in articlecontentList:
            screenname = self.myWtFindElement(articlecontent, By.CLASS_NAME, "screen-name")
            title = self.mySysStringCleanup(screenname.text)
            paramsIn['daPingTitleActual'] = title
            paramsIn['father'] = articlecontent
            if 'daPingTitleExpect' in paramsIn:
                if paramsIn['daPingTitleExpect'] in title:
                # if paramsIn['daPingTitleExpect'] == title:
                    self.dapingPbGuanliMaoyangDetail(driver, paramsIn, checkPoint)

                    break

            else:
                self.dapingPbGuanliMaoyangDetail(driver, paramsIn, checkPoint)

                self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def dapingPbGuanliMaoyangEnd(self, driver, paramsIn, checkPoint):
        """大屏管理菜单中大屏冒烟"""
        self.myWtGetJsLog(driver, self.jsLogExclude)

        # if self.smokeCheck is True:
        #     self.myPbKeyboardListener()

        handles = paramsIn['handles']
        self.myWtWndowhandlesClose(driver, handles)


    def dapingPbGuanliMaoyangDetail(self, driver, paramsIn, checkPoint):
        """大屏管理菜单中大屏冒烟"""
        father = paramsIn['father']
        title = paramsIn['daPingTitleActual']
        font = self.myWtFindElement(father, By.TAG_NAME, "section")

        self.myWtActionMoveToElement(driver, font)

        # 单击预览
        preview = self.myWtFindElement(father, By.CLASS_NAME, 'preview')
        eltooltip = self.myWtFindElement(preview, By.CLASS_NAME, 'item')

        self.myWtClick(eltooltip)
        logger.debug('单击进入大屏：{}'.format(title))

        handles = self.myWtWndowhandlesOpen(driver, 2, newhandleNum=1)
        paramsIn['handles'] = handles

        self.myWtFindElement(driver, By.CLASS_NAME, 'report-wrap')


    def dapingPbCheckJianKong(self, driver, elt):
        """监控检查是否正常
        elt为监控屏幕控件<video
        注：浏览器非headless状态才可用，否则可能不准"""
        logger.debug('**监控检查开始')
        self.myWtActionMoveToElement(driver, elt)
        father = self.myWtFindElement(elt, By.XPATH, './../..')
        # outerHTML = self.myPbStringCleanup(father.get_attribute("outerHTML"))
        # logger.debug(outerHTML)
        self.myWtClickEx(father, By.CLASS_NAME, 'prism-fullscreen-btn')
        time.sleep(1)
        # video = self.myWtFindElement(father, By.CLASS_NAME, 'prism-player')
        video = self.myWtFindElement(father, By.TAG_NAME, 'video')
        x, y, width, height = self.myPbGetElementSize(video)
        logger.debug("width:{}, height:{}".format(width, height))
        first = None
        if width < 300:
            first = self.myWtScreenshotAsFile(driver, temppath=True)
        else:
            first = self.myWtScreenshotByElement(driver, video)
        second = first.replace('.png', '.bak.png')
        self.mySysCopyFile(first, second)
        time.sleep(1)
        # video = self.myWtFindElement(father, By.CLASS_NAME, 'prism-player')
        video = self.myWtFindElement(father, By.TAG_NAME, 'video')
        if width < 300:
            self.myWtScreenshotAsFile(driver, temppath=True)
        else:
            self.myWtScreenshotByElement(driver, video)
        self.myWtClick(father)
        # self.myWtActionMoveToElement(driver, father)
        self.myWtClickEx(father, By.CLASS_NAME, 'prism-fullscreen-btn')
        if self.myWtImageCompare(first, second, 1) is True:
            # self.mySysAssert('监控故障')
            logger.error('监控故障')
        logger.debug('**监控检查结束')


    def dapingPbFullScreen(self, driver):
        """点击左下角全屏"""
        elt = self.myWtFindElement(driver, By.CLASS_NAME, "action-control-bar")
        self.myWtActionMoveToElement(driver, elt)
        fullscreen = self.myWtFindElement(driver, By.CLASS_NAME, "full-screen")
        self.myWtClickEx(fullscreen, By.XPATH, ".//*[name()='svg' and contains(@class,'iconfont')]")
        logger.debug('点击大屏全屏按钮')


    def dapingPbDropChildrenClick(self, driver, paramsIn, checkPoint, dropitemClkList, menuNum, scrollIntoView=True):
        """下拉控件drop-children点击
        dropitemClkList为控件列表
        menuNum为要点击第几个控件"""
        for clkNum in range(len(dropitemClkList)):
            if menuNum == clkNum:
                dropitem = dropitemClkList[clkNum]
                if scrollIntoView is True:
                    self.myWtJsScrollIntoView(driver, dropitem)
                else:
                    if not dropitem.is_displayed() or not dropitem.is_enabled():
                        self.myWtJsScrollIntoView(driver, dropitem)
                self.myWtClick(dropitem)
                return clkNum, dropitem


    ########################################################
    """app web"""
    ########################################################
    def appPbParameterDeal(self, paramsIn):
        """app 判断SIT、UAT、生产使用不同的用户名密码"""
        if ":8388/" in self.url or ":11443/" in self.url:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
            return userName, password
        else:
            self.mySysParameterValueReplaceJson(paramsIn, 'userName')
            self.mySysParameterValueReplaceJson(paramsIn, 'password')
            userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPasswordProd')
            return userName, password


    def appPbLoginOK(self, driver, userName, password, url):
        """app登录成功"""
        self.appPbwebLoginComm(driver, userName, password, url)

        time.sleep(1)
        cancel = "//span[text()='取消']/../.."
        if self.myWtEltNonexiContinue(driver, By.XPATH, cancel) is not None:
            self.myWtClickEx(driver, By.XPATH, cancel)

        self.appPbRefreshWaiting(driver)  # 判断等待

        self.myWtFindElement(driver, By.XPATH, "//div[text()='经营分析']")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        return True


    def appPbLoginPasswordError(self, driver, userName, password, url):
        """app登录失败"""
        password = '1'
        self.appPbwebLoginComm(driver, userName, password, url)

        self.myWtFindElement(driver, By.XPATH, "//p[text()='密码错误，请重新输入']")

        self.myWtGetJsLog(driver, self.jsLogExclude)


    def appPbwebLoginComm(self, driver, userName='', password='', url=''):
        """app登录"""
        logger.debug('打开网页{}'.format(url))
        driver.get(url)
        driver.maximize_window()  # 最大化窗口

        clientWidth = driver.execute_script("return document.body.clientWidth")
        clientHeight = driver.execute_script("return document.body.clientHeight")
        self.clientWidthProportion = 1366/clientWidth
        logger.debug('width:{} height:{};  app Pro横屏width 与 网页可见区域width比例：{}'.format(clientWidth, clientHeight, self.clientWidthProportion))
        # client_height = driver.execute_script("return document.body.clientHeight")

        self.myWtGetJsLog(driver, self.jsLogExclude)

        self.myWtSendKeysWebEx(driver, By.CLASS_NAME, "input-text", userName)
        self.myWtSendKeysWebEx(driver, By.CLASS_NAME, "psd", password)

        self.myWtClickEx(driver, By.CLASS_NAME, "login_button")


    def appPbSelectMainMenu(self, driver, menuStr1='', menuStr2='', menuStr3=''):
        """函数说明：选择主菜单
        输入参数：driver，menustr为菜单
        返回参数：无"""
        time.sleep(1)
        # self.appPbRefreshWaiting(driver)  # 判断界面
        # 底部菜单
        if menuStr1 != '':
            menuLeft = self.myWtFindElement(driver, By.CLASS_NAME, 'cFoot')
            self.appPbRefreshWaiting(driver)  # 判断界面
            itemList = self.myWtFindElements(menuLeft, By.CLASS_NAME, 'item')
            for item in itemList:
                if menuStr1 in item.text:
                    self.myWtClick(item)
                    time.sleep(1)
                    break

        self.appPbRefreshWaiting(driver)  # 判断界面

        # 菜单
        if menuStr2 != '':
            menuStr2List = menuStr2.split(':')
            menuStr2_1 = menuStr2List[0]
            menuStr2_2 = menuStr2List[1]
            buttonTitleList = self.myWtFindElements(driver, By.CLASS_NAME, "buttonTitle")
            for buttonTitle in buttonTitleList:
                item = self.myWtFindElement(buttonTitle, By.XPATH, ".//..")
                buttonTitleText = item.text
                if menuStr2_2 == "":
                    if menuStr2_1 in buttonTitleText and "pad" not in buttonTitleText:
                        self.myWtClick(item)
                        time.sleep(1)
                        break
                else:
                    if menuStr2_1 in buttonTitleText and menuStr2_2 in buttonTitleText:
                        self.myWtClick(item)
                        time.sleep(1)
                        break

        self.appPbRefreshWaiting(driver)  # 判断等待

        logger.debug('单击菜单：{}-{}-{}'.format(menuStr1, menuStr2, menuStr3))


    def appPbRefreshWaiting(self, driver):
        """app判断界面是否在等待，加载中"""
        return
        time.sleep(1)
        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # CLASS_NAME   fistpageloading
                if driver.find_element(By.CLASS_NAME, "van-overlay").is_displayed():  # van-toast--loading
                    if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                        return None
                    continue
                else:
                    return None
                # loading = self.myWtFindElement(driver, By.CLASS_NAME, "van-toast--loading", 1, 0, 1)
                # if loading is not None:
                #     styleStr = loading.get_attribute('style')
                #     # logger.debug(styleStr)
                #     if styleStr == 'display: none;':
                #         break
                # else:
                #     break
                # if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                #     return None
            except:
                return None
                # if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                #     logger.error('{}'.format(traceback.format_exc()))
                #     return None
                # time.sleep(0.1)


    def appPbLeftBack(self, driver, maxWaittime=None):
        """ 关闭窗口x 或 退回< """
        # self.myPbKeyboardListener()

        self.myWtGetJsLog(driver, self.jsLogExclude)
        arrowLeft = "//i[contains(@class, 'van-icon-arrow-left')]"
        if maxWaittime is None:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        else:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft, 0, maxWaittime):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        self.myWtGetJsLog(driver, self.jsLogExclude)


    def appPbCloseTopRight(self, driver, maxWaittime=None):
        """ 关闭窗口x 或 退回< """
        # time.sleep(1)
        self.myWtGetJsLog(driver, self.jsLogExclude)
        arrowLeft = "//i[contains(@class, 'van-popup__close-icon')]"
        if maxWaittime is None:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        else:
            if self.myWtEltNonexiContinue(driver, By.XPATH, arrowLeft, 0, maxWaittime):
                self.myWtClickEx(driver, By.XPATH, arrowLeft)
        self.myWtGetJsLog(driver, self.jsLogExclude)


    ########################################################
    """Oracle数据库"""
    ########################################################
    def myPbOracleExecute(self, sql):
        """oracle操作执行SQL
        sql为SQL语句，包括insert、update、select 、delete等"""
        params_in = self.params_in
        if 'test.' in self.url:
            oracleIP = params_in['oracleIP']
            oraclePort = params_in['oraclePort']
            oracleUsername = params_in['oracleUsername']
            oraclePassword = params_in['oraclePassword']
            serviceName = params_in['oracleServiceName']
            sshIP = params_in['sshIP']
            sshPort = params_in['sshPort']
            sshUsername = params_in['sshUsername']
            sshPassword = params_in['sshPassword']
            fetchall, listDictResult, sqlType, rowcount = self.mySysOracleExecute(oracleIP, oraclePort, oracleUsername, oraclePassword, serviceName, sql, sshIP, sshPort, sshUsername, sshPassword)
            if sqlType is not None:
                if sqlType == 'select':
                    if rowcount == 0:
                        logger.debug('没有查到数据')
                        return fetchall, listDictResult
                    else:
                        return fetchall, listDictResult
                else:
                    return None, None
            else:
                logger.debug('执行SQL出错')
                return None, None
        else:
            logger.debug('生产环境，不需要检查数据库')
            return None, None


    def myPbMybatis(self, fileName, sql_id, params):
        """生成SQL
        fileName为带路径的文件名
        sql_id为ipadWuLiuZhuiZong.xml中查找唯一SQL的id
        params为字典，如params = {
            'type': type,
            'wareCode': wareCode,
            'storeRegion': city,
            'storeName': cangkuName
        }
        """
        logger.debug(params)
        localPath = os.getcwd()
        mapper = PyMapper(xml_path='{}/cases/Zd/{}'.format(localPath, fileName))
        sql = mapper.statement(sql_id, params=params)
        logger.debug('{}{}'.format(sql_id, sql))
        return sql


    def myPbOracleValueListCheck(self, actualValue, fileName, sql_id, params):
        """检查数据，数据库SQL查出的数值与传入的值对比
        actualValue传入的值，如{'tabList': [1,2,3],[4,6,7]}或{1:'45',2:89}
        fileName, sql_id, params参考def myPbMybatis中的说明
        例：self.myPbOracleValueListCheck(actualValue, self.mybatisFile, 'getWDSvcDown', params)"""
        if 'test.' not in self.url:
            defName = sys._getframe().f_code.co_name  # 获取本函数名
            logger.debug('生产环境，{}不需要检查数据库'.format(defName))
            return None

        sql = self.myPbMybatis(fileName, sql_id, params)
        logger.debug('mybatis id: {}'.format(sql_id))
        fetchall, listDictResult = self.myPbOracleExecute(sql)
        logger.debug(fetchall)
        logger.debug(listDictResult)

        # 表格对比
        # if actualValue.get('tabList') is not None:
        if 'tabList' in actualValue:
            num = None
            for value in actualValue['tabList']:
                num = len(value)
                break

            actualNum = len(actualValue['tabList'])
            fetchallNum = len(fetchall)
            if actualNum > fetchallNum:
                self.mySysAssert('实际表格行数{}大于数据库记录个数{}'.format(actualNum, fetchallNum))

            rowNum = 0
            for fetch in fetchall:
                for fnum in range(0, num):
                    expectText = str(fetch[fnum])
                    actualText = list(actualValue.values())[0][rowNum][fnum]
                    logger.debug('第{}行第{}列'.format(rowNum+1, fnum+1))
                    if self.mySysIsAllNumberExclude(actualText):
                        actualText = actualText.replace(',', '')
                    if expectText == 'None':
                        expectText = '-'
                    self.mySysTextCheck(actualText, expectText)
                rowNum = rowNum + 1
                if rowNum >= actualNum:
                    break
            # return None
            return fetchall, listDictResult

        # 单行普通值对比
        else:
            num = len(actualValue)
            cpActualValue = copy.deepcopy(actualValue)

            for fetch in fetchall:
                for fnum in range(0, num):
                    expectText = str(fetch[fnum])
                    actualText = list(actualValue.values())[fnum]
                    cpActualValue[fnum+1] = actualText
                    if self.mySysIsAllNumberExclude(actualText):
                        actualText = actualText.replace(',', '')
                    if expectText == 'None':
                        expectText = '-'
                    self.mySysTextCheck(actualText, expectText)
                break
            # return cpActualValue
            return fetchall, listDictResult


    def myPbOracleValueDictCheck(self, actualValue, fileName, sql_id, params):
        """检查数据，数据库SQL查出的数值与传入的值对比
        actualValue传入的值，如{'tabList': [{'a':1, 'b':2, 'c':3},{'a':4, 'b':5, 'c':6}]}或{'a':'45', 'b':9}
        fileName, sql_id, params参考def myPbMybatis中的说明
        例：self.myPbOracleValueDictCheck(actualValue, self.mybatisFile, 'getWDSvcDown', params)"""
        if self.smokeCheck is True:
            return None

        if 'test.' not in self.url:
            defName = sys._getframe().f_code.co_name  # 获取本函数名
            logger.debug('生产环境，{}不需要检查数据库'.format(defName))
            return None

        sql = self.myPbMybatis(fileName, sql_id, params)
        logger.debug('mybatis id: {}'.format(sql_id))
        fetchall, listDictResult = self.myPbOracleExecute(sql)

        # 表格对比
        # if actualValue.get('tabList') is not None:
        if 'tabList' in actualValue:
            num = None
            for value in actualValue['tabList']:
                num = len(value)
                break

            logger.debug('actualValue:{}'.format(actualValue))
            actualNum = len(actualValue['tabList'])
            fetchallNum = len(listDictResult)
            if actualNum > fetchallNum:
                self.mySysAssert('实际表格行数{}大于数据库记录个数{}'.format(actualNum, fetchallNum))

            rowNum = 0
            for fetch in actualValue['tabList']:
                fnum = 0
                for key in fetch:
                    expectText = str(fetch[key])
                    actualText = actualValue['tabList'][rowNum][key]
                    logger.debug('第{}行第{}列'.format(rowNum+1, fnum+1))
                    # if self.mySysIsAllNumberExclude(actualText):
                    #     actualText = actualText.replace(',', '')
                    if expectText == 'None':
                        expectText = '-'
                    self.mySysTextCheck(actualText, expectText)
                    fnum = fnum + 1
                rowNum = rowNum + 1
                if rowNum >= actualNum:
                    break
            # return None
            return listDictResult

        # 单行普通值对比
        else:
            num = len(actualValue)
            cpActualValue = copy.deepcopy(actualValue)

            for fetch in actualValue:
                expectText = str(listDictResult[fetch])
                actualText = actualValue[fetch]
                cpActualValue[fetch] = actualText
                if self.mySysIsAllNumberExclude(actualText):
                    actualText = actualText.replace(',', '')
                if expectText == 'None':
                    expectText = '-'
                self.mySysTextCheck(actualText, expectText)
                break
            # return cpActualValue
            return listDictResult


    ########################################################
    """其它"""
    ########################################################
    def myPbKeyboardListener(self):
        """函数说明：键盘监听，当按下'esc'按键时结束监听
        参数无
        返回无
        例：mySysKeyboardListener('esc')"""
        if self.smokeCheck is True:
            self.mySysKeyboardListener('esc')


    def myPbPerformanceNetworkLog(self, driver, beginWaitTime=1, endWaitTime=10):
        """获取Google Chrome网页DevTools的Network接口请求和返回信息
        参数同self.myWtPerformanceNetworkLog"""
        # excludeList = ['https://cpsetest.cpgroup.cn:13080/big-screen/screen/queryScreenDetail?t=']
        excludeList = []
        return self.myWtPerformanceNetworkLog(driver, beginWaitTime, endWaitTime, excludeList)


    def myPbRefreshWaiting(self, driver, element, fileName, percent=10, falseBreak=True):
        """用图片对比差别，判断界面是否在等待，加载中
        由driver和element截取控件截图，并与fileName对比
        percent为差别系数，小于等于percent则等待，大于则退出等待
        falseBreak=True即为大于percent则退出等待，falseBreak为None时，则小于等于percent退出等待"""
        x, y, width, height = self.myPbGetElementSize(element)

        d1 = datetime.datetime.now()
        localPath = os.getcwd()
        filePathName = '{}/cases/Zd/{}'.format(localPath, fileName)
        while 1 == 1:
            newfile = self.myWtScreenshotByxy(driver, x, y, width, height)
            # newfile = self.myWtScreenshotByElementAsFile(driver, element)
            newpercent = self.myWtImageCompare(newfile, filePathName, percent)
            if falseBreak is True:
                if newpercent is False:
                    break
            else:
                if newpercent is True:
                    break

            if self.mySysTimeGapSec(d1) >= self.maxWaittime * 2:
                break
            time.sleep(1)


    def myPbGetElementSize(self, element, click=False):
        """取控件element的x, y, width, height，并返回
        click为True则取点击x和y，为False则取截图x和y"""
        clientWidthPro = self.clientWidthProportion
        x = None
        y = None
        if self.browserHeadless == 'UI' and click is False:
            x = float(element.location['x']) / clientWidthPro
            y = float(element.location['y']) / clientWidthPro
        else:
            x = float(element.location['x'])
            y = float(element.location['y'])
        scaling = element.get_attribute('scaling')
        height = None
        width = None
        if scaling is None or str(scaling) == '1':
            height = float(element.size['height'])
            width = float(element.size['width'])
        else:
            height = float(element.size['height']) / 2  # 3
            width = float(element.size['width']) / 2  # 3

        ratio = None
        if self.pixelRatio is not None:
            if self.browserHeadless == 'noUI':
                ratio = self.pixelRatio
            else:
                ratio = self.pixelRatio * 2
        else:
            ratio = 1
            # if self.browserHeadless == 'noUI':
            #     ratio = 1
            # else:
            #     if self.screenScaling is not None:
            #         ratio = self.screenScaling
            #     else:
            #         ratio = 1
        logger.debug("ratio={}, self.pixelRatio={}".format(ratio, self.pixelRatio))
        x = x * ratio
        y = y * ratio
        logger.debug("x:{},y:{},width:{},height:{}".format(x, y, width, height))

        return x, y, width, height


    def myPbScreenshotByElement(self, driver, element):
        """截取整个控件截图，存储至系统临时目录下"""
        x, y, width, height = self.myPbGetElementSize(element)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)
        return TEMP_FILE


    # def tearDown(self):
    #     """"""
    #     super().tearDown()



