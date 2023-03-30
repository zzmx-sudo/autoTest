# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
from selenium.webdriver.common.action_chains import ActionChains


logger = basic.myGlobal.getLogger()


class DapingQinShiYe(PublicOperation):
    """大屏：禽事业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingQinShiYe, self).__init__(methodName, AllPirParams)


    def dapingQinShiYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：禽事业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        # self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '青岛') and contains(@class,'title')]")
        self.dapingPbRefreshWaiting(driver)

        self.myWtClickEx(driver, By.CLASS_NAME, 'dropdown_Menu')
        self.myWtFindElement(driver, By.CLASS_NAME, 'drop-box')
        self.dapingQinShiYeDataSelect(driver, paramsIn, checkPoint, 'content', driver)

        # 监控检查是否正常
        videoList = self.myWtFindElements(driver, By.TAG_NAME, "video")
        for video in reversed(videoList):
            self.dapingPbCheckJianKong(driver, video)


    def dapingQinShiYeDataSelect(self, driver, paramsIn, checkPoint, content, elt):
        """选择所有列表中的日期"""
        title = paramsIn['daPingTitleExpect']
        contentC = self.myWtFindElement(elt, By.CLASS_NAME, content)
        dropbox = self.myWtFindElement(contentC, By.XPATH, ".//./div[contains(@class,'drop-box')]")
        dropitemList = self.myWtFindElements(dropbox, By.CLASS_NAME, 'drop-item')
        for menuNum in range(len(dropitemList)):
            contentClk = self.myWtFindElement(elt, By.CLASS_NAME, content)
            dropboxClk = self.myWtFindElement(contentClk, By.XPATH, ".//./div[contains(@class,'drop-box')]")
            dropitemClkList = self.myWtFindElements(dropboxClk, By.CLASS_NAME, 'drop-item')
            clk, localdropitem = self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, dropitemClkList, menuNum, scrollIntoView=None)

            if self.myWtEltNonexiContinue(localdropitem, By.XPATH, ".//*[name()='svg' and contains(@class,'iconfont')]") is not None:
                self.dapingQinShiYeDataSelect(driver, paramsIn, checkPoint, 'drop-children', contentClk)
            else:
                time.sleep(1)

                self.dapingPbRefreshWaiting(driver)

                datatext = str(self.myWtFindElement(driver, By.CLASS_NAME, 'dropdown_Menu').text).replace(" ", "")
                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}-{}'.format(title, datatext)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                self.myWtClickEx(driver, By.CLASS_NAME, 'dropdown_Menu')

                if self.tabClickNumOfTimes == 1:
                    break
