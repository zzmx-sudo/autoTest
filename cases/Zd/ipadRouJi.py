# -*- coding:utf-8 -*-
import sys
import os
import time
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal

logger = basic.myGlobal.getLogger()


class IpadRouJi(PublicOperation):
    """肉鸡"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadRouJi, self).__init__(methodName, AllPirParams)


    def ipadRouJiOK(self, driver, paramsIn, checkPoint):
        """肉鸡"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[8]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        jiTypeList = ['肉种鸡', '肉鸡']
        for jiType in jiTypeList:
            self.myWtClickEx(driver, By.XPATH, "//span[text()='{}']".format(jiType))

            self.ipadPbRefreshWaiting(driver)

            maincontent = self.myWtFindElements(driver, By.XPATH, "//div[@class='main-content']")
            uiPath = '{}-{}-中国区'.format(menuStr1, menuStr2)
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath + '(地图左边显示栏)', maincontent, tagList=['div', 'span'])

            self.ipadRouJiIconUp(driver, paramsIn, checkPoint)

            self.myWtClickEx(driver, By.XPATH, "//img[contains(@class, 'icon-circle')]")
            time.sleep(1)
            self.myWtClickEx(driver, By.XPATH, "//img[contains(@class, 'icon-circle')]")

            self.myWtClickEx(driver, By.XPATH, "//*[name()='svg' and contains(@class,'icon_down')]")

            datetypeList = ['年', '月', '周', '日']
            for datetype in datetypeList:
                date = self.mySysGetDate(day=-35)

                self.ipadPbSelectShowDate(driver, datetype, date)

                self.ipadRouJiChina(driver, paramsIn, checkPoint)

                self.myWtGetJsLog(driver, self.jsLogExclude)

                if self.dateClickNumOfTimes == 1:
                    break

            if self.myWtEltNonexiContinue(driver, By.XPATH, "//*[name()='svg' and contains(@class,'icon_up')]") is not None:
                self.myWtClickEx(driver, By.XPATH, "//*[name()='svg' and contains(@class,'icon_up')]")

        self.ipadPbLeftBack(driver)


    def ipadRouJiIconUp(self, driver, paramsIn, checkPoint):
        """养殖效率综合指标"""
        self.ipadPbRefreshWaiting(driver)
        iconup = "//img[contains(@class, 'icon-up')]"
        divimg = "//div[contains(text(), '养殖效率综合指标')]/../img"
        spanimg = "//span[contains(text(), '养殖效率综合指标')]/../img"
        img = "//*[contains(text(), '养殖效率综合指标')]/../img"
        topleftheader = "//div[contains(@class, 'top-left-header')]/img"
        targetheader = "//div[contains(@class, 'target-header')]/img"
        if self.myWtEltNonexiContinue(driver, By.XPATH, img, maxWaittime=0.5) is not None:
            self.myWtClickEx(driver, By.XPATH, img)
        elif self.myWtEltNonexiContinue(driver, By.XPATH, topleftheader, maxWaittime=0.5) is not None:
            self.myWtClickEx(driver, By.XPATH, topleftheader)
        elif self.myWtEltNonexiContinue(driver, By.XPATH, targetheader, maxWaittime=0.5) is not None:
            self.myWtClickEx(driver, By.XPATH, targetheader)
        else:
            self.mySysAssert(iconup)
        # self.ipadPbRefreshWaiting(driver)
        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'bar-item')]")
        for item in itemList:
            self.myWtClick(item)
        # self.ipadPbRefreshWaiting(driver)
        self.myWtGetJsLog(driver, self.jsLogExclude)
        # popup = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'van-popup--center')]")
        # self.myWtClickEx(popup, By.TAG_NAME, "svg")
        self.myWtClickEx(driver, By.XPATH, "//*[name()='svg' and contains(@class,'del')]")


    def ipadRouJiChina(self, driver, paramsIn, checkPoint):
        """中国区列表"""
        self.ipadPbRefreshWaiting(driver)
        self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadRouJiDaqu(driver, paramsIn, checkPoint)

            if self.tabClickNumOfTimes == 1:
                break


    def ipadRouJiDaqu(self, driver, paramsIn, checkPoint):
        """大区"""
        self.ipadPbRefreshWaiting(driver)

        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '历任大区负责人')]")
        self.ipadRouJiIconUp(driver, paramsIn, checkPoint)

        self.ipadPbRefreshWaiting(driver)
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadPbRefreshWaiting(driver)
            self.ipadRouJiGongsi(driver, paramsIn, checkPoint)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadRouJiGongsi(self, driver, paramsIn, checkPoint):
        """公司"""
        self.ipadPbRefreshWaiting(driver)

        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '历任公司负责人')]")
        self.ipadRouJiIconUp(driver, paramsIn, checkPoint)
        self.ipadPbRefreshWaiting(driver)

        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'item-left')]")
        for item in itemList:
            self.myWtClick(item)
            self.ipadPbCloseTopRight(driver)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbRefreshWaiting(driver)
        rowList = self.myWtFindElements(driver, By.XPATH, "//section[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadRouJiJichang(driver, paramsIn, checkPoint)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadRouJiJichang(self, driver, paramsIn, checkPoint):
        """养殖场"""
        self.ipadPbRefreshWaiting(driver)

        elt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '历任养殖场负责人')]")
        self.ipadRouJiIconUp(driver, paramsIn, checkPoint)
        self.ipadPbRefreshWaiting(driver)

        self.myWtH5FlickDown(driver, elt)
        self.myWtH5FlickUp(driver, elt)

        self.ipadPbRefreshWaiting(driver)
        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'fuzeren')]")
        for item in itemList:
            self.myWtClick(item)
            self.ipadPbCloseTopRight(driver)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbRefreshWaiting(driver)
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadRouJiDongshe(driver, paramsIn, checkPoint)

            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadRouJiDongshe(self, driver, paramsIn, checkPoint):
        """栋舍"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadRouJiIconUp(driver, paramsIn, checkPoint)

        self.ipadPbRefreshWaiting(driver)

        self.ipadPbLeftBack(driver)



