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


class IpadNiuRou(PublicOperation):
    """牛肉"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadNiuRou, self).__init__(methodName, AllPirParams)


    def ipadNiuRouOK(self, driver, paramsIn, checkPoint):
        """牛肉"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[2]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = ''

        cabinetsNumber = self.myWtFindElement(driver, By.CLASS_NAME, 'cabinetsNumber')
        spanList = self.myWtFindElements(cabinetsNumber, By.TAG_NAME, 'span')
        for span in reversed(spanList):
            # 点击“全链:>”
            self.myWtClick(span)
            break

        self.ipadPbLeftBack(driver)
