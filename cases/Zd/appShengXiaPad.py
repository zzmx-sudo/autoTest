# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
import re
from cases.Zd.ipadShengXia import IpadShengXia

logger = basic.myGlobal.getLogger()
# mybatisFile = os.path.basename(sys.argv[0]).replace('.py', '') + '.xml'
mybatisFile = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0] + '.xml'


class AppShengXiaPad(IpadShengXia):
    """生虾"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(AppShengXiaPad, self).__init__(methodName, AllPirParams)


    def appShengXiaPadOK(self, driver, paramsIn, checkPoint):
        """生虾"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.appBottomMenu[0]
        menuStr2 = self.appShouYeMenu[5]
        self.appPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        # self.appShengXiaDetail(driver, paramsIn, checkPoint)
        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    def appHunTunPadOK(self, driver, paramsIn, checkPoint):
        """馄饨"""
        menuStr1 = self.appBottomMenu[0]
        menuStr2 = self.appShouYeMenu[7]
        self.appPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        # self.appShengXiaDetail(driver, paramsIn, checkPoint)
        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    def appNiuRouPadOK(self, driver, paramsIn, checkPoint):
        """牛肉"""
        menuStr1 = self.appBottomMenu[0]
        menuStr2 = self.appShouYeMenu[6]
        self.appPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        # self.appShengXiaDetail(driver, paramsIn, checkPoint)
        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    # def appShengXiaDetail(self, driver, paramsIn, checkPoint):
    #     """生虾处理"""
    #     uiPath = ''
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     # 点击“全链”
    #     cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
    #     spanList = self.myWtFindElements(cabinetsNumber, By.TAG_NAME, 'span')
    #     for span in reversed(spanList):
    #         self.myWtClick(span)
    #         self.appShengXiaQuanLian(driver, paramsIn, checkPoint, uiPath)
    #         break
    #
    #     cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
    #     self.myWtH5FlickDown(driver, cabinetsNumber)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     # 莲花、优鲜
    #     jumpList = self.myWtFindElements(driver, By.CLASS_NAME, 'jump')
    #     for jump in jumpList:
    #         text = self.myWtFindElement(jump, By.XPATH, './/..').text
    #         self.myWtClick(jump)
    #         time.sleep(3)
    #         if '莲花' in text:
    #             self.appShengXiaLianHua(driver, paramsIn, checkPoint, uiPath)
    #         else:
    #             self.appShengXiaYouXian(driver, paramsIn, checkPoint, uiPath)
    #
    #     elt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '优鲜')]")
    #     self.myWtH5FlickDown(driver, elt)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     # 中国区SVC
    #     hearderImgList = self.myWtFindElements(driver, By.CLASS_NAME, 'hearderImg')
    #     for hearderImg in hearderImgList:
    #         self.myWtClick(hearderImg)
    #
    #         self.appShengXiaSVC(driver, paramsIn, checkPoint, uiPath)
    #
    #         if self.tabClickNumOfTimes == 1:
    #             break
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaQuanLian(self, driver, paramsIn, checkPoint, uiPath):
    #     """全链"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     # 曹VC自销、统一分配
    #     imagerightList = self.myWtFindElements(driver, By.CLASS_NAME, 'image_right')
    #     for imageright in imagerightList:
    #         name = self.myWtFindElement(imageright, By.XPATH, './/../..').text
    #         self.myWtClick(imageright)
    #         if '曹VC自销' in name:
    #             self.appShengXiaCaoVCZhixiao(driver, paramsIn, checkPoint, uiPath)
    #         else:
    #             self.appShengXiaTongYifenPei(driver, paramsIn, checkPoint, uiPath)
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaCaoVCZhixiao(self, driver, paramsIn, checkPoint, uiPath):
    #     """曹VC自销"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaTongYifenPei(self, driver, paramsIn, checkPoint, uiPath):
    #     """统一分配"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     # 单击SVC
    #     hrowList = self.myWtFindElements(driver, By.CLASS_NAME, 'hrow')
    #     for hrow in hrowList:
    #         self.myWtClick(hrow)
    #
    #         self.appShengXiaSVC(driver, paramsIn, checkPoint, uiPath)
    #
    #         if self.tabClickNumOfTimes == 1:
    #             break
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaSVC(self, driver, paramsIn, checkPoint, uiPath):
    #     """SVC"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     self.myWtFindElement(driver, By.XPATH, "//div[text()='单位: 万']")
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaLianHua(self, driver, paramsIn, checkPoint, uiPath):
    #     """莲花"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaYouXian(self, driver, paramsIn, checkPoint, uiPath):
    #     """优鲜"""
    #     self.appPbRefreshWaiting(driver)
    #
    #     self.appShengXiaWebPageTitle(driver, paramsIn, checkPoint)
    #
    #     self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")
    #
    #     self.appPbLeftBack(driver)
    #
    #
    # def appShengXiaWebPageTitle(self, driver, paramsIn, checkPoint):
    #     """获取和打印网页标题"""
    #     header = self.myWtFindElement(driver, By.CLASS_NAME, 'header').text
    #     logger.debug('当前界面：{}'.format(header))
