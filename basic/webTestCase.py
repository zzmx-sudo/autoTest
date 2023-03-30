# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.getcwd())
import unittest
from selenium import webdriver as seleniumWebdriver
# from appium import webdriver as appiumWebdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from basic.myPublic import MySwitch
if os.path.isfile("basic/myReqClient.py"):
    from basic.myReqClient import MyReqClient
from basic.mySysCommon import MySysCommon
import time
import datetime
import random
import configparser
import basic.myGlobal as myGlobal
import traceback
import shutil
import tempfile
from PIL import Image, ImageDraw
import subprocess
import threading
import multiprocessing
from multiprocessing import Process
from functools import reduce
from selenium.webdriver import DesiredCapabilities
import json
from browsermobproxy import Server
# import aircv as ac
import platform
platformSystem = platform.system()
if platformSystem == "Windows":
    import win32gui
    import win32con
    import win32api


TIME_OUT = 8        #等待时长
POOL_FREQUENCY = 0.5    #检测时间间隔

logger = myGlobal.getLogger()

class WebTestCase(unittest.TestCase, MySysCommon):
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(WebTestCase, self).__init__(methodName)

        self.maxWaittime = 20  # 最大等时间（秒）
        self.maxNumberTimes = 3  # 最大重试次数
        self.webOrPhone = 2  # 判断在操作1:web，2:手机
        self.screenRecordFileList = []  # 录像文件列表
        self.ifScreenRecord = 1  # 1录像   0不录像
        self.pathReportPic = '/report/pic/'
        self.pixelRatio = None

        if bool(AllPirParams):
            logger.debug("自动化测试")
            self.className = self.__class__.__name__  # 获取类名
            self.methodName = methodName
            self.taskId = AllPirParams['taskId']
            self.sheetName = AllPirParams['sheetName']
            self.caseId = AllPirParams['caseId']
            self.browserType = AllPirParams['browserType'].lower()
            self.params_in = AllPirParams['params_in']
            self.checkPoint = AllPirParams['checkPoint']
            self.url = AllPirParams['url']

            self.enabledProxy = 'Y'  # 是否开启代理服务记录前端request和response信息
            self.enabledGetJsLog = 'Y'  # 是否开启记录前端JS控制台信息

            # 单独调试用例时关闭
            if 'closeProxyAndJsLog' in AllPirParams and AllPirParams['closeProxyAndJsLog'] is True:
                self.enabledProxy = 'N'  # 是否开启代理服务记录前端request和response信息
                self.enabledGetJsLog = 'N'  # 是否开启记录前端JS控制台信息

            self.smokeCheck = True  # True:只做界面冒烟半自动测试（自动点击，人眼检查界面），不做界面和数据检查； None：不做界面冒烟测试，做界面和数据检查

            self.paramsApi = {}  # api接口配置字典
            self.resultPicName = None

            self.MyReqClient = MyReqClient()
            self.__getAppPathConf()
        else:
            logger.debug("自动化应用")
            self.taskId = None
            self.browserType = "chrome"

            self.smokeCheck = None

            self.enabledProxy = 'N'  # 是否开启代理服务记录前端request和response信息
            self.enabledGetJsLog = 'N'  # 是否开启记录前端JS控制台信息

        if platformSystem == "Windows":
            self.screenRealX, self.screenRealY = self.mySysGetRealScreenSize()
            screenRealX, screenRealY = self.mySysGetScreenSize()
            self.screenScaling = screenRealX / self.screenRealX
            logger.debug('屏幕缩放比例: {}'.format(self.screenRealX / screenRealX))
        else:
            self.screenRealX = None
            self.screenRealY = None


    def setUp(self):
        """"""
        # 判断浏览器类型
        self.ifbrowserTypeRight = 0
        for case in MySwitch(self.browserType):
            if case("chrome"):
                optionsOrder = seleniumWebdriver.ChromeOptions()
                optionsOrder.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 忽略连接警告信息
                optionsOrder.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # 禁用浏览器正在被自动化程序控制的提示，禁止打印日志
                if self.smokeCheck is None:
                    logger.debug("无头模式，即浏览器不提供可视化页面")
                    optionsOrder.add_argument('--headless')
                if optionsOrder.headless is True:
                    self.browserHeadless = 'noUI'
                    logger.debug("chrome浏览器无头模式")
                else:
                    self.browserHeadless = 'UI'
                    logger.debug("chrome浏览器可视化模式")
                optionsOrder.add_argument('--no-sandbox')  # 沙盒模式运行,Chrome在root权限下跑 解决DevToolsActivePort文件不存在的报错
                optionsOrder.add_argument('--disable-gpu')  # 禁用gpu加速,谷歌文档提到需要加上这个属性来规避bug
                # optionsOrder.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
                optionsOrder.add_argument('--disable-dev-shm-usage')  # 大量渲染时候写入/tmp而非/dev/shm
                optionsOrder.add_argument('--ignore-certificate-errors')  # 忽略掉那些证书错误
                optionsOrder.add_argument('--ignore-ssl-errors')  # 忽略掉ssl错误
                optionsOrder.add_argument("--disable-browser-side-navigation")
                optionsOrder.add_argument('--incognito')    # 隐身模式（无痕模式）
                # optionsOrder.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面

                # 设置浏览器分辨率（窗口大小），无头模式下必须设置
                if self.screenRealX is None:
                    optionsOrder.add_argument("--window-size=1920,1080")
                else:
                    logger.debug("当前显示器分辨率{},{}".format(self.screenRealX, self.screenRealY))
                    optionsOrder.add_argument("--window-size={},{}".format(self.screenRealX, self.screenRealY))

                # 自动化测试
                if self.taskId is not None:
                    # ipad网页（判断只适用本项目）
                    if '/apphd-web/' in self.url:
                        self.pixelRatio = 2.0
                        # mobileEmulation = {'deviceName': 'iPad'}
                        # width: 设备宽度、height: 设备高度、pixelRatio: 设备像素密度
                        mobileEmulation = {"deviceMetrics": {"width": 1024, "height": 768, "pixelRatio": self.pixelRatio}}
                        # mobileEmulation = {"deviceMetrics": {"width": 512, "height": 384, "pixelRatio": self.pixelRatio}}
                        # mobileEmulation = {"deviceMetrics": {"width": 1366, "height": 1024, "pixelRatio": self.pixelRatio}}
                        optionsOrder.add_experimental_option('mobileEmulation', mobileEmulation)
                    # app网页（判断只适用本项目）
                    elif '/app-web/' in self.url:
                        self.pixelRatio = 2.0
                        mobileEmulation = {"deviceMetrics": {"width": 683, "height": 512, "pixelRatio": self.pixelRatio}}
                        # mobileEmulation = {"deviceMetrics": {"width": 375, "height": 600, "pixelRatio": self.pixelRatio}}
                        optionsOrder.add_experimental_option('mobileEmulation', mobileEmulation)
                else:
                    logger.debug("chrome浏览器无头模式")
                    optionsOrder.add_argument('--headless')  # 无头模式,浏览器不提供可视化页面

                optionsOrder.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
                optionsOrder.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
                # optionsOrder.add_argument('--auto-open-devtools-for-tabs')  # 启动时打开F12开发者工具
                service_args = ['--verbose', '--no-sandbox']  # 沙盒模式运行

                if self.enabledProxy == 'Y':
                    # 代理
                    if platformSystem == "Windows":
                        self.proxyserver = Server("basic\\browsermob-proxy\\bin\\browsermob-proxy.bat")
                    else:
                        self.proxyserver = Server("basic/browsermob-proxy/bin/browsermob-proxy")
                    self.proxyserver.start()
                    self.loaclProxyNum = 0
                    self.proxy = self.proxyserver.create_proxy()
                    self.proxy.new_har("ht_list2", options={'captureContent': True})
                    optionsOrder.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
                    logger.debug('启动{}'.format(self.proxyserver))

                optionsOrder.add_experimental_option('w3c', False)  # 关闭w3c验证，则可以使用TouchActions滑动屏幕
                # caps = DesiredCapabilities.CHROME
                # caps['loggingPrefs'] = {'performance': 'ALL'}
                # caps['loggingPrefs'] = {'browser': 'ALL'}
                caps = {
                    'browserName': 'chrome',
                    'loggingPrefs': {
                        'browser': 'ALL',
                        'driver': 'ALL',
                        'performance': 'ALL',
                    },
                    'goog:chromeOptions': {
                        'perfLoggingPrefs': {
                            'enableNetwork': True,
                        },
                        'w3c': False,
                    },
                }
                self.driverWeb = seleniumWebdriver.Chrome(chrome_options=optionsOrder, service_args=service_args, desired_capabilities=caps)
                # self.driverWeb = seleniumWebdriver.Chrome()
                self.ifbrowserTypeRight = 1
                break

            if case("ie"):
                # IeDriver = "C:/Program Files (x86)/Internet Explorer/IEDriverServer.exe"
                # os.environ["seleniumWebdriver.ie.driver"] = IeDriver
                # self.driver = seleniumWebdriver.Ie(IeDriver)
                self.driverWeb = seleniumWebdriver.Ie()
                self.ifbrowserTypeRight = 1
                break

            if case("firefox"):
                # from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
                # binary = FirefoxBinary('F:\FirefoxPortable\Firefox.exe')
                # self.driver = seleniumWebdriver.Firefox(firefox_binary=binary)
                self.driverWeb = seleniumWebdriver.Firefox()
                self.ifbrowserTypeRight = 1
                break

            if case("PhantomJS"):
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                user_agent = "Mozilla/5.0WindowsNT6.1WOW64AppleWebKit/535.8KHTML,likeGeckoBeamrise/17.2.0.9Chrome/17.0.939.0Safari/535.8"
                dcap["phantomjs.page.settings.userAgent"] = user_agent
                self.driverWeb = seleniumWebdriver.PhantomJS(desired_capabilities=dcap)
                self.ifbrowserTypeRight = 5
                break

            if case("android"):
                PATH = lambda p: os.path.abspath(
                    os.path.join(os.path.dirname(__file__), p)
                )
                desired_caps = {}
                desired_caps['platformName'] = 'Android'  # iOS, Android, orFirefoxOS
                desired_caps['platformVersion'] = '4.4.2'
                desired_caps['deviceName'] = 'Android Emulator'  # iPhone Simulator, iPad Simulator, iPhone Retina 4-inch, Android Emulator, Galaxy S4
                desired_caps['app'] = PATH(self.__AppArdPath__)
                desired_caps["unicodeKeyboard"] = "True"
                desired_caps["resetKeyboard"] = "True"

                self.driverAndroid = appiumWebdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

                self.ifbrowserTypeRight = 2
                break

            if case("ios"):
                PATH = lambda p: os.path.abspath(
                    os.path.join(os.path.dirname(__file__), p)
                )
                desired_caps = {}
                desired_caps['platformName'] = 'ios'  # iOS, Android, orFirefoxOS
                desired_caps['platformVersion'] = '10.2'
                desired_caps['deviceName'] = 'iPhone 7'  # iPhone Simulator, iPad Simulator, iPhone Retina 4-inch, Android Emulator, Galaxy S4
                desired_caps['app'] = PATH(self.__AppIosPath__)
                desired_caps["unicodeKeyboard"] = "True"
                desired_caps["resetKeyboard"] = "True"

                self.driverIos = appiumWebdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

                self.ifbrowserTypeRight = 3
                break

            if case("api"):
                self.ifbrowserTypeRight = 6
                self.enabledProxy = 'N'
                break

        testName = self.id().split('.')[-1]  # 获取测试用例名
        testNameList = testName.split('_')
        if len(testNameList) > 1:
            nameType = testNameList[-1]
            if ('A' in nameType) or ('I' in nameType):
                if self.ifbrowserTypeRight == 1:
                    PATH = lambda p: os.path.abspath(
                        os.path.join(os.path.dirname(__file__), p)
                    )
                    desired_caps = {}
                    desired_caps['platformName'] = 'Android'
                    desired_caps['platformVersion'] = '4.4.2'
                    desired_caps['deviceName'] = 'Android Emulator'
                    desired_caps['app'] = PATH(self.__AppArdPath__)
                    desired_caps["unicodeKeyboard"] = "True"
                    desired_caps["resetKeyboard"] = "True"
                    self.driverAndroid = appiumWebdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
                    self.ifbrowserTypeRight = 4
        # else:

        if self.ifbrowserTypeRight == 1:
            self.driverWeb.implicitly_wait(0.1)  #设置隐式等待
        elif self.ifbrowserTypeRight == 2:
            self.driverAndroid.implicitly_wait(0.1)  # 设置隐式等待

            t = threading.Thread(target=self.myWtScreenRecordAsFileArd)
            t.start()
        elif self.ifbrowserTypeRight == 3:
            self.driverAndroid.implicitly_wait(0.1)  # 设置隐式等待
        elif self.ifbrowserTypeRight == 4:
            self.driverWeb.implicitly_wait(0.1)  # 设置隐式等待
            self.driverAndroid.implicitly_wait(0.1)  # 设置隐式等待

            t = threading.Thread(target=self.myWtScreenRecordAsFileArd)
            t.start()
        elif self.ifbrowserTypeRight == 5:
            self.driverWeb.implicitly_wait(0.1)  # 设置隐式等待
        elif self.ifbrowserTypeRight == 6:
            self.driverWeb = None
        else:
            logger.error('浏览器类型只能是chrome、ie、firefox或android，但输入的浏览器类型为：{}'.format(self.browserType))


    def tearDown(self):
        """"""
        testName = self.id().split('.')[-1]  # 获取测试用例名
        timeStr = self.mySysGetLocalTime()

        try:
            if self.ifbrowserTypeRight == 1:
                if self.taskId is not None:
                    self.__upLoadImg(self.driverWeb, testName, timeStr, 'web')
                self.driverWeb.quit()
                if self.enabledProxy == 'Y':
                    self.proxyserver.stop()
            elif self.ifbrowserTypeRight == 2:
                self.ifScreenRecord = 0
                t = threading.Thread(target=self.myWtExportFromArdToPC, args=(self.screenRecordFileList, ))
                t.start()

                self.__upLoadImg(self.driverAndroid, testName, timeStr, 'Android')
                self.driverAndroid.quit()
            elif self.ifbrowserTypeRight == 3:
                self.__upLoadImg(self.driverAndroid, testName, timeStr, 'ios')
                self.driverAndroid.quit()
            elif self.ifbrowserTypeRight == 4:
                self.ifScreenRecord = 0
                t = threading.Thread(target=self.myWtExportFromArdToPC, args=(self.screenRecordFileList, ))
                t.start()
                # p = multiprocessing.Process(target=self.myWtExportFromArdToPC)
                # p.start()
                # p.join()
                # p = Process(target=self.myWtExportFromArdToPC)
                # p.start()

                if self.taskId is not None:
                    if self.webOrPhone == 1:
                        self.__upLoadImg(self.driverWeb, testName, timeStr, 'web')
                    else:
                        self.__upLoadImg(self.driverAndroid, testName, timeStr, 'Android')

                self.driverWeb.quit()
                try:
                    self.driverAndroid.quit()
                except:
                    logger.error('{}'.format(traceback.format_exc()))
            elif self.ifbrowserTypeRight == 5:
                if self.taskId is not None:
                    self.__upLoadImg(self.driverWeb, testName, timeStr, 'PhantomJS')
                self.driverWeb.quit()
            elif self.ifbrowserTypeRight == 6:
                self.driverWeb = None
            else:
                logger.error('浏览器类型只能是chrome、ie、firefox或android，但输入的浏览器类型为：{}'.format(self.browserType))
        except:
            logger.error(traceback.format_exc())

        if self.browserType == "firefox":
            self.mySysCloseProcess("firefox.exe")
            self.mySysCloseProcess("WerFault.exe")

        self.myWtCheckProxyResult()


    def __upLoadImg(self, driver, testName, timeStr, type):
        """更新截图"""
        try:
            result = None
            picName = '{}{}{}{}_{}.png'.format(os.getcwd(), self.pathReportPic, testName, timeStr, type)  # 图片名称
            if self.resultPicName is not None:
                self.mySysCopyFile(self.resultPicName, picName)
                self.myWtScreenshotPrint(picName)
            else:
                result = self.myWtGet_screenshot_as_fileEx(driver, picName, 1)
            if result is not None:
                self.MyReqClient.uploadImg(self.taskId, self.caseId, self.browserType, picName)  # 上传图片
        except:
            logger.error('{}'.format(traceback.format_exc()))


    def myWtGet_screenshot_as_fileEx(self, driver, picName, printlog=0):
        """get_screenshot_as_file扩展，添加错误重试功能
        picName为图片名
        printlog=0时不print日志，！=0则print日志"""
        fileSize = 0
        NumberTimes = 1
        while fileSize == 0:
            try:
                driver.get_screenshot_as_file(picName)  # 截图保存
                fileSize = os.path.getsize(picName)
                # logger.debug('文件大小(字节) ：{} ({})'.format(fileSize, picName))

                if NumberTimes >= self.maxNumberTimes:
                    logger.error('截图失败：{}'.format(picName))
                    return None
                NumberTimes = NumberTimes + 1
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error('截图失败：{} {}'.format(picName, traceback.format_exc()))
                    return None
                NumberTimes = NumberTimes + 1
        logger.info('截图: {}'.format(picName))
        if printlog != 0:
            self.myWtScreenshotPrint(picName)
            # print('screenshot: {}'.format(picName))
            # print('testcasename: [{}][{}][{}]'.format(self.taskId.split('/')[-1], self.sheetName, self.caseId))
        return True


    def myWtScreenshotPrint(self, picName):
        """print日志
        picName为文件名"""
        print('screenshot: {}'.format(picName))
        print('testcasename: [{}][{}][{}][{}]'.format(self.taskId.split('/')[-1], self.sheetName, self.caseId, self.url))


    def myWtScreenshotAsFile(self, driver, rectangle=[], temppath=None):
        """截取整个屏幕截图
        rectangle为矩形坐标[x, y, width, height]，默认为空
        temppath为非None时，在临时目录截屏幕图，返回文件名"""
        if temppath is not None:
            PATH = lambda p: os.path.abspath(p)
            TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
            self.myWtGet_screenshot_as_fileEx(driver, TEMP_FILE)
            return TEMP_FILE

        testName = self.id().split('.')[-1]  # 获取测试用例名
        timeStr = self.mySysGetLocalMillisecond()
        picName = '{}{}{}{}.png'.format(os.getcwd(), self.pathReportPic, testName, timeStr)  # 图片名称
        picBakName = '{}{}{}{}.bak.png'.format(os.getcwd(), self.pathReportPic, testName, timeStr)  # 图片名称

        self.resultPicName = picName

        if len(rectangle) == 0:
            self.myWtGet_screenshot_as_fileEx(driver, picName)
        else:
            self.myWtGet_screenshot_as_fileEx(driver, picBakName)

            x, y, width, height = rectangle
            im = Image.open(picBakName)
            draw = ImageDraw.Draw(im)  # 实例化一个对象
            picX = im.size[0]
            picY = im.size[1]
            logger.debug("图片大小:{},{}".format(picX, picY))

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
                #         ratio = 1
                #     else:
                #         ratio = 1
            logger.debug("ratio={}, self.pixelRatio={}".format(ratio, self.pixelRatio))
            x = x*ratio
            if x > picX:
                x = picX
            y = y*ratio
            if y > picY:
                y = picY
            xwidth = x + width  # *ratio
            if xwidth > picX:
                xwidth = picX
            yheight = y + height  # *ratio
            if yheight > picY:
                yheight = picY
            draw.line((x, y, xwidth, y, xwidth, yheight, x, yheight, x, y), fill="#ff0500", width=5)
            im.save(picName)

        return picName


    def myWtScreenshotByElementAsFile(self, driver, element):
        """截取控件截图"""
        fileName = self.myWtScreenshotAsFile(driver)

        # 获取元素bounds
        location = element.location
        size = element.size

        x = None
        y = None
        if self.browserHeadless == 'UI':
            x = float(location['x']) / self.screenScaling
            y = float(location['y']) / self.screenScaling
        else:
            x = float(location['x'])
            y = float(location['y'])
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
            #     # if self.screenScaling is not None:
            #     #     ratio = self.screenScaling
            #     # else:
            #     #     ratio = 1
            # else:
            #     if self.screenScaling is not None:
            #         ratio = self.screenScaling
            #     else:
            #         ratio = 1
        x = x * ratio
        y = y * ratio

        box = (x, y, x + width, y + height)

        # 截取图片
        # image = Image.open(fileName)
        fp = open(fileName, 'rb')
        image = Image.open(fp)
        image.load()
        newImage = image.crop(box)
        newImage.save(fileName)
        fp.close()
        logger.debug('控件({})(x:{},y:{},width:{},height:{})截图：{}'.format(element, x, y, width, height, fileName))
        del image
        return fileName


    def myWtScreenshotByElement(self, driver, element):
        """ 截取整个控件截图，存储至系统临时目录下"""
        PATH = lambda p: os.path.abspath(p)
        TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
        self.myWtGet_screenshot_as_fileEx(driver, TEMP_FILE)

        # 获取元素bounds
        location = element.location
        size = element.size

        x = None
        y = None
        if self.browserHeadless == 'UI':
            x = float(location['x']) / self.screenScaling
            y = float(location['y']) / self.screenScaling
        else:
            x = float(location['x'])
            y = float(location['y'])
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
        x = x * ratio
        y = y * ratio

        box = (x, y, x + width, y + height)

        # 截取图片
        # image = Image.open(TEMP_FILE)
        fp = open(TEMP_FILE, 'rb')
        image = Image.open(fp)
        image.load()
        fp.close()
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)
        logger.debug('控件({})(x:{},y:{},width:{},height:{})截图：{}'.format(element, x, y, width, height, TEMP_FILE))
        del image
        return TEMP_FILE


    def myWtScreenshotByxy(self, driver, x=0, y=210 , width=300, height=150):
        """ 截取坐标截图，存储至系统临时目录下"""
        PATH = lambda p: os.path.abspath(p)
        TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")
        self.myWtGet_screenshot_as_fileEx(driver, TEMP_FILE)

        box = (x, y, x + width, y + height)

        # 截取图片
        # image = Image.open(TEMP_FILE)
        fp = open(TEMP_FILE, 'rb')
        image = Image.open(fp)
        image.load()
        fp.close()

        newImage = image.crop(box)
        newImage.save(TEMP_FILE)
        logger.debug('(x:{},y:{},width:{},height:{})截图：{}'.format(x, y, width, height, TEMP_FILE))
        del image
        logger.debug(TEMP_FILE)
        return TEMP_FILE


    def myWtScreenshotByXyAsFile(self, driver, x=0, y=210 , width=300, height=150):
        """按坐标截取截图"""
        fileName = self.myWtScreenshotAsFile(driver)

        box = (x, y, x + width, y + height)

        # 截取图片
        # image = Image.open(fileName)
        fp = open(fileName, 'rb')
        image = Image.open(fp)
        image.load()
        newImage = image.crop(box)
        newImage.save(fileName)
        fp.close()
        del image
        return fileName


    def myWtImageCompare(self, oldImage, newImage, percent=10):
        """ 对比图片
        oldImage, newImage为两个对应的图片全路径文件名
        percent值设为0，则100%相似时返回True，设置的值越大，相差越大"""
        import math
        import operator

        # image1 = Image.open(oldImage)
        # image2 = Image.open(newImage)
        fp = open(oldImage, 'rb')
        image1 = Image.open(fp)

        fp = open(newImage, 'rb')
        image2 = Image.open(fp)


        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        fp.close()
        fp.close()
        del image1
        del image2

        differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            logger.debug('图片差异度：{} ({}) ({})'.format(differ, oldImage, newImage))
            return True
        else:
            logger.debug('图片差异度：{} ({}) ({})'.format(differ, oldImage, newImage))
            return False


    def myWtImageFindTemplate(self, oldImage, newImage, confidence=None):
        """ 在大图片oldImage中查找小图片newImage，输入两个对应的图片全路径文件名
        confidence为相似度
        返回{'result': (445.5, 222.5), 'rectangle': ((442, 219), (442, 226), (449, 219), (449, 226)), 'confidence': 0.9933133125305176}
        其中confidence匹配相似度，rectangle匹配图片在原始图像上四边形的坐标，result匹配图片在原始图片上的中心坐标点"""
        yuan = ac.imread(oldImage)
        mubi = ac.imread(newImage)
        if confidence is not None:
            return ac.find_template(yuan, mubi, confidence)
        else:
            return ac.find_template(yuan, mubi)


    def myWtImageGrayProcess(self, fileName):
        """ 图片灰度处理
        fileName为要处理的图片全路径名
        返回处理后的全路径文件名"""
        im = Image.open(fileName)
        im_gray = im.convert('L')
        newfileName = "{}.png".format(fileName)
        im_gray.save(newfileName)
        return newfileName


    def myWtImageFindSimilarColor(self, fileName, rgb, deviation=0):
        """ 图片中查找相同或相似点
        fileName为要处理的图片全路径名
        rgb为颜色，如[52, 123, 205]
        deviation为颜色最大相差值，默认0
        返回所有满足条件坐标列表"""
        pr, pg, pb = rgb
        img = Image.open(fileName)
        width, height = img.size  # 获取图片尺寸的长度和宽度
        # 获取图片的图像类型
        if img.mode != 'RGB':
            img = img.convert("RGB")
        pixlist = []
        if self.browserHeadless == 'UI':
            if deviation == 0:
                for x in range(width):
                    for y in range(height):
                        # 获取某个像素位置的值
                        r, g, b = img.getpixel((x, y))
                        if pr == r and pg == g and pb == b:
                            pixlist.append([x * self.screenScaling, y * self.screenScaling])
            else:
                for x in range(width):
                    for y in range(height):
                        # 获取某个像素位置的值
                        r, g, b = img.getpixel((x, y))
                        if abs(pr - r) <= deviation and abs(pg - g) <= deviation and abs(pb == b) <= deviation:
                            pixlist.append([x * self.screenScaling, y * self.screenScaling])
        else:
            if deviation == 0:
                for x in range(width):
                    for y in range(height):
                        # 获取某个像素位置的值
                        r, g, b = img.getpixel((x, y))
                        if pr == r and pg == g and pb == b:
                            pixlist.append([x, y])
            else:
                for x in range(width):
                    for y in range(height):
                        # 获取某个像素位置的值
                        r, g, b = img.getpixel((x, y))
                        if abs(pr - r) <= deviation and abs(pg - g) <= deviation and abs(pb == b) <= deviation:
                            pixlist.append([x, y])
        # logger.debug('坐标：{}'.format(pixlist))
        return pixlist


    def myWtImageSimilarColorSortOut(self, fileName, rgb, colordeviation=0, xydeviation=10):
        """ 图片中查找相同或相似点，并返回
        fileName为要处理的图片全路径名
        rgb为颜色，如[52, 123, 205]
        colordeviation为颜色最大相差值，默认0
        xydeviation为坐标x和y最大相差值，默认10
        返回所有满足条件坐标列表"""
        pixlist = self.myWtImageFindSimilarColor(fileName, rgb, colordeviation)
        newpixlist = []
        for pix in pixlist:
            x, y = pix
            ifadd = 1
            for newpix in newpixlist:
                xx, yy = newpix
                if abs(xx - x) <= xydeviation and abs(yy - y) <= xydeviation:
                    ifadd = 0
                    continue
            if ifadd == 1:
                newpixlist.append([x, y])
        logger.debug('坐标：{}'.format(newpixlist))
        return newpixlist


    def myWtScreenRecordAsFileArd(self):
        """手机录像"""
        screenRecordFileList = []
        while self.ifScreenRecord == 1:
            try:
                d1 = datetime.datetime.now()
                testName = self.id().split('.')[-1]  # 获取测试用例名
                timeStr = self.mySysGetLocalTime()
                fileName = '{}{}.mp4'.format(testName, timeStr)
                cmdStr = 'adb shell screenrecord --bit-rate 2000000 --time-limit 30 /sdcard/{}'.format(fileName)

                out_temp = tempfile.TemporaryFile(mode='w+')  # 得到一个临时文件对象， 调用close后，此文件从磁盘删除
                # out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
                fileNo = out_temp.fileno()  # 获取临时文件的文件号
                sub = subprocess.Popen(cmdStr, shell=True, stdout=fileNo, stderr=fileNo)
                sub.wait()

                self.screenRecordFileList = self.mySysListAddLimit(screenRecordFileList, fileName, 3)

                # 从临时文件读出shell命令的输出结果
                out_temp.seek(0)
                rt = out_temp.read()
                out_temp.close()
                # # 以换行符拆分数据，并去掉换行符号存入列表
                # rt_list = rt.strip().split('\n')
                # logger.debug(rt)

                logger.info('录像：{}'.format(fileName))

                d2 = self.mySysTimeGapSec(d1)
                if d2 < 28:
                    time.sleep(28 - d2)
            except:
                logger.error('{}'.format(traceback.format_exc()))
            # finally:
            #     if out_temp:
            #         out_temp.close()
        self.ifScreenRecord = 1


    def myWtExportFromArdToPC(self, fileNameList):
        """从手机导出文件到PC"""
        time.sleep(31)
        try:
            for fileName in fileNameList:
                cmdStr = 'adb pull /sdcard/{} {}{}{}'.format(fileName, os.getcwd(), self.pathReportPic, fileName)

                out_temp = tempfile.TemporaryFile(mode='w+')  # 得到一个临时文件对象， 调用close后，此文件从磁盘删除
                # out_temp = tempfile.SpooledTemporaryFile(bufsize=10 * 1000)
                fileNo = out_temp.fileno()  # 获取临时文件的文件号
                sub = subprocess.Popen(cmdStr, shell=True, stdout=fileNo, stderr=fileNo)
                sub.wait()

                # 从临时文件读出shell命令的输出结果
                out_temp.seek(0)
                rt = out_temp.read()
                out_temp.close()
                # # 以换行符拆分数据，并去掉换行符号存入列表
                # rt_list = rt.strip().split('\n')
                # logger.debug(rt)

                if "1 file pulled" in rt:
                    logger.info('导出录像：{}{}{}'.format(os.getcwd(), self.pathReportPic, fileName))
                else:
                    logger.error('导出录像失败：{}{}{} {}'.format(os.getcwd(), self.pathReportPic, fileName, rt))
        except:
            logger.error('{}'.format(traceback.format_exc()))


    def myWtGetProxyResult(self):
        """截取代理接口所有结果
        代理目录为autoTest/basic/browsermob-proxy"""
        proxy = self.proxy
        result = proxy.har
        # logger.debug(result)
        return result


    def myWtGetProxyAllResult(self):
        """取代理接口全部结果:
        res = self.myWtGetProxyAllResult()
        结果列表中再取res['request']  res['response']"""
        if self.enabledProxy == 'Y':
            result = self.myWtGetProxyResult()
            entries = result['log']['entries']
            localList = []
            for res in entries:
                localList.append(res)
            logger.debug('本次GetProxy取接口数：{}'.format(len(entries)))
            # logger.debug(localList)
            return localList
        else:
            return []


    def myWtGetProxyNewResult(self):
        """取代理接口最新结果:
        res = self.myWtGetProxyNewResult()
        结果列表中再取res['request']  res['response']"""
        result = self.myWtGetProxyResult()
        entries = result['log']['entries']
        allNum = len(entries)
        localList = []
        for res in range(self.loaclProxyNum, allNum):
            localList.append(entries[res])
        logger.debug('本次GetProxy取接口数：{}  全部接口数：{}'.format(allNum - self.loaclProxyNum, allNum))
        self.loaclProxyNum = allNum
        # logger.debug(localList)
        return localList


    def myWtGetProxyNewAloneResult(self, localList, url):
        """取代理接口最新查询过滤url的结果:
        res = self.myWtGetProxyNewAloneResult(asdf, 'getChannelChinaAreaInfo')
        结果列表中再取res['request']  res['response']"""
        newlist = []
        for res in localList:
            request = res['request']
            requrl = request['url']
            if url in requrl:
                response = res['response']
                data = {
                    'request': request,
                    'response': response,
                }
                newlist.append(data)
        # logger.debug(newlist)
        return newlist


    def myWtCheckProxyResult(self):
        """检查代理中是否401和501之类的错误，code不为000000的错误，响应时间大于300ms也会打印error日志"""
        if self.enabledProxy == 'Y':
            result = self.myWtGetProxyResult()
            # self.mySysWriteFile(str(result['log']['entries']), 'D:/cc.txt')
            for res in result['log']['entries']:
                request = res['request']
                response = res['response']
                resptime = res['time']
                status = response['status']

                # if resptime > 300:
                #     # logger.error('接口响应时间{}ms\nrequest:{}\nresponse:{}'.format(resptime, request, response))
                #     logger.warning('接口响应时间{}ms\nrequest:{}'.format(resptime, request))

                firstchar = str(status)[0]
                # if firstchar in ['4', '5']:
                if firstchar in ['5']:
                    # http返回4和5开头报错
                    logger.error('request:{}\nresponse:{}'.format(request, response))
                    # self.mySysAssert('request:{}\nresponse:{}'.format(request, response))
                else:
                    # 业务code返回非000000报错，每个系统可能不一样，要单独定制
                    # logger.debug('request:{}\nresponse:{}'.format(request, response))
                    # if (response['content'].get('text') is not None) and (type(response['content']).__name__ == 'dict') and (response['content']['text'].get('code') is not None) and (response['content']['text'][0] == '{'):
                    if ('text' in response['content']) and (type(response['content']).__name__ == 'dict') and ('code' in response['content']['text']) and (response['content']['text'][0] == '{'):
                        textdict = json.loads(str(response['content']['text']))
                        # if textdict.get('code') is not None:
                        if 'code' in textdict:
                            code = json.loads(str(response['content']['text']))['code']
                            if code != "000000":
                                logger.error('request:{}\nresponse:{}'.format(request, response))
                                # self.mySysAssert('request:{}\nresponse:{}'.format(request, response))


    def myWtGetJsLog(self, driver, jsLogExclude=[]):
        """获取控制台js log日志信息，如果控制台日志报错则打印error日志"""
        if self.enabledGetJsLog == 'Y':
            browser = driver.get_log('browser')  # 控件台日志
            # browser = driver.get_log('driver')
            # logger.debug(browser)
            logger.debug('控制台js log总个数：{}'.format(len(browser)))
            num = 0
            for entry in browser:
                # logger.debug(entry['level'])  # INFO DEBUG WARNING SEVERE
                # if entry['level'] == 'ERROR' or entry['level'] == 'SEVERE':
                if entry['level'] not in ['INFO', 'DEBUG', 'WARNING']:
                    # logger.error(entry['message'])
                    iferror = 1
                    for jsLog in jsLogExclude:
                        # if jsLog in str(entry['message']):
                        if jsLog in str(entry):
                            iferror = 0
                            break
                    if iferror == 1:
                        logger.error('控制台js log：{}'.format(entry))
                        # self.mySysAssert('控制台js log：{}'.format(entry))
                        num = num + 1
            logger.debug('控制台js log错误个数：{}'.format(num))


    def myWtPerformanceNetworkLog(self, driver, beginWaitTime=1, endWaitTime=10, excludeList=[]):
        """获取Google Chrome网页DevTools的Network接口请求和返回信息
        输入参数：driver
        beginWaitTime为进入过程之前等待时间，默认1秒
        endWaitTime为进入过程处理最大等待时间，默认10秒
        excludeList为不处理的url或url关键字列表
        返回字典：{"8312.62"{
                'url':"http:www.c.com",
                'request_postData': None,
                'request_headers': None,
                'response': '',
                'status': '',
                'starttimestamp': 1646808543151,
                'endtimestamp': 1646808545156,
                'responseTime': 235,
            },
            "6575.62"{
                'url': "http:www.b.com",
                'request_postData': "",
                'request_headers': None,
                'response': None,
                'status': '',
                'starttimestamp': 1646808543151,
                'endtimestamp': 1646808545156,
                'responseTime': 235,
            }}
        其中responseTime为接口响应时间，单位为ms毫秒，starttimestamp开始时间，endtimestamp为结束时间"""
        logger.debug("***开始获取Chrome网页Network接口请求和返回信息")
        time.sleep(beginWaitTime)
        performanceList = {}
        d1 = datetime.datetime.now()
        while 1 == 1:
            request_log = driver.get_log('performance')
            for item in request_log:
                # logger.debug(item)
                message = json.loads(item['message'])
                # logger.debug(message)
                method = message['message']['method']
                messageparams = message['message']['params']
                requestId = messageparams.get('requestId')  # 得到requestId
                # logger.debug("requestId:{}".format(requestId))
                if method == "Network.requestWillBeSent":
                    request = messageparams.get('request')
                    if request is not None:
                        url = request.get('url')
                        # logger.debug(url)
                        # 排除处理
                        excludeif = 0
                        for exclude in excludeList:
                            if exclude in url:
                                excludeif = 1
                                break
                        if excludeif == 1:
                            continue

                        if performanceList.get(requestId) is None:
                            performanceList[requestId] = {}

                        postData = request.get('postData')
                        # logger.debug("postData: {}".format(postData))
                        headers = request.get('headers')
                        starttimestamp = item.get('timestamp')
                        # logger.debug('starttimestamp: {}'.format(starttimestamp))

                        performanceList[requestId]["url"] = url
                        performanceList[requestId]["request_postData"] = postData
                        performanceList[requestId]["request_headers"] = headers
                        performanceList[requestId]["starttimestamp"] = starttimestamp

                        if performanceList.get(requestId) is not None:
                            endtimestamp = performanceList[requestId].get('endtimestamp')
                            if endtimestamp is not None:
                                timeuse = datetime.datetime.fromtimestamp(endtimestamp / 1000) - datetime.datetime.fromtimestamp(starttimestamp / 1000)
                                responseTime = timeuse.microseconds / 1000.0 + timeuse.seconds * 60
                                performanceList[requestId]['responseTime'] = responseTime

                        # responseBody = None
                        try:
                            # 通过requestId获取接口内容
                            responseBody = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                            # logger.debug("ResponseBody: {}".format(responseBody))
                            performanceList[requestId]["response"] = responseBody
                        except:
                            performanceList[requestId]["response"] = None
                            # logger.error(traceback.format_exc())
                        # logger.debug('requesturl: {}\npostData: {}\nresponse: {}'.format(url, postData, responseBody))

                elif method == "Network.responseReceived":
                    response = messageparams.get('response')
                    if response is not None:
                        if requestId is not None:
                            if performanceList.get(requestId) is None:
                                performanceList[requestId] = {}

                        endtimestamp = item.get('timestamp')
                        # logger.debug('endtimestamp: {}'.format(endtimestamp))
                        performanceList[requestId]["endtimestamp"] = endtimestamp
                        status = response.get('status')
                        performanceList[requestId]["status"] = status
                        # logger.debug('status: {}'.format(status))
                        responseurl = response.get('url')
                        if responseurl is not None:
                            urltmp = performanceList[requestId].get('url')
                            if urltmp is None:
                                performanceList[requestId]['url'] = responseurl

                        if performanceList.get(requestId) is not None:
                            starttimestamp = performanceList[requestId].get('starttimestamp')
                            if starttimestamp is not None:
                                timeuse = datetime.datetime.fromtimestamp(endtimestamp / 1000) - datetime.datetime.fromtimestamp(starttimestamp / 1000)
                                responseTime = timeuse.microseconds / 1000.0 + timeuse.seconds * 1000
                                performanceList[requestId]['responseTime'] = responseTime

                        try:
                            # 通过requestId获取接口内容
                            responseBody = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                            # logger.debug("ResponseBody: {}".format(responseBody))
                            performanceList[requestId]["response"] = responseBody
                        except:
                            performanceList[requestId]["response"] = None
                            # logger.error(traceback.format_exc())

            # 如果存在不全的信息，则取self.myWtGetProxyAllResult()更新对应信息，如果信息全则退出
            logStr = None
            ifbreak = 0
            notFinishNum = 0
            for pfm in performanceList:
                # if performanceList[pfm]['url'] != "data:," and (performanceList[pfm].get("starttimestamp") is None or performanceList[pfm].get("endtimestamp") is None):
                if "http" in performanceList[pfm].get('url') and ("endtimestamp" not in performanceList[pfm] and "responseTime" not in performanceList[pfm]):
                    localListfind = 0
                    localList = self.myWtGetProxyAllResult()
                    for local in localList:
                        responsetmp = local.get("response")
                        if responsetmp is not None:
                            timetmp = local.get("time")
                            if timetmp is not None:
                                performanceList[pfm]['responseTime'] = timetmp
                                logger.debug("取Proxy更新responseTime：\n{} \n{}".format(pfm, responsetmp))
                                # logger.debug("取Proxy更新responseTime：\n{}: {}\n{}".format(pfm, performanceList[pfm], responsetmp))
                                localListfind = 1

                            contenttmp = responsetmp.get("content")
                            if contenttmp is not None:
                                contenttexttmp = contenttmp.get("text")
                                if contenttexttmp is not None:
                                    if type(contenttexttmp) == dict:
                                        performanceList[pfm]['response']['body'] = contenttexttmp
                                        logger.debug("取Proxy更新body：{}".format(responsetmp))
                                    break
                    if localListfind == 1:
                        continue

                    logStr = "等待接口信息返回超时：{}: {}".format(pfm, performanceList[pfm])
                    ifbreak = 1
                    notFinishNum = notFinishNum + 1
                    # break
            if ifbreak == 0:
                logger.debug("performanceList接口数: {}  接口信息收集成功".format(len(performanceList)))
                # for pf in performanceList:
                #     logger.debug("{}: {}".format(pf, performanceList[pf]))
                logger.debug("***结束获取Chrome网页Network接口请求和返回信息")
                return performanceList

            # 大于10秒返回
            if self.mySysTimeGapSec(d1) >= endWaitTime:
                logger.debug(logStr)
                logger.debug("performanceList接口数: {}  其中信息不全接口：{}".format(len(performanceList), notFinishNum))
                # for pf in performanceList:
                #     logger.debug("{}: {}".format(pf, performanceList[pf]))
                logger.debug("***结束获取Network接口请求和返回信息")
                return performanceList


    def __getAppPathConf(self):
        """读取conf/config.ini配置文件"""
        fileName = '{}/conf/config.ini'.format(os.getcwd())
        cf = configparser.ConfigParser()
        # logger.debug('读取客户端和服务端IP配置文件:{}'.format(fileName))
        cf.read(fileName)
        sections =  cf.sections()
        if 'APP' in sections:
            self.__AppArdPath__ = cf.get('APP', 'ArdPath')
            self.__AppIosPath__ = cf.get('APP', 'IosPath')
        else:
            logger.info('找不到APP的Path配置文件')



    ###############################
    """控件操作"""
    ###############################
    def myWtFindElement(self, element, myby, myCtrlIdent, ifPrintErr=1, ifDisEna=1, maxWaittime=-1):
        """函数说明：选择单个控件
        输入参数：driver，myby为By.ID等，myCtrlIdent为控件标识
        输出参数：driver.find_element(myby, myCtrlIdent)"""
        # logger.debug('Ex开始')  #######
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime

        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # element.find_element(myby, myCtrlIdent)
                # logger.debug('Ex ifDisEna 开始')  #######
                if ifDisEna == 1:
                    # 判断是否可见
                    while not (element.find_element(myby, myCtrlIdent).is_displayed()):
                        if self.mySysTimeGapSec(d1) >= maxWaittime:
                            logger.warning('{}：{}  is not displayed'.format(myby, myCtrlIdent))
                            return None
                        time.sleep(0.1)
                    # 判断是否可用
                    while not (element.find_element(myby, myCtrlIdent).is_enabled()):
                        if self.mySysTimeGapSec(d1) >= maxWaittime:
                            logger.warning('{}：{}  is not enabled'.format(myby, myCtrlIdent))
                            return None
                        time.sleep(0.1)
                # logger.debug('{}：{}'.format(myby, myCtrlIdent))
                # logger.debug('Ex ifDisEna 结束')  #######
                return element.find_element(myby, myCtrlIdent)
            except:
                # logger.debug('Ex except')  #######
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    if ifPrintErr == 1:
                        err = '{}：{}  {}'.format(myby, myCtrlIdent, traceback.format_exc())
                        self.mySysAssert(err)
                    return None
                time.sleep(0.1)


    def myWtFindElements(self, element, myby, myCtrlIdent, ifPrintErr=1, ifFindElt=0):
        """函数说明：选择多个控件
        输入参数：driver，myby为By.ID等，myCtrlIdent为控件标识
        输出参数：driver.find_element(myby, myCtrlIdent)"""
        if ifFindElt == 1:
            self.myWtFindElement(element, myby, myCtrlIdent, 0)  # 等待
        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # self.driver.find_elements(myby, myCtrlIdent)
                # logger.debug('{}：{}'.format(myby, myCtrlIdent))
                return element.find_elements(myby, myCtrlIdent)
            except:
                if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                    if ifPrintErr == 1:
                        err = '{}：{}  {}'.format(myby, myCtrlIdent, traceback.format_exc())
                        self.mySysAssert(err)
                    return None
                time.sleep(0.1)


    def myWtElementEx(self, element, ifPrintErr=1, ifDisEna=1, maxWaittime=-1):
        """函数说明：选择控件
        输入参数：driver
        返回参数：None或控件element"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # element
                if ifDisEna == 1:
                    # 判断是否可见
                    while not (element.is_displayed()):
                        if self.mySysTimeGapSec(d1) >= maxWaittime:
                            logger.warning('{}  is not displayed'.format(element))
                            return None
                        time.sleep(0.1)
                    # 判断是否可用
                    while not (element.is_enabled()):
                        if self.mySysTimeGapSec(d1) >= maxWaittime:
                            logger.warning('{}  is not enabled'.format(element))
                            return None
                        time.sleep(0.1)
                return element
            except:
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    if ifPrintErr == 1:
                        logger.error('{}  {}'.format(element, traceback.format_exc()))
                    return None
                time.sleep(0.1)


    def myWtSendKeys(self, element, text, clear=0):
        """在输入框输入对应text值"""
        if clear != 0:
            element.clear()
            element.click()
        element.send_keys(text)
        logger.debug('控件{}输入：{}'.format(element, text))


    def myWtSendKeysElements(self, element, myby, myCtrlIdent, text, clear=0):
        """在对应输入框输入对应text值"""
        eltList = self.myWtFindElements(element, myby, myCtrlIdent)
        for elt in eltList:
            if elt.is_displayed():
                self.myWtSendKeys(elt, text, clear)


    def myWtSendKeysEx(self, element, myby, myCtrlIdent, text, ifPrintErr=1, ifDisEna=1, clear=0):
        """手机，输入框输入对应text值"""
        currentTime = 0
        elt = self.myWtFindElement(element, myby, myCtrlIdent, ifPrintErr, ifDisEna)
        if elt is not None:
            while 1 == 1:
                try:
                    if clear != 0:
                        elt.clear()
                        elt.click()
                    elt.send_keys(text)

                    if myby == 'name':
                        break

                    resultText = elt.get_attribute("text")
                    if resultText == text:
                        break

                    currentTime = currentTime + 1
                    if currentTime >= self.maxNumberTimes:
                        logger.error('控件{} ({})输入失败：{}'.format(myby, myCtrlIdent, text))
                        return None
                except:
                    currentTime = currentTime + 1
                    # logger.error('控件{} ({})输入失败：{}   {}'.format(myby, myCtrlIdent, text, traceback.format_exc()))
                    if currentTime >= self.maxNumberTimes:
                        tmpstr = traceback.format_exc()
                        if tmpstr.find("elt.send_keys") == -1 and tmpstr.find("elt.get_attribute") == -1:
                            logger.error('控件{} ({})输入失败：{}   {}'.format(myby, myCtrlIdent, text, traceback.format_exc()))
                            return None
                        else:
                            break

            logger.debug('控件{} ({})输入：{}'.format(myby, myCtrlIdent, text))
        else:
            logger.error('控件{} ({})输入失败：{}'.format(myby, myCtrlIdent, text))


    def myWtSendKeysWebEx(self, element, myby, myCtrlIdent, text, ifPrintErr=1, ifDisEna=1, clear=0):
        """WEB网页，输入框输入对应text值"""
        currentTime = 0
        elt = self.myWtFindElement(element, myby, myCtrlIdent, ifPrintErr, ifDisEna)
        if elt is not None:
            while 1 == 1:
                try:
                    if clear != 0:
                        elt.clear()
                        elt.click()
                    elt.send_keys(text)

                    resultText = elt.get_attribute("value")
                    if str(resultText).strip() == str(text).strip():
                        break

                    resultText = elt.text
                    if str(resultText).strip() == str(text).strip():
                        break

                    currentTime = currentTime + 1
                    if currentTime >= self.maxNumberTimes:
                        logger.error('控件{} ({})输入失败：{}'.format(myby, myCtrlIdent, text))
                        return None
                except:
                    currentTime = currentTime + 1
                    # logger.error('控件{} ({})输入失败：{}   {}'.format(myby, myCtrlIdent, text, traceback.format_exc()))
                    if currentTime >= self.maxNumberTimes:
                        tmpstr = traceback.format_exc()
                        if tmpstr.find("elt.send_keys") == -1 and tmpstr.find("elt.get_attribute") == -1:
                            logger.error('控件{} ({})输入失败：{}   {}'.format(myby, myCtrlIdent, text, traceback.format_exc()))
                            return None
                        else:
                            break

            logger.debug('控件{} ({})输入：{}'.format(myby, myCtrlIdent, text))
        else:
            logger.error('控件{} ({})输入失败：{}'.format(myby, myCtrlIdent, text))


    def myWtClick(self, element, ifPrintErr=1, maxWaittime=-1):
        """控件点击"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                if element is not None:
                    text = self.mySysStringCleanup(element.text)
                    name = element.get_attribute("name")
                    element.click()
                    # if name == '' or name is None:
                    if text != "":
                        logger.debug('单击控件：({})  text：{}'.format(element, text))
                    else:
                        logger.debug('单击控件：({})  text：{}'.format(element, name))
                else:
                    if ifPrintErr == 1:
                        err = '未找到控件：({})'.format(element)
                        self.mySysAssert(err)
                return True
            except:
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    if ifPrintErr == 1:
                        err = '{}  {}'.format(element, traceback.format_exc())
                        self.mySysAssert(err)
                    return None
                time.sleep(0.1)


    def myWtClickEx(self, element, myby, myCtrlIdent, ifPrintErr=1, ifDisEna=1, maxWaittime=-1):
        """控件点击"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        elt = self.myWtFindElement(element, myby, myCtrlIdent, ifPrintErr, ifDisEna, maxWaittime)
        if elt is not None:
            text = self.mySysStringCleanup(elt.text)
            name = elt.get_attribute("name")
            elt.click()
            # if name == '' or name is None:
            if text != "":
                logger.debug('单击控件：{} ({})  text：{}'.format(myby, myCtrlIdent, text))
            else:
                logger.debug('单击控件：{} ({})  text：{}'.format(myby, myCtrlIdent, name))
        else:
            err = '未找到控件：{} {} ({})'.format(element, myby, myCtrlIdent)
            self.mySysAssert(err)


    def myWtCheckboxRadioSelect(self, element, myby, myCtrlIdent, selected=1, ifPrintErr=1, ifDisEna=1):
        """checkbox ( 复选框 ) 和radio (单选框 )点击选择"""
        elt = self.myWtFindElement(element, myby, myCtrlIdent, ifPrintErr, ifDisEna)
        text = self.mySysStringCleanup(elt.text)
        name = elt.get_attribute("name")
        if elt.get_attribute("checked") == 'false':
            if selected == 1:
                elt.click()
        else:
            if selected == 0:
                elt.click()
        # if name == '' or name is None:
        if text != "":
            logger.debug('单击控件：{} ({})  text：{}'.format(myby, myCtrlIdent, text))
        else:
            logger.debug('单击控件：{} ({})  text：{}'.format(myby, myCtrlIdent, name))


    def myWtSelectByText(self, driver, text):
        """下拉框选择"""
        if text != "":
            Select(driver).select_by_visible_text(text)
        # else:
        #     Select(driver).deselect_by_visible_text(text)


    def myWtEltNonexiContinue(self, element, myby, myCtrlIdent, ifPrintErr=0, maxWaittime=2):
        """控件不存在，则返回None；控件存在，则返回控件
        输入参数：element为driver等
        myby为By.ID等
        myCtrlIdent为控件标识
        返回参数：None或driver.find_element(myby, myCtrlIdent)"""
        time.sleep(1)
        d1 = datetime.datetime.now()
        while 1 == 1:
            try:
                # 判断是否可见
                while not (element.find_element(myby, myCtrlIdent).is_displayed()):
                    if self.mySysTimeGapSec(d1) >= maxWaittime:
                        logger.warning('{}：{}  is not displayed'.format(myby, myCtrlIdent))
                        return None
                    time.sleep(0.1)
                # 判断是否可用
                while not (element.find_element(myby, myCtrlIdent).is_enabled()):
                    if self.mySysTimeGapSec(d1) >= maxWaittime:
                        logger.warning('{}：{}  is not enabled'.format(myby, myCtrlIdent))
                        return None
                    time.sleep(0.1)
                return element.find_element(myby, myCtrlIdent)
            except:
                if ifPrintErr == 1:
                    err = '{}：{}  '.format(myby, myCtrlIdent)
                    self.mySysAssert(err)
                return None


    def myWtFindElementsCpnText(self, driver, myby, myCtrlIdent, text, maxWaittime=-1):
        """判断text相同或in，返回对应控件"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        eltList = self.myWtFindElements(driver, myby, myCtrlIdent)
        ifSuccess = 1
        num = 0
        # logger.debug(eltList)
        for elt in eltList:
            # logger.debug('---' + elt.text + '---')
            # logger.debug('---'+elt.get_attribute("name")+'---')
            if str(text).strip() in str(elt.text).strip() or str(elt.text).strip() == str(text).strip() or str(elt.get_attribute("name")).strip() == str(text).strip():
                # logger.debug('---' + elt.text + '---')
                ifSuccess = 0
                logger.debug('找到控件：{}'.format(text))
                return elt

        if ifSuccess == 1:
            err = '未找到控件：{}'.format(text)
            self.mySysAssert(err)


    def myWtElementsClickNumber(self, element, myby, myCtrlIdent, serialNumber=1, ifFindElt=0):
        """点击控件列表中第几个，默认第一个"""
        self.myWtFindElements(element, myby, myCtrlIdent)
        eltList = self.myWtFindElements(element, myby, myCtrlIdent, 1, ifFindElt)
        num = 1
        ifSuccess = 1
        for elt in eltList:
            # logger.debug(elt)
            if num == serialNumber:
                text = elt.text
                logger.debug('单击控件：{}'.format(text))
                # elt.click()
                self.myWtClick(elt)
                ifSuccess = 0
                return text
            num = num + 1

        if ifSuccess == 1:
            err = '未找到控件：{} {} ({})'.format(element, myby, myCtrlIdent)
            self.mySysAssert(err)


    def myWtElementsChooseTextClick(self, eltList, text, ifBreak=1, serialNumber=0, maxWaittime=-1):
        """判断text相同，则点击"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        ifSuccess = 1
        num = 0
        # logger.debug(eltList)
        for elt in eltList:
            # logger.debug('---' + elt.text + '---')
            # logger.debug('---'+elt.get_attribute("name")+'---')
            if str(elt.text).strip() == str(text).strip() or str(elt.get_attribute("name")).strip() == str(text).strip():
                # logger.debug('---' + elt.text + '---')
                num = num + 1
                eltTmp = self.myWtElementEx(elt, 0, 1, maxWaittime)
                if eltTmp is not None:
                    if serialNumber == 0:
                        eltTmp.click()
                        ifSuccess = 0
                        logger.debug('单击控件：{}'.format(text))
                        # return eltTmp.location
                        if ifBreak == 1:
                            break
                    elif num == serialNumber:
                        # logger.debug('单击控件：{}'.format(text))
                        self.myWtClick(elt)
                        ifSuccess = 0
                        if ifBreak == 1:
                            break
                else:
                    continue

        if ifSuccess == 1:
            err = '未找到控件：{}'.format(text)
            self.mySysAssert(err)


    def myWtElementsChooseTextClickEx(self, driver, myby, myCtrlIdent, text, ifBreak=1, serialNumber=0, maxWaittime=-1):
        """判断text相同，则点击"""
        eltList = self.myWtFindElements(driver, myby, myCtrlIdent)
        self.myWtElementsChooseTextClick(eltList, text, ifBreak, serialNumber, maxWaittime)


    def myWtElementsSimilarTextClick(self, eltList, text, ifBreak=1, serialNumber=0, maxWaittime=-1):
        """判断text相似，则点击"""
        if maxWaittime == -1:
            maxWaittime = self.maxWaittime
        ifSuccess = 1
        num = 0
        # logger.debug(eltList)
        for elt in eltList:
            # logger.debug('---' + elt.text + '---')
            # logger.debug('---'+elt.get_attribute("name")+'---')
            if str(text).strip() in str(elt.text).strip() or str(text).strip() in str(elt.get_attribute("name")).strip():
                # logger.debug('---' + elt.text + '---')
                num = num + 1
                eltTmp = self.myWtElementEx(elt, 0, 1, maxWaittime)
                if eltTmp is not None:
                    if serialNumber == 0:
                        eltTmp.click()
                        ifSuccess = 0
                        logger.debug('单击控件：{}'.format(text))
                        # return eltTmp.location
                        if ifBreak == 1:
                            break
                    elif num == serialNumber:
                        # logger.debug('单击控件：{}'.format(text))
                        self.myWtClick(elt)
                        ifSuccess = 0
                        if ifBreak == 1:
                            break
                else:
                    continue

        if ifSuccess == 1:
            err = '未找到控件：{}'.format(text)
            self.mySysAssert(err)


    def myWtElementsChooseClickEx(self, element, myby, myCtrlIdent, elementEnd, mybyEnd, myCtrlIdentEnd):
        """手机，存在myCtrlIdent，则点击。如果不存在则下拉直到存在，直到myCtrlIdentEnd退出"""
        while 1 == 1:
            elt = self.myWtFindElement(element, myby, myCtrlIdent, 0)
            eltEnd = self.myWtFindElement(elementEnd, mybyEnd, myCtrlIdentEnd, 0)
            if elt is not None:
                self.myWtClick(elt)
                break
            elif eltEnd is not None:
                err = '未找到控件：{}({})'.format(element, myby, myCtrlIdent)
                self.mySysAssert(err)
                break
            else:
                self.myWtPhoneSwipeUp(element)


    def myWtElementsChooseAttributeClick(self, eltList, attributeName, text):
        """判断attribute相同，则点击"""
        ifSuccess = 1
        for elt in eltList:
            # logger.debug('---' + elt.get_attribute(attributeName) + '---')
            if str(elt.get_attribute(attributeName)).strip() == str(text).strip():
                eltTmp = self.myWtElementEx(elt, 0, 1, 1)
                if eltTmp is not None:
                    eltTmp.click()
                    ifSuccess = 0
                    logger.debug('单击控件：{}({})'.format(attributeName, text))
                    # return eltTmp.location
                    break
                else:
                    continue

        if ifSuccess == 1:
            err = '未找到控件：{}({})'.format(attributeName, text)
            self.mySysAssert(err)


    def myWtTablesChooseTextClickElt(self, eltList, text, myby, myCtrlIdent):
        """判断table中的text相同，则点击对应控件"""
        ifSuccess = 1
        for elt in eltList:
            tdList = self.myWtFindElements(elt, By.TAG_NAME, 'td')
            for td in tdList:
                # logger.debug(td.text)
                if td.text == text:
                    logger.debug(td.text)
                    self.myWtClickEx(elt, myby, myCtrlIdent)
                    ifSuccess = 0
                    break
            if ifSuccess == 0:
                break

        if ifSuccess == 1:
            err = '未找到控件：{} {}({})'.format(text, myby, myCtrlIdent)
            self.mySysAssert(err)


    def myWtTablesChooseTextClickEltEx(self, eltList, text, myby, myCtrlIdent, myText):
        """判断table中的text相同，则点击对应控件"""
        ifSuccess = 1
        for elt in eltList:
            if text in elt.text:
                self.myWtElementsChooseTextClickEx(elt, myby, myCtrlIdent, myText)
                ifSuccess = 0
                break
            # tdList = self.myWtFindElements(elt, By.TAG_NAME, 'td')
            # for td in tdList:
            #     # logger.debug(td.text)
            #     if td.text == text:
            #         logger.debug(td.text)
            #         self.myElementsChooseTextClickEx(elt, myby, myCtrlIdent, myText)
            #         ifSuccess = 0
            #         break
            # if ifSuccess == 0:
            #     break

        if ifSuccess == 1:
            err = '未找到控件：{} {}({} {})'.format(text, myby, myCtrlIdent, myText)
            self.mySysAssert(err)


    def myWtElementsChooseTextSendKeys(self, eltList, text, inputStr):
        """判断text相同，则输入inputStr"""
        ifSuccess = 1
        for elt in eltList:
            # logger.debug(elt.text)
            # logger.debug('-'+elt.get_attribute("name")+'-')
            if str(elt.text).strip() == str(text).strip() or str(elt.get_attribute("name")).strip() == str(text).strip():
                eltTmp = self.myWtElementEx(elt, 0, 1)
                if eltTmp is not None:
                    self.myWtSendKeys(eltTmp, inputStr)
                    ifSuccess = 0
                    # return eltTmp.location
                break

        if ifSuccess == 1:
            err = '未找到控件：{}'.format(text)
            self.mySysAssert(err)


    def myWtElementsChooseAttributeSendKeys(self, eltList, attributeName, text, inputStr):
        """判断attribute和text相同，则输入inputStr"""
        ifSuccess = 1
        for elt in eltList:
            # logger.debug('---' + elt.get_attribute(attributeName) + '---')
            if str(elt.get_attribute(attributeName)).strip() == str(text).strip():
                eltTmp = self.myWtElementEx(elt, 0, 1, 1)
                if eltTmp is not None:
                    self.myWtSendKeys(eltTmp, inputStr)
                    ifSuccess = 0
                    # return eltTmp.location
                    break
                else:
                    continue

        if ifSuccess == 1:
            err = '未找到控件：{}({})'.format(attributeName, text)
            self.mySysAssert(err)


    def myWtJSRefreshWaiting(self, driver):
        """JS判断界面是否在等待，加载中"""
        # time.sleep(1)
        logger.debug("JS开始获取网页加载状态")
        maxWaittime = self.maxWaittime
        d1 = datetime.datetime.now()
        while 1 == 1:
            readyState = driver.execute_script('return document.readyState')
            if readyState == 'complete':
                logger.debug("JS结束获取网页加载状态：{}".format(readyState))
                break

            if self.mySysTimeGapSec(d1) >= maxWaittime:
                break


    def myWtActionChains(self, driver):
        """返回ActionChains(driver)"""
        time.sleep(1)
        action = ActionChains(driver)
        return action


    def myWtActionKeydown(self, driver, key):
        """点击键盘"""
        self.myWtActionChains(driver).key_down(key).perform()
        logger.debug('点击键盘：{}'.format(key))
        time.sleep(1)


    def myWtActionMoveToElement(self, driver, elt):
        """移动鼠标到控件上"""
        self.myWtActionChains(driver).move_to_element(elt).perform()
        textContent = self.mySysStringCleanup(str(elt.get_attribute("textContent")))
        if len(textContent) > 4:
            logger.debug('移动鼠标到控件上：{}'.format(textContent[0:4]))
        else:
            logger.debug('移动鼠标到控件上：{}'.format(textContent))
        time.sleep(1)


    def myWtActionclick(self, driver, x, y, leftClick=True):
        """鼠标点击网页坐标
        坐标x和y
        leftClick为True时为鼠标左键点击，为其它为鼠标右键点击"""
        action = self.myWtActionChains(driver)
        if leftClick is True:
            action.move_by_offset(x, y).click().release().perform()
            logger.debug("鼠标左键点击:x={},y={}".format(x, y))
        else:
            action.move_by_offset(x, y).context_click().release().perform()
            logger.debug("鼠标右键点击:x={},y={}".format(x, y))
        # action.move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前
        # action.release().perform()
        time.sleep(1)


    def myWtActionElementclickByXY(self, driver, element, x, y, leftClick=True):
        """鼠标点击控件坐标
        坐标x和y
        leftClick为True时为鼠标左键点击，为其它为鼠标右键点击"""
        action = self.myWtActionChains(driver)
        if leftClick is True:
            action.move_to_element_with_offset(element, x, y).click().release().perform()
            logger.debug("鼠标左键在控件中点击:x={},y={},控件:({})".format(x, y, element))
        else:
            action.move_to_element_with_offset(element, x, y).context_click().release().perform()
            logger.debug("鼠标右键在控件中点击:x={},y={},控件:({})".format(x, y, element))
        # action.move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前
        # action.release().perform()
        time.sleep(1)


    def myWtActionMoveToElementByXY(self, driver, element, x, y):
        """鼠标移动到控件坐标上
        坐标x和y"""
        action = self.myWtActionChains(driver)
        action.move_to_element_with_offset(element, x, y).release().perform()
        logger.debug("鼠标移动到控件坐标:x={},y={}上,控件:({})".format(x, y, element))
        time.sleep(1)


    def myWtTouchActionTap(self, driver, elt):
        """点击控件"""
        time.sleep(1)
        # TouchAction(driver).tap(elt).perform()
        logger.debug('单击控件：{}'.format(elt))
        time.sleep(1)


    def myWtTouchActionLongpress(self, driver, elt):
        """点击长按"""
        time.sleep(1)
        # TouchAction(driver).long_press(elt).wait(2000).perform()
        logger.debug('单击长按控件：{}'.format(elt))
        time.sleep(1)


    def myWtCursorMoveFatherClickElt(self, driver, elt, myby, myCtrlIdent):
        """把鼠标移到控件上，控件上的某个控件显示，点击某个控件"""
        maxWaittime = self.maxWaittime
        d1 = datetime.datetime.now()

        while 1 == 1:
            self.myWtActionChains(driver).move_to_element(elt).perform()
            time.sleep(1)
            anticonClose = self.myWtFindElement(elt, myby, myCtrlIdent, 0)
            if anticonClose is None:
                if self.mySysTimeGapSec(d1) >= maxWaittime:
                    logger.warning('没有找到 {}：{}'.format(myby, myCtrlIdent))
                    break
                time.sleep(1)
                continue
            else:
                self.myWtClick(anticonClose)
                break


    def myWtJsScrollIntoView(self, driver, element, down=True):
        """鼠标向下或上滚动至-元素element可见
        down=True时向下滚动，其它为向上"""
        if down is True:
            driver.execute_script("arguments[0].scrollIntoView();", element)  # 向下滚动至元素可见
            logger.debug('向下滚动至元素可见')
        else:
            driver.execute_script("arguments[0].scrollIntoView(false);", element)  # 向上滚动至元素可见
            logger.debug('向上滚动至元素可见')


    def myWtWndowhandlesOpen(self, driver, allHandlesNum, newhandleNum=None):
        """判断浏览器是否成功打开新handle，并切换到新handle
        allHandlesNum为新打开handle后所有handle的总合数
        newhandleNum为新打开handle的编号，默认新最大编号
        函数返回：handles"""
        d1 = datetime.datetime.now()
        while 1 == 1:
            d1 = datetime.datetime.now()
            handles = driver.window_handles
            if len(handles) >= allHandlesNum:
                break

            if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                self.mySysAssert('打开新窗口失败')
            time.sleep(0.5)

        handles = driver.window_handles
        if newhandleNum is None:
            driver.switch_to.window(handles[len(handles)-1])
        else:
            driver.switch_to.window(handles[newhandleNum])
        return handles


    def myWtWndowhandlesClose(self, driver, handles, num=None):
        """关闭handle，并切换到某handle
        handles为self.myWtWndowhandlesOpen中返回值
        num为要关闭handle的编号，默认切换第一个handle"""
        driver.close()
        if num is None:
            driver.switch_to_window(handles[0])
        else:
            driver.switch_to_window(handles[num])


    ##############################
    """控件检查"""
    ##############################

    def myWtSelectCheck(self, driver, expectText):
        """检查下拉框内容
        对比driver.get_attribute("value")和expectText
        相同返回True，不同返回None"""
        logger.debug('预期下拉框选择：{}'.format(expectText))
        actualValue = driver.get_attribute("value")
        optionList = self.myWtFindElements(By.TAG_NAME, "option", driver)
        for option in optionList:
            tmpValue = option.get_attribute("value")
            if tmpValue == actualValue:
                tmpText = str(option.text)
                if expectText == tmpText:
                    logger.debug('实际下拉框选择：{}'.format(tmpText))
                    return True
                else:
                    err = '内容不相符，预期下拉框选择：{}   实际下拉框选择：{}'.format(expectText, tmpText)
                    self.mySysAssert(err)
                    return None
        err = '内容不相符，预期下拉框选择：{}'.format(expectText)
        self.mySysAssert(err)
        return None


    def myWtInputCheck(self, driver, expectText):
        """检查输入框内容
        对比driver.get_attribute("value")和expectText
        相同返回True，不同返回None"""
        logger.debug('预期输入框内容：{}'.format(expectText))
        # actualText = driver.text#("value")
        actualText = driver.get_attribute("value")
        if expectText == actualText:
            logger.debug('实际输入框内容：{}'.format(actualText))
            return True
        else:
            err = '内容不相符，预期输入框内容：{}    实际输入框内容：{}'.format(expectText, actualText)
            self.mySysAssert(err)
            return None


    def myWtTextCheck(self, driver, expectText, ifFuzzy=0):
        """text检查，对比driver.text和expectText
        ifFuzzy为0则为完全匹配，为1则为模糊匹配
        相同返回True，不同返回None"""
        logger.debug('预期text内容：{}'.format(expectText))
        actualText = driver.text
        if ifFuzzy == 0:
            if expectText == actualText:
                logger.debug('实际text内容：{}'.format(actualText))
                return True
            else:
                err = '内容不相符，实际text内容：{}'.format(actualText)
                self.mySysAssert(err)
                return None
        else:
            if expectText in actualText:
                logger.debug('实际text内容：{}'.format(actualText))
                return True
            else:
                err = '内容不相符，实际text内容：{}'.format(actualText)
                self.mySysAssert(err)
                return None


    def myWtAttributeCheck(self, driver, expectText, attributeName, ifFuzzy=0):
        """属性检查
        driver.get_attribute(attributeName)和expectText对比"""
        logger.debug('预期属性{}内容：{}'.format(attributeName, expectText))
        actualText = driver.get_attribute(attributeName)
        if ifFuzzy == 0:
            if expectText == actualText:
                logger.debug('实际属性{}内容：{}'.format(attributeName, actualText))
                return True
            else:
                err = '内容不相符，实际属性{}内容：{}'.format(attributeName, actualText)
                self.mySysAssert(err)
                return None
        else:
            if expectText in actualText:
                logger.debug('实际text内容：{}'.format(actualText))
                return True
            else:
                err = '内容不相符，实际text内容：{}'.format(actualText)
                self.mySysAssert(err)
                return None


    def myWtH5FlickUp(self, driver, elt, frequency=1, sleepTime=0, y1Temp=200):
        """ 屏幕向上滑动
        frequency为滑动次数
        y1Temp为滑动像素，默认200"""
        time.sleep(sleepTime)
        action = TouchActions(driver)
        for i in range(0, frequency):
            # Action.scroll_from_element(elt, 0, -200).perform()
            # 从元素像下滑动200像素，以500的速度向下滑动
            action.flick_element(elt, 0, y1Temp, 600).perform()
            logger.debug("屏幕向上滑动")
            # time.sleep(0.5)
        time.sleep(1)


    def myWtH5FlickDown(self, driver, elt, frequency=1, sleepTime=0, y1Temp=-200):
        """ 屏幕向下滑动 """
        time.sleep(sleepTime)
        action = TouchActions(driver)
        for i in range(0, frequency):
            # Action.scroll_from_element(elt, 0, -200).perform()
            action.flick_element(elt, 0, y1Temp, 600).perform()
            logger.debug("屏幕向上滑动")
            # time.sleep(0.5)
        time.sleep(1)


    ###############################
    """手机"""
    ###############################

    def myWtGetWinSize(self, driver):
        """获得机器屏幕大小x,y"""
        NumberTimes = 1
        while 1 == 1:
            try:
                x = driver.get_window_size()['width']
                y = driver.get_window_size()['height']
                return (x, y)
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                NumberTimes = NumberTimes + 1


    def myWtPhoneTap(self, driver, lx, ly):
        """单击坐标，以1920*1080为标准，按实际的比例处理坐标"""
        # time.sleep(2)
        l = self.myWtGetWinSize(driver)
        x = int(int(l[0]) / 1080)
        y = int(int(l[1]) / 1920)
        driver.tap([(lx * x, ly * y)], )
        logger.debug('单击坐标：({},{})'.format(lx * x, ly * y))


    def myWtPhoneSwipeAuto(self, driver, element, sleepTime=0):
        """屏幕滑动，自动判断"""
        time.sleep(sleepTime)
        while 1 == 1:
            l = self.myWtGetWinSize(driver)
            location = element.location
            size = element.size
            y = int(location["y"])
            height = int(size["height"])
            yHeight = y + height
            if yHeight >= int(l[1]):
                driver.swipe(200, 400, 200, 200)
                logger.debug("屏幕滑动：({},{})到({},{})".format(200, 400, 200, 200))
            else:
                break


    def myWtPhoneSwipe(self, driver, x1, y1, x2, y2, frequency=1, sleepTime=0):
        """屏幕滑动
        按坐标x1, y1, x2, y2滑动
        frequency为次数"""
        time.sleep(sleepTime)
        l = self.myWtGetWinSize(driver)
        x1 = x1 * int(int(l[0]) / 1080)
        y1 = y1 * int(int(l[1]) / 1920)
        x2 = x2 * int(int(l[0]) / 1080)
        y2 = y2 * int(int(l[1]) / 1920)
        for i in range(0,frequency):
            driver.swipe(x1, y1, x1, y2)
            logger.debug("屏幕滑动：({},{})到({},{})".format(x1, y1, x2, y2))
            # time.sleep(0.5)
        time.sleep(1)


    def myWtPhoneSwipeUp(self, driver, frequency=1, sleepTime=0, y1Temp=0.75, y2Temp=0.25):
        """屏幕向上滑动"""
        time.sleep(sleepTime)
        l = self.myWtGetWinSize(driver)
        for i in range(0,frequency):
            x1 = int(l[0] * 0.5)  # x坐标
            y1 = int(l[1] * y1Temp)  # 起始y坐标
            y2 = int(l[1] * y2Temp)  # 终点y坐标
            driver.swipe(x1, y1, x1, y2)
            logger.debug("屏幕向上滑动")
            # time.sleep(0.5)
        time.sleep(1)


    def myWtPhoneSwipeDown(self, driver, frequency=1, sleepTime=0, y1Temp=0.25, y2Temp=0.75):
        """屏幕向下滑动"""
        time.sleep(sleepTime)
        l = self.myWtGetWinSize(driver)
        for i in range(0, frequency):
            x1=int(l[0]*0.5)
            y1=int(l[1]*y1Temp)
            y2=int(l[1]*y2Temp)
            driver.swipe(x1,y1,x1,y2)
            logger.debug("屏幕向下滑动")
            # time.sleep(0.5)
        time.sleep(1)


    def myWtPhoneSwipeLeft(self, driver, frequency=1, sleepTime=0, x1Temp=0.75, x2Temp=0.25):
        """屏幕向左滑动"""
        time.sleep(sleepTime)
        l = self.myWtGetWinSize(driver)
        for i in range(0, frequency):
            x1=int(l[0]*x1Temp)
            y1=int(l[1]*0.5)
            x2=int(l[0]*x2Temp)
            driver.swipe(x1,y1,x2,y1)
            logger.debug("屏幕向左滑动")
            # time.sleep(0.5)
        time.sleep(1)


    def myWtPhoneSwipeRight(self, driver, frequency=1, sleepTime=0, x1Temp=0.25, x2Temp=0.75):
        """屏幕向右滑动"""
        time.sleep(sleepTime)
        l = self.myWtGetWinSize(driver)
        for i in range(0, frequency):
            x1=int(l[0]*x1Temp)
            y1=int(l[1]*0.5)
            x2=int(l[0]*x2Temp)
            driver.swipe(x1,y1,x2,y1)
            logger.debug("屏幕向右滑动")
            # time.sleep(0.5)
        time.sleep(1)


    def myWtPhonePasteText(self, driver, elt, text, x=0, y=0):
        """手机，粘贴（通过剪切板）"""
        os.system("adb shell  am startservice ca.zgrs.clipper/.ClipboardService")  # 启动广播服务
        time.sleep(0.5)
        # os.system("adb shell am broadcast -a clipper.get")  # 取手机剪切板内容
        os.system("adb shell am broadcast -a clipper.set -e text {}".format(text))  # 设置手机剪切板
        time.sleep(0.5)
        self.myWtTouchActionLongpress(driver, elt)
        time.sleep(1)
        location = elt.location
        xBegin = int(location["x"])
        yBegin = int(location["y"])
        if x == 0:
            x = xBegin + 130
        if y == 0:
            y = yBegin + 225
        self.myWtPhoneTap(driver, x, y)
        time.sleep(1)
        logger.debug("粘贴文本({})成功".format(text))


    def myWtPhoneSetTypewriting(self):
        """切换输入法"""
        # os.system("adb shell ime list -s")  # 列出所有输入法
        # os.system("adb shell settings get secure default_input_method")  # 查看默认输入法
        # os.system("adb shell ime set com.sohu.inputmethod.sogou/.SogouIME")  # 切换搜狗输入法
        os.system("adb shell ime set com.baidu.input_mz/com.meizu.input.MzInputService")  # 切换百度输入法
        logger.debug("切换输入法")
        time.sleep(1)
