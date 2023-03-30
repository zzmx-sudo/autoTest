# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal


logger = basic.myGlobal.getLogger()


class DapingCTISiLiaoZhuiZong(PublicOperation):
    """大屏：CTI饲料追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingCTISiLiaoZhuiZong, self).__init__(methodName, AllPirParams)


    def dapingCTISiLiaoZhuiZongOK(self, driver, paramsIn, checkPoint):
        """用例说明：CTI饲料追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '{}')]".format(title))
        self.dapingPbRefreshWaiting(driver)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.dapingCTISiLiaoZhuiZongMapDispose(driver, paramsIn, checkPoint)

        # 切换省区、公司
        tabsitemList = self.myWtFindElements(driver, By.CLASS_NAME, "tabs_item")
        for tabsitemNum in range(0, len(tabsitemList)):
            if tabsitemNum == 0:
                continue
            self.myWtClick(tabsitemList[tabsitemNum])

            self.dapingPbRefreshWaiting(driver)

            body = self.myWtFindElements(driver, By.CLASS_NAME, "map_analyze_yufeicarousel")
            uiPath = '大屏-{}'.format(title)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        self.myWtClickEx(driver, By.CLASS_NAME, 'head')
        self.myWtFindElement(driver, By.CLASS_NAME, 'drop-box')
        self.dapingCTISiLiaoZhuiZongDataSelect(driver, paramsIn, checkPoint, 'content', driver)


    def dapingCTISiLiaoZhuiZongDataSelect(self, driver, paramsIn, checkPoint, content, elt):
        """选择所有列表中的日期"""
        title = paramsIn['daPingTitleExpect']
        contentC = self.myWtFindElement(elt, By.CLASS_NAME, content)
        dropbox = self.myWtFindElement(contentC, By.XPATH, ".//./div[contains(@class,'drop-box')]")
        dropitemList = self.myWtFindElements(dropbox, By.CLASS_NAME, 'drop-item')
        for menuNum in range(len(dropitemList)):
            contentClk = self.myWtFindElement(elt, By.CLASS_NAME, content)
            dropboxClk = self.myWtFindElement(contentClk, By.XPATH, ".//./div[contains(@class,'drop-box')]")
            dropitemClkList = self.myWtFindElements(dropboxClk, By.CLASS_NAME, 'drop-item')
            clk, localdropitem = self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, dropitemClkList, menuNum)

            if self.myWtEltNonexiContinue(localdropitem, By.XPATH, ".//*[name()='svg' and contains(@class,'iconfont')]") is not None:
                self.dapingCTISiLiaoZhuiZongDataSelect(driver, paramsIn, checkPoint, 'drop-children', contentClk)
            else:
                time.sleep(1)

                self.dapingPbRefreshWaiting(driver)

                datatext = str(self.myWtFindElement(driver, By.CLASS_NAME, 'head').text).replace(" ", "")
                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}-{}'.format(title, datatext)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

                self.myWtClickEx(driver, By.CLASS_NAME, 'head')

                if self.tabClickNumOfTimes == 1:
                    break


    def dapingCTISiLiaoZhuiZongMapDispose(self, driver, paramsIn, checkPoint):
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
                    if (xx < 231 * self.screenScaling and yy > 354 * self.screenScaling) or (xx < 154 * self.screenScaling and yy < 83 * self.screenScaling) or (xx > 497 * self.screenScaling and yy > 316 * self.screenScaling):
                        logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                        continue
                else:
                    if (xx < 231 and yy > 354) or (xx < 154 and yy < 83) or (xx > 497 and yy > 316):
                        logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                        continue

                self.myWtActionMoveToElementByXY(driver, mapboxglcanvas, xx+3, yy+3)

                body = self.myWtFindElements(driver, By.TAG_NAME, "body")
                uiPath = '大屏-{}'.format(title)
                self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['tooltip_number'], tagType=By.CLASS_NAME)

                if self.tabClickNumOfTimes == 1:
                    break
