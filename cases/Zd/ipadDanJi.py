# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal



logger = basic.myGlobal.getLogger()


class IpadDanJi(PublicOperation):
    """蛋鸡"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadDanJi, self).__init__(methodName, AllPirParams)


    def ipadDanJiOK(self, driver, paramsIn, checkPoint):
        """中国区地图"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        districtName = paramsIn['DistrictName']
        companyName = paramsIn['CompanyName']
        farmName = paramsIn['FarmName']
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[11]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        self.myWtFindElement(driver, By.XPATH, "//span[text()='中国区']")

        maincontent = self.myWtFindElements(driver, By.XPATH, "//div[@class='main-content']")
        uiPath = '{}-{}-中国区'.format(menuStr1, menuStr2)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath+'(地图左边显示栏)', maincontent, tagList=['div', 'span'])

        self.ipadDanJiIconUp(driver, paramsIn, checkPoint)

        # 点击隐藏和显示左框
        self.myWtClickEx(driver, By.XPATH, "//img[contains(@class, 'icon-circle')]")
        time.sleep(1)
        self.myWtClickEx(driver, By.XPATH, "//img[contains(@class, 'icon-circle')]")

        # 切换中国区表格
        self.myWtClickEx(driver, By.XPATH, "//*[name()='svg' and contains(@class,'icon_down')]")

        # 日期控件年月周日顺序点击
        datetypeList = ['年', '月', '周', '日']
        for datetype in datetypeList:
            date = self.mySysGetDate(day=-35)

            self.ipadPbSelectShowDate(driver, datetype, date)

            self.ipadDanJiChina(driver, paramsIn, checkPoint, uiPath)

            self.myWtGetJsLog(driver, self.jsLogExclude)

            if self.dateClickNumOfTimes == 1:
                break
        self.ipadPbLeftBack(driver)


    def ipadDanJiIconUp(self, driver, paramsIn, checkPoint):
        """养殖效率综合指标"""
        self.myWtClickEx(driver, By.XPATH, "//img[contains(@class, 'icon-up')]")
        # self.ipadPbRefreshWaiting(driver)
        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'bar-item')]")
        for item in itemList:
            self.myWtClick(item)
        # self.ipadPbRefreshWaiting(driver)
        self.myWtGetJsLog(driver, self.jsLogExclude)
        # popup = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'van-popup--center')]")
        # self.myWtClickEx(popup, By.TAG_NAME, "svg")
        self.myWtClickEx(driver, By.XPATH, "//*[name()='svg' and contains(@class,'del')]")


    def ipadDanJiChina(self, driver, paramsIn, checkPoint, uiPath):
        """中国区列表"""
        self.ipadPbRefreshWaiting(driver)
        tabList = ['大区排名', '公司排名', '养殖场排名']
        for tab in tabList:
            self.myWtClickEx(driver, By.XPATH, "//span[contains(text(), '{}')]".format(tab))
            self.ipadPbRefreshWaiting(driver)

            uiPathT = '{}({})'.format(uiPath, tab)
            tbody = self.myWtFindElements(driver, By.CLASS_NAME, 'tbody')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, tbody, By.CLASS_NAME, 'tbody_row', By.TAG_NAME, 'li', tagList=['div'])

            rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
            for row in rowList:
                text = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'van-tab--active')]").text
                self.myWtClick(row)
                if '大区' in text:
                    uiPathT = '{}-{}'.format(uiPath, tab.replace('排名', ''))
                    self.ipadDanJiDaqu(driver, paramsIn, checkPoint, uiPathT)
                elif '公司' in text:
                    uiPathT = '{}-大区-{}'.format(uiPath, tab.replace('排名', ''))
                    self.ipadDanJiGongsi(driver, paramsIn, checkPoint, uiPathT)
                elif '养殖场' in text:
                    uiPathT = '{}-大区-公司-{}'.format(uiPath, tab.replace('排名', ''))
                    self.ipadDanJiJichang(driver, paramsIn, checkPoint, uiPathT)

                if self.tabClickNumOfTimes == 1:
                    break


    def ipadDanJiDaqu(self, driver, paramsIn, checkPoint, uiPath):
        """大区"""
        self.ipadPbRefreshWaiting(driver)

        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '大区负责人')]")

        # 检查
        uiPathT = '{}'.format(uiPath)
        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "region-grid")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(总览)', regionmain, tagList=['div', 'span'])

        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "region-grid-table")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(品项)', regionmain, tagList=['div', 'p', 'span'])

        regiongridtable = self.myWtFindElement(driver, By.CLASS_NAME, "region-grid-table")
        regionmain = self.myWtFindElements(regiongridtable, By.CLASS_NAME, "table-body")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(品项)table', regionmain, By.TAG_NAME, 'li', By.CLASS_NAME, 'body-item', tagList=[])

        chargetable = self.myWtFindElement(driver, By.CLASS_NAME, 'region-charge-table')
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-head')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, excludeTextList=['(元/kg)'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, tagList=['div'])
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-body')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', excludeTextList=['至今'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', tagList=['div'])

        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, 'tbody_reverse_color')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(公司排名)', regionmain, By.CLASS_NAME, "tbody_row", By.TAG_NAME, 'li', tagList=['div'])
        uiPathT = '{}-公司'.format(uiPath)

        self.ipadDanJiIconUp(driver, paramsIn, checkPoint)

        self.ipadPbRefreshWaiting(driver)
        # 公司列表
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadPbRefreshWaiting(driver)
            self.ipadDanJiGongsi(driver, paramsIn, checkPoint, uiPathT)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)

    def ipadDanJiGongsi(self, driver, paramsIn, checkPoint, uiPath):
        """公司"""
        self.ipadPbRefreshWaiting(driver)

        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '公司负责人对比')]")

        # 检查
        uiPathT = '{}'.format(uiPath)
        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "grid-list")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(总览)', regionmain, tagList=['div', 'span'])

        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "middle-grid-table")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(品项)', regionmain, tagList=['div', 'p', 'span'])

        regiongridtable = self.myWtFindElement(driver, By.CLASS_NAME, "middle-grid-table")
        regionmain = self.myWtFindElements(regiongridtable, By.CLASS_NAME, "table-body")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(品项)table', regionmain, By.TAG_NAME, 'li', By.CLASS_NAME, 'body-item', tagList=[])

        chargetable = self.myWtFindElement(driver, By.CLASS_NAME, 'table-warp')
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-head')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, excludeTextList=['(元/kg)'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, tagList=['div'])
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-body')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', excludeTextList=['至今'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', tagList=['div'])

        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, 'tbody_reverse_color')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(养殖场排名)', regionmain, By.CLASS_NAME, "tbody_row", By.TAG_NAME, 'li', tagList=['div'])
        uiPathT = '{}-养殖场'.format(uiPath)

        # t1.join()

        self.ipadDanJiIconUp(driver, paramsIn, checkPoint)
        self.ipadPbRefreshWaiting(driver)

        # 公司负责人列表
        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'table-list-item')]")
        for item in itemList:
            self.myWtClick(item)
            self.ipadPbCloseTopRight(driver)
            if self.tabClickNumOfTimes == 1:
                break

        # 养殖场列表
        self.ipadPbRefreshWaiting(driver)
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadDanJiJichang(driver, paramsIn, checkPoint, uiPathT)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadDanJiJichang(self, driver, paramsIn, checkPoint, uiPath):
        """养殖场"""
        self.ipadPbRefreshWaiting(driver)

        elt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '养殖场负责人对比')]")

        # 检查
        uiPathT = '{}'.format(uiPath)
        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "grid-list")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(总览)', regionmain, tagList=['div', 'span'])

        chargetable = self.myWtFindElement(driver, By.CLASS_NAME, 'table-warp')
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-head')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, excludeTextList=['(元/kg)'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(负责人)title', regionmain, tagList=['div'])
        regionmain = self.myWtFindElements(chargetable, By.CLASS_NAME, 'table-body')
        # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', excludeTextList=['至今'], tagList=['div'])
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(负责人)table', regionmain, tdby=By.CLASS_NAME, tdCtrlIdent='common-width', tagList=['div'])

        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, 'tbody_reverse_color')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(栋舍排名)', regionmain, By.CLASS_NAME, "tbody_row", By.TAG_NAME, 'li', tagList=['div'])
        uiPathT = '{}-栋舍'.format(uiPath)

        # t1.join()

        self.ipadDanJiIconUp(driver, paramsIn, checkPoint)
        self.ipadPbRefreshWaiting(driver)

        self.myWtH5FlickDown(driver, elt)
        self.myWtH5FlickUp(driver, elt)

        self.ipadPbRefreshWaiting(driver)
        itemList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'table-list-item')]")
        for item in itemList:
            self.myWtClick(item)
            self.ipadPbCloseTopRight(driver)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbRefreshWaiting(driver)
        rowList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'tbody_row')]")
        for row in rowList:
            self.myWtClick(row)
            self.ipadDanJiDongshe(driver, paramsIn, checkPoint, uiPathT)
            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadDanJiDongshe(self, driver, paramsIn, checkPoint, uiPath):
        """栋舍"""
        self.ipadPbRefreshWaiting(driver)

        # 检查
        uiPathT = '{}'.format(uiPath)
        regionmain = self.myWtFindElements(driver, By.CLASS_NAME, "grid-list")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT + '(总览)', regionmain, tagList=['div', 'span'])

        self.ipadDanJiIconUp(driver, paramsIn, checkPoint)

        self.ipadPbRefreshWaiting(driver)

        self.ipadPbLeftBack(driver)



