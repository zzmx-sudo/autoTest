# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingXianDaiShiPin(PublicOperation):
    """大屏：现代食品"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingXianDaiShiPin, self).__init__(methodName, AllPirParams)


    def dapingXianDaiShiPinOK(self, driver, paramsIn, checkPoint):
        """用例说明：现代食品"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 净利润后5名和前5名弹窗
        slotlistcontaier = self.myWtFindElement(driver, By.CLASS_NAME, "slot-list-contaier")
        clearfixList = self.myWtFindElements(slotlistcontaier, By.CLASS_NAME, "clearfix")
        for clearfix in clearfixList:
            self.myWtClickEx(clearfix, By.XPATH, './/./div')
            self.dapingPbCloseDialog(driver, True)

            if self.tabClickNumOfTimes == 1:
                break

        self.dapingXianDaiShiPinMapDispose(driver, paramsIn, checkPoint)


    def dapingXianDaiShiPinMapDispose(self, driver, paramsIn, checkPoint):
        """移动到地图所有点击显示浮窗"""
        title = paramsIn['daPingTitleExpect']

        mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-chinaMap")
        x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

        pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [4, 219, 95], 5, 40)  # 盈利达标
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [206, 197, 42], 3, 40)  # 盈利未达标
        pixlist.extend(tmppixlist)
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [205, 81, 71], 5, 40)  # 亏损
        pixlist.extend(tmppixlist)

        if len(pixlist) != 0:
            for pix in pixlist:
                xx = pix[0]
                yy = pix[1]
                # 排除
                if self.browserHeadless == 'UI':
                    if (xx < 282 * self.screenScaling and yy > 328 * self.screenScaling) or (xx > 594 * self.screenScaling and yy > 318 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (xx < 282 and yy > 328) or (xx > 594 and yy > 318):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionElementclickByXY(driver, mapboxglcanvas, xx+3, yy+3)

                self.dapingPbRefreshWaiting(driver)

                self.dapingPbCloseDialog(driver, True)

                if self.tabClickNumOfTimes == 1:
                    break
