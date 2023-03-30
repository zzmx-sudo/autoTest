# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingCTIZhuZhuiZong(PublicOperation):
    """大屏：CTI猪追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingCTIZhuZhuiZong, self).__init__(methodName, AllPirParams)


    def dapingCTIZhuZhuiZongOK(self, driver, paramsIn, checkPoint):
        """用例说明：CTI猪追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title.replace("CTI", "CTI ")))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 右边点击下拉框选择‘猪屠宰’
        selectedbox = self.myWtFindElement(driver, By.CLASS_NAME, 'select_wrap')
        self.myWtClick(selectedbox)
        self.myWtClickEx(selectedbox, By.XPATH, ".//*[contains(text(), '猪屠宰')]")

        # 切换省区
        tabsitemList = self.myWtFindElements(driver, By.CLASS_NAME, "tabs_item")
        for tabsitem in tabsitemList:
            self.myWtClick(tabsitem)

        body = self.myWtFindElements(driver, By.CLASS_NAME, "map_analyze_yufeicarousel")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.myWtClickEx(driver, By.CLASS_NAME, 'head')
        self.myWtFindElement(driver, By.CLASS_NAME, 'drop-box')
        self.dapingCTIZhuZhuiZongDataSelect(driver, paramsIn, checkPoint, 'content', driver)


    def dapingCTIZhuZhuiZongDataSelect(self, driver, paramsIn, checkPoint, content, elt):
        """选择所有列表中的日期"""
        title = paramsIn['daPingTitleExpect']
        contentC = self.myWtFindElement(elt, By.CLASS_NAME, content)
        dropbox = self.myWtFindElement(contentC, By.XPATH, ".//./div[contains(@class,'drop-box')]")
        dropitemList = self.myWtFindElements(dropbox, By.CLASS_NAME, 'drop-item')
        for menuNum in range(len(dropitemList)):
            contentClk = self.myWtFindElement(elt, By.CLASS_NAME, content)
            dropboxClk = self.myWtFindElement(contentClk, By.XPATH, ".//./div[contains(@class,'drop-box')]")
            dropitemClkList = self.myWtFindElements(dropboxClk, By.CLASS_NAME, 'drop-item')
            clk, localdropitem = self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, dropitemClkList, menuNum)

            if self.myWtEltNonexiContinue(localdropitem, By.XPATH, ".//*[name()='svg' and contains(@class,'iconfont')]") is not None:
                self.dapingCTIZhuZhuiZongDataSelect(driver, paramsIn, checkPoint, 'drop-children', contentClk)
            else:
                time.sleep(1)

                self.dapingPbRefreshWaiting(driver)

                datatext = str(self.myWtFindElement(driver, By.CLASS_NAME, 'head').text).replace(" ", "")
                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}-{}'.format(title, datatext)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                self.myWtClickEx(driver, By.CLASS_NAME, 'head')

                if self.tabClickNumOfTimes == 1:
                    break
