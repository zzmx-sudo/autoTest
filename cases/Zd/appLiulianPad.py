# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal
import re
from cases.Zd.ipadLiulian import IpadLiuLian


logger = basic.myGlobal.getLogger()
# mybatisFile = os.path.basename(sys.argv[0]).replace('.py', '') + '.xml'
mybatisFile = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0] + '.xml'


class AppLiuLianPad(IpadLiuLian):
    """榴莲"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(AppLiuLianPad, self).__init__(methodName, AllPirParams)


    def appLiuLianPadOK(self, driver, paramsIn, checkPoint):
        """榴莲"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.appBottomMenu[0]
        menuStr2 = self.appShouYeMenu[4]
        self.appPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        paramsIn["uiPath"] = uiPath

        self.ipadLiuLianDetail(driver, paramsIn, checkPoint)
