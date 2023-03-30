# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingShuiChanShiYe(PublicOperation):
    """大屏：水产事业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingShuiChanShiYe, self).__init__(methodName, AllPirParams)


    def dapingShuiChanShiYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：水产事业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, "jump-url")
        for jumpurl in jumpurlList:
            self.dapingPbRefreshWaiting(driver)
            self.myWtClick(jumpurl)

            self.dapingPbRefreshWaiting(driver)

            self.dapingPbCloseDialog(driver, True)

        self.dapingShuiChanShiYeMapDispose(driver, paramsIn, checkPoint)


    def dapingShuiChanShiYeMapDispose(self, driver, paramsIn, checkPoint):
        """移动到地图所有点击显示浮窗"""
        title = paramsIn['daPingTitleExpect']

        mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-areaPointMap")
        x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

        pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [3, 249, 72], 2, 40)  # 盈利达标
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [255, 219, 0], 2, 40)  # 盈利未达标
        pixlist.extend(tmppixlist)
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [255, 78, 43], 2, 40)  # 亏损
        pixlist.extend(tmppixlist)

        if len(pixlist) != 0:
            for pix in pixlist:
                xx = pix[0]
                yy = pix[1]
                # 排除
                if self.browserHeadless == 'UI':
                    if (yy > 456 * self.screenScaling) or (xx < 76 * self.screenScaling and yy > 384 * self.screenScaling) or (xx > 307 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (yy > 456) or (xx < 76 and yy > 384) or (xx > 307):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionElementclickByXY(driver, mapboxglcanvas, xx+3, yy+3)

                self.myWtFindElement(driver, By.CLASS_NAME, "open")

                if self.tabClickNumOfTimes == 1:
                    break