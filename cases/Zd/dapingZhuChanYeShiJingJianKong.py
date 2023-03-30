# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingZhuChanYeShiJingJianKong(PublicOperation):
    """大屏：猪产业实景监控"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingZhuChanYeShiJingJianKong, self).__init__(methodName, AllPirParams)


    def dapingZhuChanYeShiJingJianKongOK(self, driver, paramsIn, checkPoint):
        """用例说明：猪产业实景监控"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 监控检查是否正常
        videoList = self.myWtFindElements(driver, By.TAG_NAME, "video")
        for video in reversed(videoList):
            self.dapingPbCheckJianKong(driver, video)

        # 弹窗
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, "jump-url")
        for jumpurl in jumpurlList:
            self.dapingPbRefreshWaiting(driver)
            self.myWtClick(jumpurl)

            self.dapingPbRefreshWaiting(driver)

            dlg = self.myWtFindElement(driver, By.CLASS_NAME, "content-dialog")
            dlgtext = str(dlg.text).split('\n')[0]

            # 监控检查是否正常
            videoList = self.myWtFindElements(dlg, By.TAG_NAME, "video")
            for video in videoList:
                self.dapingPbCheckJianKong(driver, video)

            body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
            uiPath = '[大屏]-[{}]-[{}]'.format(title, dlgtext)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(driver)
