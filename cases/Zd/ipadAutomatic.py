# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal

logger = basic.myGlobal.getLogger()


class IpadAutomatic(PublicOperation):
    """登录模块"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadAutomatic, self).__init__(methodName, AllPirParams)


    def ipadAutomaticOK(self, driver, paramsIn, checkPoint):
        """"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        for leftMenu in reversed(self.ipadLeftMenu):
            self.ipadPbSelectMainMenu(driver, menuStr1=leftMenu)
            self.ipadPbRefreshWaiting(driver)

            self.ipadRecursionClick(driver, paramsIn, checkPoint, [], self.ipadLeftMenu)


    def ipadRecursionClick(self, driver, paramsIn, checkPoint, clickOuterHTMLList=[], clickTextList=[]):
        """"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        divEltList = self.myWtFindElements(driver, By.TAG_NAME, 'div')
        buttonEltList = self.myWtFindElements(driver, By.TAG_NAME, 'button')
        # divEltList.reverse()
        eltList = divEltList + buttonEltList

        # 判断界面是否存在dialog
        ifDialog = 0
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'van-dialog', 0, 0.5):
            ifDialog = 1

        for elt in eltList:
            try:
                if not elt.is_displayed():
                    continue
                if not elt.is_enabled():
                    continue
            except:
                continue

            height = elt.size['height']
            width = elt.size['width']

            if height < 120 and height > 16:  # 20
                logger.debug('width:{},height:{}'.format(width, height))
                outerHTML = self.mySysStringCleanup(str(elt.get_attribute("outerHTML"))).replace(' ', '')
                # logger.debug('outerHTML:{}'.format(outerHTML))
                # logger.debug('text:{}'.format(elt.get_attribute("innerText")))
                excludeTextRst, clickOuterHTMLList = self.ipadExcludeTextElt(driver, paramsIn, checkPoint, outerHTML, clickOuterHTMLList, clickTextList)
                # logger.debug('clickOuterHTMLList:{}'.format(clickOuterHTMLList))
                excludeHtmlRst = self.ipadExcludeHtmlElt(driver, paramsIn, checkPoint, outerHTML, clickOuterHTMLList)
                if excludeTextRst and excludeHtmlRst:
                    clickElt = self.myWtElementEx(elt, 1, 1, 0.5)
                    if (clickElt is not None) and (clickElt.get_attribute("class") != 'showDate'):
                        logger.debug('outerHTMLOk:{}'.format(outerHTML))
                        logger.debug('clickOuterHTMLListOk:{}'.format(clickOuterHTMLList))
                        pasttUrl = driver.current_url
                        pastPngFilename = self.myWtScreenshotByXyAsFile(driver)
                        self.myWtClick(elt, 0, 0.5)
                        clickOuterHTMLList.append(outerHTML)
                        time.sleep(1)
                        # self.myWtFindElement(driver, By.TAG_NAME, 'body')
                        self.ipadPbRefreshWaiting(driver)
                        currentUrl = driver.current_url
                        crtPngFilename = self.myWtScreenshotByXyAsFile(driver)
                        cpRst = self.myWtImageCompare(pastPngFilename, crtPngFilename)
                        # self.mySysRemoveFile(pastPngFilename)
                        # self.mySysRemoveFile(crtPngFilename)
                        if (pasttUrl != currentUrl) or (cpRst is False):
                            self.ipadRecursionClick(driver, paramsIn, checkPoint, clickOuterHTMLList, clickTextList)
            logger.debug('clickOuterHTMLList个数:{}'.format(len(clickOuterHTMLList)))
        # 点击<退出当前界面
        if ifDialog == 0:
            self.ipadPbLeftBack(driver, 0.5)


    def ipadExcludeHtmlElt(self, driver, paramsIn, checkPoint, outerHTML ,clickOuterHTMLList):
        """"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        # list = ['<button', '退出登录', 'van-toast--loading', '托管模式', 'van-overlay']
        list = ['安全中心', '语言切换', '清除缓存', '版本更新', '退出登录', 'van-toast--loading', '托管模式', 'van-overlay']
        for item in list:
            if item in str(clickOuterHTMLList):
                return False
        for html in clickOuterHTMLList:
            if outerHTML in str(html):
                return False
        return True


    def ipadExcludeTextElt(self, driver, paramsIn, checkPoint, outerHTML, clickOuterHTMLList, clickTextList):
        """"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        for text in clickTextList:
            logger.debug("ipadExcludeTextElt:{}\n{}".format(outerHTML, text))
            if text in str(outerHTML):
                logger.debug("ipadExcludeTextEltOk:{}".format(text))
                clickOuterHTMLList.append(outerHTML)
                return False, clickOuterHTMLList
        return True, clickOuterHTMLList
