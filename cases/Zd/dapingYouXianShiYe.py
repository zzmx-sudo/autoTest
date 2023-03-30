# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingYouXianShiYe(PublicOperation):
    """大屏：优鲜事业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingYouXianShiYe, self).__init__(methodName, AllPirParams)


    def dapingYouXianShiYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：优鲜事业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        zdchinaMap = self.myWtFindElement(driver, By.CLASS_NAME, "zd-chinaMap")
        x, y, width, height = self.myPbGetElementSize(zdchinaMap)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

        pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [2, 215, 90], 10, 15)
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [204, 78, 66], 10, 15)
        pixlist.extend(tmppixlist)

        if len(pixlist) != 0:
            for pix in pixlist:
                xx = pix[0]
                yy = pix[1]
                # 排除
                if self.browserHeadless == 'UI':
                    if xx < 25:
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue
                else:
                    if xx < 25 * self.screenScaling:
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue

                self.myWtActionElementclickByXY(driver, zdchinaMap, xx + 2, yy + 2)

                self.dapingPbRefreshWaiting(driver)

                if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "zd-dialog") is not None:
                    cityname = self.myWtFindElement(driver, By.CLASS_NAME, "bm-city-name").text
                    body = self.myWtFindElements(driver, By.CLASS_NAME, "zd-dialog")
                    uiPath = '大屏-{}-{}'.format(title, cityname)
                    self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content', 'profit-numer', 'column-content'], tagType=By.CLASS_NAME)

                    self.dapingPbCloseDialog(driver)
                    time.sleep(1)

                    if self.tabClickNumOfTimes == 1:
                        break
