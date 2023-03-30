# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingYuShiFenXi(PublicOperation):
    """大屏：预实分析"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingYuShiFenXi, self).__init__(methodName, AllPirParams)


    def dapingYuShiFenXiOK(self, driver, paramsIn, checkPoint):
        """用例说明：预实分析"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        # self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '中国区')]")
        self.dapingPbRefreshWaiting(driver)

        partReportList = self.myWtFindElements(driver, By.NAME, "partReport")
        for partReportNum in range(len(partReportList)):
            if partReportNum > 15:
                continue
            partReport = partReportList[partReportNum]
            x, y, width, height = self.myPbGetElementSize(partReport, True)
            logger.debug(x)
            if x < 200:
                reptext = self.mySysStringCleanup(partReport.text).replace(' ', '')[0:5]
                self.myWtClick(partReport)

                self.dapingPbRefreshWaiting(driver)

                # 选择月
                self.myWtClickEx(driver, By.CLASS_NAME, 'selectedbox')
                self.myWtClickEx(driver, By.XPATH, "//*[contains(text(), '本月')]")
                self.dapingPbRefreshWaiting(driver)

                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}-{}-月'.format(title, reptext)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                # 选择年
                self.myWtClickEx(driver, By.CLASS_NAME, 'selectedbox')
                self.myWtClickEx(driver, By.XPATH, "//*[contains(text(), '本年')]")
                self.dapingPbRefreshWaiting(driver)

                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}-{}-月'.format(title, reptext)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                # partReportTwList = self.myWtFindElements(driver, By.NAME, "partReport")
                # for partReportTwNum in range(len(partReportTwList)):
                #     if partReportTwNum < 17:
                #         continue

                self.myWtClickEx(driver, By.CLASS_NAME, 'tabs')  # 退出事业板块

                if self.tabClickNumOfTimes == 1:
                    break
