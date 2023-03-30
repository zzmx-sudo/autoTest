# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class Daping100DaoCai(PublicOperation):
    """大屏：100道菜"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(Daping100DaoCai, self).__init__(methodName, AllPirParams)


    def daping100DaoCaiOK(self, driver, paramsIn, checkPoint):
        """用例说明：100道菜"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        self.dapingPbFullScreen(driver)

        eltList = self.myWtFindElements(driver, By.CLASS_NAME, "carousel_con_wrap")
        t1 = self.mySysThreading(self.dapingPbActionMoveToElement, driver, eltList)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        reportwrapList = self.myWtFindElements(driver, By.NAME, "partReport")
        for reportwrapNum in range(len(reportwrapList)):
            reportwrap = reportwrapList[reportwrapNum]
            opentext = self.mySysStringCleanup(reportwrap.text).replace(' ', '')

            self.myWtJsScrollIntoView(driver, reportwrap)
            self.myWtClickEx(reportwrap, By.XPATH, './/./div')
            self.dapingPbRefreshWaiting(driver)

            body = self.myWtFindElements(driver, By.CLASS_NAME, "layer-content")
            uiPath = '大屏-{}-{}'.format(title, opentext)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(driver, actionbar='close-btn')

            if self.tabClickNumOfTimes == 1:
                break

        self.dapingPbActionMoveToElementStop(t1)
