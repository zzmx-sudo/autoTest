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


class AppZhanQuZhuiZongPad(PublicOperation):
    """战区追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(AppZhanQuZhuiZongPad, self).__init__(methodName, AllPirParams)


    def appZhanQuZhuiZongPadOK(self, driver, paramsIn, checkPoint):
        """战区追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.appBottomMenu[0]
        menuStr2 = self.appShouYeMenu[1]
        self.appPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        date = self.mySysGetDate(day=-31)
        self.ipadPbSelectShowDate(driver, "", date)

        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '月累计')]")

        # 切换通州店、北苑路店
        tabList = self.myWtFindElements(driver, By.CLASS_NAME, "van-tab__text--ellipsis")
        for tab in tabList:
            self.myWtClick(tab)

            vantabactive = self.myWtFindElement(driver, By.CLASS_NAME, 'van-tab--active')
            vantabactiveTitle = vantabactive.text
            uiPathT = '{}-{}'.format(uiPath, vantabactiveTitle)
            summary = self.myWtFindElements(driver, By.CLASS_NAME, 'summary')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'小老板汇总', summary, tagList=['div'])

            uiPathT = '{}-{}'.format(uiPath, vantabactiveTitle)
            listContainer = self.myWtFindElements(driver, By.CLASS_NAME, 'listContainer')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'列表', listContainer, tagList=['listItem2', 'listItem3', 'listItem4', 'listItem5', 'listItem6'], tagType=By.CLASS_NAME)

            # 切换地图和列表
            svgList = self.myWtFindElements(driver, By.XPATH, "//*[name()='svg' and contains(@class,'svg-icon')]")
            for svg in svgList:
                use = self.myWtFindElement(svg, By.TAG_NAME, "use")
                href = use.get_attribute("xlink:href")
                logger.debug(href)
                # 地图
                if href == '#iconditu':
                    self.myWtClick(svg)
                    self.myWtFindElement(driver, By.XPATH, "//div[text()='子战区业绩']")

                    uiPathT = '{}-{}'.format(uiPath, vantabactiveTitle)
                    panel = self.myWtFindElements(driver, By.CLASS_NAME, 'panel')
                    self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'-地图', panel, tagList=['num'], tagType=By.CLASS_NAME)

                    # time.sleep(2)
                # 列表
                elif href == '#iconbiaoge':
                    self.myWtClick(svg)
                    self.myWtFindElement(driver, By.XPATH, "//div[text()='小老板']")
                    time.sleep(1)

            # 列表点击
            self.myWtFindElement(driver, By.CLASS_NAME, "listContainer")
            itemBoxList = self.myWtFindElements(driver, By.CLASS_NAME, "itemBox")
            for itemBox in itemBoxList:
                self.myWtClick(itemBox)

                self.appZhanQuZhuiZongPadXiaoLaoBan(driver, paramsIn, checkPoint, uiPathT)

                if self.tabClickNumOfTimes == 1:
                    break

        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '当日')]")

        self.ipadPbLeftBack(driver)


    def appZhanQuZhuiZongPadXiaoLaoBan(self, driver, paramsIn, checkPoint, uiPath):
        """小老板列表"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名

        uiPathT = '{}-小老板列表汇总'.format(uiPath)
        bottomItem = self.myWtFindElements(driver, By.CLASS_NAME, 'bottomItem')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, bottomItem, tagList=['value', 'topValue'], tagType=By.CLASS_NAME)

        uiPathT = '{}-小老板客户列表'.format(uiPath)
        bottom = self.myWtFindElements(driver, By.CLASS_NAME, 'bottom')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, bottom, tagList=['item'], tagType=By.CLASS_NAME)

        self.myWtClickEx(driver, By.XPATH, "//span[text()='产品']")

        uiPathT = '{}-小老板列表汇总'.format(uiPath)
        bottomItem = self.myWtFindElements(driver, By.CLASS_NAME, 'bottomItem')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, bottomItem, tagList=['value', 'topValue'], tagType=By.CLASS_NAME)

        uiPathT = '{}-小老板产品列表'.format(uiPath)
        bottom = self.myWtFindElements(driver, By.CLASS_NAME, 'bottom')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, bottom, tagList=['item'], tagType=By.CLASS_NAME)

        self.ipadPbLeftBack(driver)
