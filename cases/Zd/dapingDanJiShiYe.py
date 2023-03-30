# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingDanJiShiYe(PublicOperation):
    """大屏：蛋鸡事业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingDanJiShiYe, self).__init__(methodName, AllPirParams)


    def dapingDanJiShiYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：蛋鸡事业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 分公司利润
        slotlistcontaier = self.myWtFindElement(driver, By.CLASS_NAME, "slot-list-contaier")
        clearfixList = self.myWtFindElements(slotlistcontaier, By.CLASS_NAME, "clearfix")
        for clearfix in clearfixList:
            if "header" not in clearfix.get_attribute("class"):
                self.myWtClick(clearfix)
                self.dapingPbRefreshWaiting(driver)
                self.dapingPbCloseDialog(driver, True)

        # 亏损预警
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, "jump-url")
        for jumpurl in jumpurlList:
            self.myWtClick(jumpurl)
            self.dapingPbRefreshWaiting(driver)
            self.dapingPbCloseDialog(driver, True)

        self.dapingDanJiShiYeMapDispose(driver, paramsIn, checkPoint)


    def dapingDanJiShiYeMapDispose(self, driver, paramsIn, checkPoint):
        """移动到地图所有点击显示浮窗"""
        title = paramsIn['daPingTitleExpect']

        mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-largerMap")
        x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

        pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [4, 219, 95], 5, 40)  # 盈利达标
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [206, 191, 31], 2, 40)  # 盈利未达标
        pixlist.extend(tmppixlist)
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [205, 81, 71], 5, 40)  # 亏损
        pixlist.extend(tmppixlist)

        if len(pixlist) != 0:
            for pix in pixlist:
                xx = pix[0]
                yy = pix[1]
                # 排除
                if self.browserHeadless == 'UI':
                    if (xx < 128 * self.screenScaling and yy < 75 * self.screenScaling) or (xx < 195 * self.screenScaling and yy > 338 * self.screenScaling) or (xx > 557 * self.screenScaling and yy > 354 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (xx < 128 and yy < 75) or (xx < 195 and yy > 338) or (xx > 557 and yy > 354):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionElementclickByXY(driver, mapboxglcanvas, xx+3, yy+3)

                self.dapingPbRefreshWaiting(driver)

                self.dapingPbCloseDialog(driver, True)

                if self.tabClickNumOfTimes == 1:
                    break
