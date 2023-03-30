# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingQuanQiuMaiQuanQiuMai(PublicOperation):
    """大屏：全球买全球卖战略追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingQuanQiuMaiQuanQiuMai, self).__init__(methodName, AllPirParams)


    def dapingQuanQiuMaiQuanQiuMaiOK(self, driver, paramsIn, checkPoint):
        """用例说明：全球买全球卖战略追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        tabsitemList = self.myWtFindElements(driver, By.XPATH, "//span[contains(text(), '跨境组') and contains(@class,'tabs_item')]")
        for tabsitem in tabsitemList:
            self.myWtClick(tabsitem)

            tabsitemTwList = self.myWtFindElements(driver, By.XPATH, "//span[contains(text(), '口产品业绩') and contains(@class,'tabs_item')]")
            for tabsitemTw in tabsitemTwList:
                self.myWtClick(tabsitemTw)

                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}'.format(title)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                if self.tabClickNumOfTimes == 1:
                    break
