# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
import basic.myGlobal as myGlobal
from cases.Zd.appShengXiaPad import AppShengXiaPad
from cases.Zd.appLiulianPad import AppLiuLianPad
from cases.Zd.appZhanQuZhuiZongPad import AppZhanQuZhuiZongPad




logger = myGlobal.getLogger()


class CommApp(AppShengXiaPad, AppLiuLianPad, AppZhanQuZhuiZongPad):
    """战房app-web"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(CommApp, self).__init__(methodName, AllPirParams)


    def testAppLoginOK(self):
        """用例：登录app成功"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        # self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        # self.mySysParameterValueReplaceJson(paramsIn, 'password')
        # userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginOK(driver, userName, password, self.url)


    def testAppLoginPasswordError(self):
        """用例：登录app失败"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginPasswordError(driver, userName, password, self.url)


    def testAppShengXiaOK(self):
        """用例：生虾"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginOK(driver, userName, password, self.url)

        self.appShengXiaPadOK(driver, paramsIn, checkPoint)


    def testAppNiuRouOK(self):
        """用例：牛肉"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginOK(driver, userName, password, self.url)

        self.appNiuRouPadOK(driver, paramsIn, checkPoint)


    def testAppLiuLianOK(self):
        """用例：榴莲"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginOK(driver, userName, password, self.url)

        self.appLiuLianPadOK(driver, paramsIn, checkPoint)


    def testAppZhanQuZhuiZongOK(self):
        """用例：战区追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.appPbParameterDeal(paramsIn)

        self.appPbLoginOK(driver, userName, password, self.url)

        self.appZhanQuZhuiZongPadOK(driver, paramsIn, checkPoint)
