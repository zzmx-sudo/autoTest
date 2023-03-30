# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
import basic.myGlobal as myGlobal
# from cases.Zd.ipadAutomatic import IpadAutomatic
from cases.Zd.ipadWuLiuZhuiZong import IpadWuLiuZhuiZong
from cases.Zd.ipadDanJi import IpadDanJi
from cases.Zd.ipadRouJi import IpadRouJi
from cases.Zd.ipadShengXia import IpadShengXia
# from cases.Zd.ipadHunTun import IpadHunTun
# from cases.Zd.ipadNiuRou import IpadNiuRou




logger = myGlobal.getLogger()


class Comm(IpadWuLiuZhuiZong, IpadDanJi, IpadRouJi, IpadShengXia):
    """战房ipad-web"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(Comm, self).__init__(methodName, AllPirParams)


    # def testIpadAutomaticOK(self):
    #     """用例：网页ipad全自动点击探索"""
    #     # caseName = sys._getframe().f_code.co_name  #获取本函数名
    #     driver = self.driverWeb
    #     paramsIn = self.params_in
    #     checkPoint = self.checkPoint
    #     userName, password = self.ipadPbParameterDeal(paramsIn)
    #
    #     self.ipadPbLoginOK(driver, userName, password, self.url)
    #
    #     self.ipadAutomaticOK(driver, paramsIn, checkPoint)


    def testIpadLoginOK(self):
        """用例：ipad登录成功"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        # self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        # self.mySysParameterValueReplaceJson(paramsIn, 'password')
        # userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)


    def testIpadLoginPasswordError(self):
        """用例：ipad登录失败"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginPasswordError(driver, userName, password, self.url)


    def testIpadWuLiuZhuiZongOK(self):
        """用例：物流追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadWuLiuZhuiZongOK(driver, paramsIn, checkPoint)


    def testIpadDanJiOK(self):
        """用例：蛋鸡"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadDanJiOK(driver, paramsIn, checkPoint)


    def testIpadRouJiOK(self):
        """用例：肉鸡"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadRouJiOK(driver, paramsIn, checkPoint)


    def testIpadShengXiaOK(self):
        """用例：生虾"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadShengXiaOK(driver, paramsIn, checkPoint)


    def testIpadHunTunOK(self):
        """用例：馄饨"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadHunTunOK(driver, paramsIn, checkPoint)


    def testIpadNiuRouOK(self):
        """用例：牛肉"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadPbLoginOK(driver, userName, password, self.url)

        self.ipadNiuRouOK(driver, paramsIn, checkPoint)


