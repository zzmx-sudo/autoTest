# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingZhuWangZhanLue(PublicOperation):
    """大屏：猪王战略"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingZhuWangZhanLue, self).__init__(methodName, AllPirParams)


    def dapingZhuWangZhanLueOK(self, driver, paramsIn, checkPoint):
        """用例说明：猪王战略"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        clientWidthPro = self.clientWidthProportion
        titleElt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        eltList = self.myWtFindElements(driver, By.CLASS_NAME, "carousel_wrap_ver")
        eltList.append(titleElt)
        t1 = self.mySysThreading(self.dapingPbActionMoveToElement, driver, eltList)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.myWtGetJsLog(driver, self.jsLogExclude)
        partReportList = self.myWtFindElements(driver, By.NAME, "partReport")
        for partReport in partReportList:
            x = int(float(partReport.location['x']) / clientWidthPro)
            y = int(float(partReport.location['y']) / clientWidthPro)
            text = self.mySysStringCleanup(str(partReport.get_attribute("textContent")))[0:4].replace(' ', '')
            logger.debug("{} {} {}".format(x, y, text))
            if x >= 900/clientWidthPro:  # if x == 900 / clientWidthPro or x == 1350 / clientWidthPro:
                if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "close", 0, 0) is not None:
                    self.dapingPbCloseDialog(driver)

                self.myWtClickEx(partReport, By.XPATH, ".//..")

                self.dapingPbRefreshWaiting(driver)

                self.myWtFindElement(driver, By.CLASS_NAME, "close")

                self.dapingPbRefreshWaiting(driver)

                body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
                uiPath = '大屏-{}-{}'.format(title, text)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                self.myWtGetJsLog(driver, self.jsLogExclude)

                self.dapingPbCloseDialog(driver)

                if self.tabClickNumOfTimes == 1:
                    break

        self.dapingPbActionMoveToElementStop(t1)

