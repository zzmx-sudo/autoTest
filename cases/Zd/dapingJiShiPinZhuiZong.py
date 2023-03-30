# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingJiShiPinZhuiZong(PublicOperation):
    """大屏：鸡食品追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingJiShiPinZhuiZong, self).__init__(methodName, AllPirParams)


    def dapingJiShiPinZhuiZongOK(self, driver, paramsIn, checkPoint):
        """用例说明：鸡食品追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        self.ipadPbSwitchToFrame(driver)

        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title.replace("鸡食品", "鸡食品跨区销售")))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['tab-vizHeader'], tagType=By.CLASS_NAME)

        # '串货销售汇总'和'公共区域主要城市分布'中的公司名
        tabvizHeaderWrapperList = self.myWtFindElements(driver, By.CLASS_NAME, 'tab-vizHeaderLabelContainer')
        for tabvizHeaderWrapperNum in range(len(tabvizHeaderWrapperList)):
            self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '价格比较')]")
            if tabvizHeaderWrapperNum == 1:
                continue
            # self.myWtClick(tabvizHeaderWrapperList[tabvizHeaderWrapperNum])
            tabvizHeaderWrapperList = self.myWtFindElements(driver, By.CLASS_NAME, 'tab-vizHeaderWrapper')
            self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, tabvizHeaderWrapperList, tabvizHeaderWrapperNum)

            self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '返回首页')]")

            tabvizHeaderWrapperTwoList = self.myWtFindElements(driver, By.CLASS_NAME, 'tab-vizHeaderWrapper')
            for tabvizHeaderWrapperTwoNum in range(len(tabvizHeaderWrapperTwoList)):
                # self.myWtClick(tabvizHeaderWrapperTwo)

                tabvizHeaderWrapperTwoList = self.myWtFindElements(driver, By.CLASS_NAME, 'tab-vizHeaderWrapper')
                self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, tabvizHeaderWrapperTwoList, tabvizHeaderWrapperTwoNum)

                if self.myWtEltNonexiContinue(driver, By.XPATH, "//div[contains(text(), '返回上页')]", maxWaittime=6) is None:
                    self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '返回首页')]")
                else:
                    self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '返回上页')]")
                time.sleep(1)

                break
                # if self.tabClickNumOfTimes == 1:
                #     break

            self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '返回首页')]")

            break
            # if self.tabClickNumOfTimes == 1:
            #     break

        # 价格比较>>
        self.myWtClickEx(driver, By.CLASS_NAME, 'tab-button-zone-text')
        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '返回首页')]")

        self.ipadPbSwitchToDefault(driver)
