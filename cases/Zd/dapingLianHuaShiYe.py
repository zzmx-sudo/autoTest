# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingLianHuaShiYe(PublicOperation):
    """大屏：莲花事业"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingLianHuaShiYe, self).__init__(methodName, AllPirParams)


    def dapingLianHuaShiYeOK(self, driver, paramsIn, checkPoint):
        """用例说明：莲花事业"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        titleElt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver, endWaitTime=10)

        home = self.myWtEltNonexiContinue(driver, By.CLASS_NAME, "home", maxWaittime=0)
        if home is not None:
            if "display: none;" not in home.get_attribute('style'):
                self.myWtClickEx(driver, By.CLASS_NAME, "home")

        eltList = self.myWtFindElements(driver, By.CLASS_NAME, "ani_content")
        eltList.append(titleElt)
        t1 = self.mySysThreading(self.dapingPbActionMoveToElement, driver, eltList)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.dapingLianHuaShiYeMapDispose(driver, paramsIn, checkPoint)

        self.dapingPbActionMoveToElementStop(t1)


    def dapingLianHuaShiYeMapDispose(self, driver, paramsIn, checkPoint):
        """移动到地图所有点击显示浮窗"""
        title = paramsIn['daPingTitleExpect']

        mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-chinaMap")
        x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
        TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

        pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [0, 249, 72], 5, 40)  # 盈利达标
        tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [255, 55, 28], 5, 40)  # 亏损
        pixlist.extend(tmppixlist)

        if len(pixlist) != 0:
            for pix in pixlist:
                xx = pix[0]
                yy = pix[1]
                # 排除
                if self.browserHeadless == 'UI':
                    if (xx < 100 * self.screenScaling and yy < 100 * self.screenScaling) or (yy > 414 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (xx < 100 and yy < 100) or (yy > 414):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionElementclickByXY(driver, mapboxglcanvas, xx+3, yy+3)

                # self.dapingPbRefreshWaiting(driver)

                self.myWtFindElement(driver, By.CLASS_NAME, "home")

                mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "zd-chinaMap")
                x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
                TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

                pixtmplist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [15, 193, 194], 5, 40)  # 蓝色

                if len(pixtmplist) != 0:
                    for pixtmp in pixtmplist:
                        xx = pixtmp[0]
                        yy = pixtmp[1]
                        # 排除
                        if self.browserHeadless == 'UI':
                            if (xx < 100 * self.screenScaling and yy < 100 * self.screenScaling) or (yy > 414 * self.screenScaling):
                                logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                                continue
                        else:
                            if (xx < 100 and yy < 100) or (yy > 414):
                                logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                                continue

                        self.myWtActionElementclickByXY(driver, mapboxglcanvas, xx + 1, yy + 1)

                        storename = self.myWtFindElement(driver, By.CLASS_NAME, "store").text
                        body = self.myWtFindElements(driver, By.CLASS_NAME, "store-layer")
                        uiPath = '大屏-{}-{}-浮窗'.format(title, storename)
                        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['div'])

                        self.myWtClickEx(driver, By.XPATH, "//span[contains(text(), '标杆对比')]")

                        body = self.myWtFindElements(driver, By.CLASS_NAME, "open")
                        uiPath = '大屏-{}-{}'.format(title, storename)
                        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content', 'num'], tagType=By.CLASS_NAME)

                        body = self.myWtFindElements(driver, By.CLASS_NAME, "list_content")
                        uiPath = '大屏-{}-{}'.format(title, storename)
                        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['span'])

                        self.dapingPbCloseDialog(driver, True)

                        if self.tabClickNumOfTimes == 1:
                            break
                if self.tabClickNumOfTimes == 1:
                    break
