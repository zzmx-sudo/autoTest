# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingSiLiao(PublicOperation):
    """大屏：饲料"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingSiLiao, self).__init__(methodName, AllPirParams)


    def dapingSiLiaoOK(self, driver, paramsIn, checkPoint):
        """用例说明：饲料"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        # 选择月
        self.myWtClickEx(driver, By.CLASS_NAME, 'selectedbox')
        self.myWtClickEx(driver, By.XPATH, "//*[contains(text(), '本月')]")
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 选择年
        self.myWtClickEx(driver, By.CLASS_NAME, 'selectedbox')
        self.myWtClickEx(driver, By.XPATH, "//*[contains(text(), '本年')]")
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.dapingSiLiaoMapDispose(driver, paramsIn, checkPoint)


    def dapingSiLiaoMapDispose(self, driver, paramsIn, checkPoint):
        """移动到地图所有点击显示浮窗"""
        title = paramsIn['daPingTitleExpect']

        mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-chinaMap")
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
                    if (yy < 78 * self.screenScaling) or (xx < 238 * self.screenScaling and yy > 331 * self.screenScaling) or (xx > 465 * self.screenScaling and yy > 320 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (yy < 78) or (xx < 238 and yy > 331) or (xx > 465 and yy > 320):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionMoveToElementByXY(driver, mapboxglcanvas, xx+3, yy+3)

                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}'.format(title)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['tooltip_number'], tagType=By.CLASS_NAME)

                if self.tabClickNumOfTimes == 1:
                    break
