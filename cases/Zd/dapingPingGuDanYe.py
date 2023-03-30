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


class DapingPingGuDanYe(PublicOperation):
    """大屏：平谷蛋业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingPingGuDanYe, self).__init__(methodName, AllPirParams)


    def dapingPingGuDanYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：平谷蛋业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title), maxWaittime=30)
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        jumpurlDict = {}
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, 'jump-url')
        for jumpurl in jumpurlList:
            height = jumpurl.size['height']
            width = jumpurl.size['width']
            # 判断控件大小
            if height != 100 and width != 100:
                key = "{},{}".format(height, width)
                # 累计每种大小的控件点击次数
                if key in jumpurlDict:
                    jumpurlDict[key] = jumpurlDict[key] + 1
                else:
                    jumpurlDict[key] = 1

                if self.tabClickNumOfTimes == 1:
                    # 某种控件点击次数大于等于2则不再点击
                    if jumpurlDict[key] >= 2:
                        continue

                logger.debug(jumpurlDict)
                logger.debug(jumpurl.size)
                self.myWtClick(jumpurl)

                self.dapingPbRefreshWaiting(driver)

                contentdialog = self.myWtFindElement(driver, By.CLASS_NAME, 'content-dialog')
                if self.myWtEltNonexiContinue(contentdialog, By.TAG_NAME, 'canvas') is not None:
                    self.myWtFindElement(contentdialog, By.TAG_NAME, 'canvas')

                body = self.myWtFindElements(driver, By.CLASS_NAME, "content-dialog")
                uiPath = '大屏-{}-弹窗'.format(title)
                # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, excludeTextList=['图例', '沃尔玛', '正大优鲜', '有限公司', '有限责任公司', 'COMPANY'], tagList=['inner-content'], tagType=By.CLASS_NAME)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                diajumpurlList = self.myWtFindElements(contentdialog, By.CLASS_NAME, 'jump-url')
                for diajumpurl in diajumpurlList:
                    diaheight = diajumpurl.size['height']
                    diawidth = diajumpurl.size['width']
                    key = "{},{}".format(diaheight, diawidth)
                    # 累计每种大小的控件点击次数
                    if key in jumpurlDict:
                        jumpurlDict[key] = jumpurlDict[key] + 1
                    else:
                        jumpurlDict[key] = 1

                    if self.tabClickNumOfTimes == 1:
                        # 某种控件点击次数大于等于2则不再点击
                        if jumpurlDict[key] >= 2:
                            continue

                    logger.debug(jumpurlDict)
                    logger.debug(diajumpurl.size)
                    self.myWtClick(diajumpurl)

                    self.dapingPbRefreshWaiting(driver)
                    if self.myWtEltNonexiContinue(contentdialog, By.CLASS_NAME, 'content-dialog') is not None:
                        # 业务分析员
                        contentdialog2 = self.myWtFindElement(contentdialog, By.CLASS_NAME, 'content-dialog')

                        body = self.myWtFindElements(contentdialog, By.CLASS_NAME, "content-dialog")
                        uiPath = '大屏-{}-弹窗-业务分析员'.format(title)
                        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                        self.myWtGetJsLog(driver, self.jsLogExclude)

                        # 关闭窗口
                        self.dapingPbCloseDialog(contentdialog2)
                    elif self.myWtEltNonexiContinue(contentdialog, By.TAG_NAME, 'iframe') is not None:
                        # 销售城市
                        self.ipadPbSwitchToFrame(driver)

                        self.myWtFindElement(driver, By.CLASS_NAME, 'ff-IFrameSizedToWindow')

                        body = self.myWtFindElements(driver, By.CLASS_NAME, "ff-IFrameSizedToWindow")
                        uiPath = '大屏-{}-弹窗-销售城市'.format(title)
                        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                        self.ipadPbSwitchToDefault(driver)

                        self.myWtGetJsLog(driver, self.jsLogExclude)

                        self.dapingPbCloseDialog(driver, True)

                self.dapingPbCloseDialog(driver)



