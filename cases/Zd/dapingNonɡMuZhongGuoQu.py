# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal



logger = basic.myGlobal.getLogger()


class DapingNongMuZhongGuoQu(PublicOperation):
    """大屏：农牧中国区"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingNongMuZhongGuoQu, self).__init__(methodName, AllPirParams)


    def dapingNongMuZhongGuoQuOK(self, driver, paramsIn, checkPoint):
        """用例说明：农牧中国区"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        titleElt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title), maxWaittime=50)
        self.dapingPbRefreshWaiting(driver)

        eltList = self.myWtFindElements(driver, By.CLASS_NAME, "carousel_wrap_ver")
        eltList.append(titleElt)
        t1 = self.mySysThreading(self.dapingPbActionMoveToElement, driver, eltList)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 事业板块
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, "jump-url")
        for jumpurl in range(0, len(jumpurlList)):
            if jumpurl == 0:
                continue
            if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'close', maxWaittime=0) is not None:
                self.dapingPbCloseDialog(driver)

            self.myWtClick(jumpurlList[jumpurl])

            handles = self.myWtWndowhandlesOpen(driver, 3, newhandleNum=2)
            self.dapingPbRefreshWaiting(driver)
            self.myWtWndowhandlesClose(driver, handles, 1)

            if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'close', maxWaittime=0) is not None:
                self.dapingPbCloseDialog(driver)

        # 大区列表
        carouselitemList = self.myWtFindElements(driver, By.CLASS_NAME, "carousel_item")
        for carouselitem in range(0, len(carouselitemList)):
            self.myWtClick(carouselitemList[carouselitem])

            self.dapingPbRefreshWaiting(driver)

            # 区
            titlecurrent = self.myWtFindElement(driver, By.CLASS_NAME, "title-current").text
            body = self.myWtFindElements(driver, By.TAG_NAME, "open")
            uiPath = '大屏-{}-{}'.format(title, titlecurrent)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            # 饲料、其它
            itembgList = self.myWtFindElements(driver, By.CLASS_NAME, "item-bg")
            for itembg in itembgList:
                if "left-title" not in itembg.get_attribute("class"):
                    self.myWtClick(itembg)

            # 中国区
            if carouselitem == 0:
                self.myWtClickEx(driver, By.XPATH, "//div[text()='中国区']")

                self.dapingPbRefreshWaiting(driver)

                body = self.myWtFindElements(driver, By.TAG_NAME, "open")
                uiPath = '大屏-{}-中国区'.format(title)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                itembgList = self.myWtFindElements(driver, By.CLASS_NAME, "item-bg")
                for itembg in itembgList:
                    if "left-title" not in itembg.get_attribute("class"):
                        self.myWtClick(itembg)

            self.dapingPbCloseDialog(driver)

            if self.tabClickNumOfTimes == 1:
                break

        self.dapingPbActionMoveToElementStop(t1)
