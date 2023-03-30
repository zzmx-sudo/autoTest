# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
from selenium.webdriver.common.action_chains import ActionChains
import re


logger = basic.myGlobal.getLogger()
fileName = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0]


class DapingZhuChanYeLian(PublicOperation):
    """大屏：猪产业链"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingZhuChanYeLian, self).__init__(methodName, AllPirParams)


    def dapingZhuChanYeLianOK(self, driver, paramsIn, checkPoint):
        """用例说明：猪产业链"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        refFileName = fileName + '-ref.png'
        element = self.myWtFindElement(driver, By.XPATH, "//div[contains(@style, 'a87ae2e20b10430e9056aec2903d911a.PNG')]")
        self.myPbRefreshWaiting(driver, element, refFileName, 4000)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 养殖产能、饲料客户规模场
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, 'jump-url')
        for jumpurl in jumpurlList:
            self.myWtClick(jumpurl)
            self.dapingPbRefreshWaiting(driver)
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '饲料空间（吨）')]")

            self.dapingPbRefreshWaiting(driver)

            body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
            uiPath = '大屏-{}-养殖产能'.format(title)
            # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, excludeTextList=['-未带料'], tagList=['inner-content'], tagType=By.CLASS_NAME)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(driver)

            self.myWtGetJsLog(driver, self.jsLogExclude)

            if self.dateClickNumOfTimes == 1:
                break

        # 白条、畅销品、低价品、低周转品、副产品、熟调
        self.dapingPbRefreshWaiting(driver)
        pareaList = self.myWtFindElements(driver, By.CLASS_NAME, 'parea')
        for parea in pareaList:
            self.myWtClick(parea)
            self.dapingPbRefreshWaiting(driver)
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '圆形大小：销量（吨）')]")
            # innercontent = self.myWtFindElement(driver, By.CLASS_NAME, 'inner-content')

            body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
            uiPath = '大屏-{}-白条'.format(title)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(driver)

            self.myWtGetJsLog(driver, self.jsLogExclude)

            if self.dateClickNumOfTimes == 1:
                break

        # 白条、段类、肋排
        self.dapingPbRefreshWaiting(driver)
        careaitemList = self.myWtFindElements(driver, By.CLASS_NAME, 'carea-item')
        for careaitem in careaitemList:
            self.myWtClick(careaitem)
            self.dapingPbRefreshWaiting(driver)
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '分城市利润bottom 10 排名')]")

            body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
            uiPath = '大屏-{}-段类'.format(title)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(driver)

            self.myWtGetJsLog(driver, self.jsLogExclude)

            if self.dateClickNumOfTimes == 1:
                break






