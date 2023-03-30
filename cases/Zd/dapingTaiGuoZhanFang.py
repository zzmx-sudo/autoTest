# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
import re


logger = basic.myGlobal.getLogger()
fileName = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0]


class DapingTaiGuoZhanFang(PublicOperation):
    """大屏：泰国战房"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(DapingTaiGuoZhanFang, self).__init__(methodName, AllPirParams)


    def dapingTaiGuoZhanFangOK(self, driver, paramsIn, checkPoint):
        """用例说明：泰国战房"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        title = paramsIn['daPingTitleExpect']
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), 'Financial')]")
        self.dapingPbRefreshWaiting(driver)

        # 最下方链接
        self.myWtClickEx(driver, By.CLASS_NAME, 'nav-global')
        self.myWtClickEx(driver, By.CLASS_NAME, 'nav-close')

        self.dapingPbFullScreen(driver)

        refFileName = fileName + '-ref.png'
        element = self.myWtFindElement(driver, By.CLASS_NAME, "nav-global")
        self.myPbRefreshWaiting(driver, element, refFileName, 10, None)

        body = self.myWtFindElements(driver, By.TAG_NAME, "body")
        uiPath = '大屏-{}'.format(title)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, body, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # Company Financial Performance List
        jumpurlList = self.myWtFindElements(driver, By.CLASS_NAME, "jump-url")
        for jumpurlNum in range(len(jumpurlList)):
            if jumpurlNum == 0:
                continue
            self.myWtClick(jumpurlList[jumpurlNum])

            dialogElt = self.myWtFindElement(driver, By.CLASS_NAME, "open")
            dialog = self.myWtFindElements(driver, By.CLASS_NAME, "open")
            uiPath = '[大屏]-[{}]-[Company Financial Performance List]'.format(title)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, dialog, tagList=['inner-content'], tagType=By.CLASS_NAME)

            self.dapingPbCloseDialog(dialogElt)

        self.dapingTaiGuoZhanFangNavigationBarComp(driver, paramsIn, checkPoint)


    def dapingTaiGuoZhanFangDlgCheck(self, driver, paramsIn, checkPoint):
        """弹窗检查"""
        title = paramsIn['daPingTitleExpect']

        self.dapingPbRefreshWaiting(driver)
        dialogElt = self.myWtFindElement(driver, By.XPATH, "//section[contains(@class,'masker')]")
        dialog = self.myWtFindElements(driver, By.XPATH, "//section[contains(@class,'masker')]")
        dialogElttext = str(dialogElt.text).split('\n')[0]
        uiPath = '[大屏]-[{}]-[{}]'.format(title, dialogElttext)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, dialog, tagList=['inner-content'], tagType=By.CLASS_NAME)

        # 第二层弹窗
        layerbtnList = self.myWtFindElements(dialogElt, By.CLASS_NAME, "layer-btn")
        for layerbtnNum in range(len(layerbtnList)):
            if layerbtnNum == 0:
                continue
            self.myWtClick(layerbtnList[layerbtnNum])

            self.dapingPbRefreshWaiting(driver)

            dialogdlgElt = self.myWtFindElement(dialogElt, By.XPATH, ".//./following-sibling::section")
            dialogdlgElttext = str(dialogdlgElt.text).split('\n')[0]
            dialogdlg = self.myWtFindElements(dialogElt, By.XPATH, ".//./following-sibling::section")
            uiPath = '[大屏]-[{}]-[{}]-[{}]'.format(title, dialogElttext, dialogdlgElttext)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, dialogdlg, tagList=['inner-content'], tagType=By.CLASS_NAME)

            # self.dapingPbCloseDialog(dialogdlgElt)
            self.dapingPbCloseDialog(dialogdlgElt, actionbar='close-btn')

        # self.dapingPbCloseDialog(dialogElt)
        self.dapingPbCloseDialog(dialogElt, actionbar='close-btn')


    def dapingTaiGuoZhanFangNavigationBarComp(self, driver, paramsIn, checkPoint):
        """选择导航栏并检查地图数据点弹窗"""
        self.myWtClickEx(driver, By.CLASS_NAME, 'head')
        self.myWtFindElement(driver, By.CLASS_NAME, 'drop-box')
        self.dapingTaiGuoZhanFangNavigationBarCompTmp(driver, paramsIn, checkPoint, 'content', driver)


    def dapingTaiGuoZhanFangNavigationBarCompTmp(self, driver, paramsIn, checkPoint, content, elt):
        """选择点击导航栏并检查地图数据点弹窗，递归找子目录"""
        contentC = self.myWtFindElement(elt, By.CLASS_NAME, content)
        dropbox = self.myWtFindElement(contentC, By.XPATH, ".//./div[contains(@class,'drop-box')]")
        dropitemList = self.myWtFindElements(dropbox, By.CLASS_NAME, 'drop-item')
        for menuNum in range(len(dropitemList)):
            contentClk = self.myWtFindElement(elt, By.CLASS_NAME, content)
            dropboxClk = self.myWtFindElement(contentClk, By.XPATH, ".//./div[contains(@class,'drop-box')]")
            dropitemClkList = self.myWtFindElements(dropboxClk, By.CLASS_NAME, 'drop-item')
            clk, localdropitem = self.dapingPbDropChildrenClick(driver, paramsIn, checkPoint, dropitemClkList, menuNum)

            if self.myWtEltNonexiContinue(localdropitem, By.XPATH, ".//*[name()='svg' and contains(@class,'iconfont')]") is not None:
                self.dapingTaiGuoZhanFangNavigationBarCompTmp(driver, paramsIn, checkPoint, 'drop-children', contentClk)
            else:
                time.sleep(1)

                self.dapingPbRefreshWaiting(driver)

                mapboxglcanvas = self.myWtFindElement(driver, By.CLASS_NAME, "mapboxgl-canvas")
                x, y, width, height = self.myPbGetElementSize(mapboxglcanvas)
                TEMP_FILE = self.myWtScreenshotByxy(driver, x, y, width, height)

                pixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [202, 46, 17], 2, 20)  # %Change＜0
                tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [211, 182, 3], 2, 20)  # 0≤%Change ≤5%
                pixlist.extend(tmppixlist)
                tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [1, 210, 61], 0, 20)  # %Change > 5%
                pixlist.extend(tmppixlist)
                tmppixlist = self.myWtImageSimilarColorSortOut(TEMP_FILE, [165, 165, 167], 5, 20)  # No data
                pixlist.extend(tmppixlist)

                if len(pixlist) != 0:
                    for pix in pixlist:
                        xx = pix[0]
                        yy = pix[1]
                        # 排除
                        if self.browserHeadless == 'UI':
                            if xx < 500 * self.screenScaling or xx > 1600 * self.screenScaling or yy > 760 * self.screenScaling or yy < 200 * self.screenScaling:
                                logger.debug("不用处理的坐标: ({},{})".format(xx * self.screenScaling, yy * self.screenScaling))
                                continue
                        else:
                            if xx < 500 or xx > 1600 or yy > 760 or yy < 200:
                                logger.debug("不用处理的坐标: ({},{})".format(xx, yy))
                                continue

                        self.myWtActionMoveToElementByXY(driver, mapboxglcanvas, xx, yy)

                        # self.dapingPbRefreshWaiting(driver)

                        rst = self.dapingTaiGuoZhanFangFuChuang(driver, paramsIn, checkPoint)

                        if rst:
                            if self.tabClickNumOfTimes == 1:
                                break
                    if self.tabClickNumOfTimes == 1:
                        break

                self.myWtClickEx(driver, By.CLASS_NAME, 'head')

            if self.tabClickNumOfTimes == 1:
                break
            break


    def dapingTaiGuoZhanFangFuChuang(self, driver, paramsIn, checkPoint):
        """判断地图浮窗是否存在，存在则点击打开并检查"""
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'mapboxgl-popup-anchor-bottom', maxWaittime=1) is not None:
            self.myWtClickEx(driver, By.CLASS_NAME, 'mapboxgl-popup-anchor-bottom')

            self.dapingTaiGuoZhanFangDlgCheck(driver, paramsIn, checkPoint)

            # 关闭浮窗
            largerMap = self.myWtFindElement(driver, By.CLASS_NAME, "zd-largerMap")
            self.myWtActionElementclickByXY(driver, largerMap, 10, 10)
            time.sleep(1)

            return True
        else:
            return False

