# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
import re

logger = basic.myGlobal.getLogger()
# mybatisFile = os.path.basename(sys.argv[0]).replace('.py', '') + '.xml'
mybatisFile = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0] + '.xml'


class IpadLiuLian(PublicOperation):
    """榴莲"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadLiuLian, self).__init__(methodName, AllPirParams)


    def ipadLiuLianOK(self, driver, paramsIn, checkPoint):
        """榴莲"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[6]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)

        self.ipadLiuLianDetail(driver, paramsIn, checkPoint)


    def ipadLiuLianDetail(self, driver, paramsIn, checkPoint):
        """榴莲处理"""
        uiPath = ''

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        # 年度销售计划
        self.myWtClickEx(driver, By.CLASS_NAME, 'year')
        self.ipadLiuLianXiaoShouJiHua(driver, paramsIn, checkPoint, uiPath)

        date = self.mySysGetDate(day=-31)
        self.ipadPbSelectShowDate(driver, "", date)

        # 切换地图
        switch = self.myWtFindElement(driver, By.CLASS_NAME, "switch")
        liList = self.myWtFindElements(switch, By.TAG_NAME, "li")
        for li in liList:
            self.myWtClick(li)
            time.sleep(1)

        # 点击泰国发出>查看货柜列表
        cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
        self.myWtClickEx(cabinetsNumber, By.CLASS_NAME, 'image_right')
        self.ipadLiuLianHuoGui(driver, paramsIn, checkPoint, uiPath)

        cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
        self.myWtH5FlickDown(driver, cabinetsNumber)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        # 莲花
        self.myWtClickEx(driver, By.XPATH, "//span[contains(text(), '莲花')]/following-sibling::img")
        self.ipadLiuLianLianHua(driver, paramsIn, checkPoint, uiPath)
        # 优鲜
        self.myWtClickEx(driver, By.XPATH, "//span[contains(text(), '优鲜')]/following-sibling::img")
        self.ipadLiuLianYouXian(driver, paramsIn, checkPoint, uiPath)

        elt = self.myWtFindElement(driver, By.XPATH, "//li[contains(text(), 'B2C')]")
        self.myWtH5FlickDown(driver, elt)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        # 中国区SVC
        arrowList = self.myWtFindElements(driver, By.CLASS_NAME, 'arrow')
        for arrow in arrowList:
            self.myWtClick(arrow)

            self.ipadLiuLianSVC(driver, paramsIn, checkPoint, uiPath)

            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadLiuLianHuoGui(self, driver, paramsIn, checkPoint, uiPath):
        """货柜列表"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.ipadPbClickCNYexTHB(driver)

        # 货柜状态
        statusitemList = self.myWtFindElements(driver, By.CLASS_NAME, 'status-item')
        for statusitem in statusitemList:
            self.myWtClick(statusitem)
            typeText = statusitem.text
            if "已销" in typeText or "在销" in typeText:
                logger.debug(typeText)
                # 货柜明细
                stablerowList = self.myWtFindElements(driver, By.CLASS_NAME, 'table_row')
                for stablerow in stablerowList:
                    tablecellList = self.myWtFindElements(stablerow, By.CLASS_NAME, "table_cell")
                    for tablecell in tablecellList:
                        spanList = self.myWtFindElements(tablecell, By.TAG_NAME, "span")
                        for span in reversed(spanList):
                            guiNum = span.text
                            self.myWtClick(span)
                            self.ipadLiuLianHuoGuiDetail(driver, paramsIn, checkPoint, uiPath)
                            break

                    if self.tabClickNumOfTimes == 1:
                        break

        self.ipadPbLeftBack(driver)


    def ipadLiuLianHuoGuiDetail(self, driver, paramsIn, checkPoint, uiPath):
        """货柜明细"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.ipadPbClickCNYexTHB(driver)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianXiaoShouJiHua(self, driver, paramsIn, checkPoint, uiPath):
        """榴莲销售计划"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        # 榴莲销售计划按月
        self.myWtClickEx(driver, By.CLASS_NAME, 'image_right')
        self.ipadLiuLianXiaoShouJiHuaMonth(driver, paramsIn, checkPoint, uiPath)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianXiaoShouJiHuaMonth(self, driver, paramsIn, checkPoint, uiPath):
        """榴莲销售计划按月"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianSVC(self, driver, paramsIn, checkPoint, uiPath):
        """SVC"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.myWtFindElement(driver, By.XPATH, "//div[text()='单位: 万']")

        self.ipadPbClickCNYexTHB(driver)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianLianHua(self, driver, paramsIn, checkPoint, uiPath):
        """莲花"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")

        self.ipadPbClickCNYexTHB(driver)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianYouXian(self, driver, paramsIn, checkPoint, uiPath):
        """优鲜"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadLiuLianWebPageTitle(driver, paramsIn, checkPoint)

        self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")

        self.ipadPbClickCNYexTHB(driver)

        self.ipadPbLeftBack(driver)


    def ipadLiuLianWebPageTitle(self, driver, paramsIn, checkPoint):
        """获取和打印网页标题"""
        header = self.mySysStringCleanup(self.myWtFindElement(driver, By.CLASS_NAME, 'header').text)
        logger.debug('当前界面：{}'.format(header))


