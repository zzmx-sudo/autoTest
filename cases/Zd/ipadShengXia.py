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
# mybatisFile = os.path.basename(sys.argv[0]).replace('.py', '') + '.xml'
mybatisFile = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0] + '.xml'


class IpadShengXia(PublicOperation):
    """生虾"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadShengXia, self).__init__(methodName, AllPirParams)


    def ipadShengXiaOK(self, driver, paramsIn, checkPoint):
        """生虾"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[5]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    def ipadHunTunOK(self, driver, paramsIn, checkPoint):
        """馄饨"""
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[7]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    def ipadNiuRouOK(self, driver, paramsIn, checkPoint):
        """牛肉"""
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[2]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        self.ipadShengXiaDetail(driver, paramsIn, checkPoint)


    def ipadShengXiaDetail(self, driver, paramsIn, checkPoint):
        """生虾处理"""
        uiPath = paramsIn["uiPath"]

        self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        # self.ipadShengXiaBatch(driver, paramsIn, checkPoint)

        datetypeList = ['年', '月']
        for datetype in datetypeList:
            date = self.mySysGetDate(day=-35)

            self.ipadPbSelectShowDate(driver, datetype, date)

            uiPathT = '{}-中国区'.format(uiPath)
            table = self.myWtFindElements(driver, By.CLASS_NAME, 'table')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['span'])

            # 点击“全链”
            # cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
            # spanList = self.myWtFindElements(cabinetsNumber, By.TAG_NAME, 'span')
            # for span in reversed(spanList):
            #     self.myWtClick(span)
            #     self.ipadShengXiaQuanLian(driver, paramsIn, checkPoint, uiPathT)
            #     break
            #
            # cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
            # self.myWtH5FlickDown(driver, cabinetsNumber)
            B2C = self.myWtFindElement(driver, By.XPATH, "//p[contains(text(), 'B2C')]")
            self.myWtH5FlickDown(driver, B2C)

            self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

            uiPathT = '{}-终端渠道'.format(uiPath)
            table = self.myWtFindElements(driver, By.CLASS_NAME, 'content')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

            # 莲花、优鲜
            jumpList = self.myWtFindElements(driver, By.CLASS_NAME, 'jump')
            for jump in jumpList:
                text = self.myWtFindElement(jump, By.XPATH, './/..').text
                self.myWtClick(jump)
                time.sleep(3)
                if '莲花' in text:
                    self.ipadShengXiaLianHua(driver, paramsIn, checkPoint, uiPathT)
                else:
                    self.ipadShengXiaYouXian(driver, paramsIn, checkPoint, uiPathT)

            elt = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '优鲜')]")
            self.myWtH5FlickDown(driver, elt)

            self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

            uiPathT = '{}-中国区SVC'.format(uiPath)
            table = self.myWtFindElements(driver, By.CLASS_NAME, 'svc_content')
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

            # 中国区SVC
            hearderImgList = self.myWtFindElements(driver, By.CLASS_NAME, 'hearderImg')
            for hearderImg in hearderImgList:
                self.myWtClick(hearderImg)

                self.ipadShengXiaSVC(driver, paramsIn, checkPoint, uiPath)

                if self.tabClickNumOfTimes == 1:
                    break

            self.ipadShengXiaKuChun(driver, paramsIn, checkPoint)

            if self.dateClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadShengXiaQuanLian(self, driver, paramsIn, checkPoint, uiPath):
        """全链"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        uiPathT = '{}-全链'.format(uiPath)
        table = self.myWtFindElements(driver, By.CLASS_NAME, 'left')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'right')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        # 曹VC自销、统一分配
        imagerightList = self.myWtFindElements(driver, By.CLASS_NAME, 'image_right')
        for imageright in imagerightList:
            name = self.myWtFindElement(imageright, By.XPATH, './/../..').text
            self.myWtClick(imageright)
            if '曹VC自销' in name:
                self.ipadShengXiaCaoVCZhixiao(driver, paramsIn, checkPoint, uiPathT)
            else:
                self.ipadShengXiaTongYifenPei(driver, paramsIn, checkPoint, uiPathT)

        self.ipadPbLeftBack(driver)


    def ipadShengXiaCaoVCZhixiao(self, driver, paramsIn, checkPoint, uiPath):
        """曹VC自销"""
        self.ipadShengXiaSVC(driver, paramsIn, checkPoint, uiPath)


    def ipadShengXiaTongYifenPei(self, driver, paramsIn, checkPoint, uiPath):
        """统一分配"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        uiPathT = '{}-统一分配'.format(uiPath)
        table = self.myWtFindElements(driver, By.CLASS_NAME, 'svc_content')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        # 单击SVC
        hrowList = self.myWtFindElements(driver, By.CLASS_NAME, 'hrow')
        for hrow in hrowList:
            self.myWtClick(hrow)

            self.ipadShengXiaSVC(driver, paramsIn, checkPoint, uiPathT)

            if self.tabClickNumOfTimes == 1:
                break

        self.ipadPbLeftBack(driver)


    def ipadShengXiaSVC(self, driver, paramsIn, checkPoint, uiPath):
        """SVC"""
        self.ipadPbRefreshWaiting(driver)

        title = self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        self.myWtFindElement(driver, By.XPATH, "//div[text()='单位: 万']")

        uiPathT = '{}-SVC'.format(uiPath)
        table = self.myWtFindElements(driver, By.CLASS_NAME, 'content')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        self.ipadPbLeftBack(driver)


    def ipadShengXiaLianHua(self, driver, paramsIn, checkPoint, uiPath):
        """莲花"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        uiPathT = '{}-莲花'.format(uiPath)
        table = self.myWtFindElements(driver, By.CLASS_NAME, 'left')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'right')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['span'])

        self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'left')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'right')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['span'])

        self.ipadPbLeftBack(driver)


    def ipadShengXiaYouXian(self, driver, paramsIn, checkPoint, uiPath):
        """优鲜"""
        self.ipadPbRefreshWaiting(driver)

        self.ipadShengXiaWebPageTitle(driver, paramsIn, checkPoint)

        uiPathT = '{}-优鲜'.format(uiPath)
        table = self.myWtFindElements(driver, By.CLASS_NAME, 'left')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'right')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['span'])

        self.myWtClickEx(driver, By.XPATH, "//li[text()='排省']")

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'left')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['li'])

        table = self.myWtFindElements(driver, By.CLASS_NAME, 'right')
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT, table, tagList=['span'])

        self.ipadPbLeftBack(driver)


    def ipadShengXiaWebPageTitle(self, driver, paramsIn, checkPoint):
        """获取和打印网页标题"""
        header = self.mySysStringCleanup(self.myWtFindElement(driver, By.CLASS_NAME, 'header').text)
        logger.debug('当前界面：{}'.format(header))
        return header


    def ipadShengXiaBatch(self, driver, paramsIn, checkPoint):
        """批次"""
        self.myWtClickEx(driver, By.CLASS_NAME, "showBatch")
        time.sleep(1)
        pickerdates = self.myWtFindElement(driver, By.CLASS_NAME, "picker_dates")
        tab = self.myWtFindElement(pickerdates, By.CLASS_NAME, "tab")
        divList = self.myWtFindElements(tab, By.TAG_NAME, "div")
        for div in divList:
            self.myWtClick(div)
            time.sleep(1)
            break

        self.myWtClickEx(driver, By.CLASS_NAME, "showBatch")
        time.sleep(1)
        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '所有订单')]")


    def ipadShengXiaKuChun(self, driver, paramsIn, checkPoint):
        """库存情况"""
        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '库存情况') and contains(@class,'up')]")
        time.sleep(1)
        self.myWtClickEx(driver, By.XPATH, "//div[contains(text(), '库存情况') and contains(@class,'down')]")

