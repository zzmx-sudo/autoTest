# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
import basic.myGlobal as myGlobal
# from cases.Zd.ipadAutomatic import IpadAutomatic
from cases.Zd.ipadApiGetChannelChinaAreaInfo import IpadApiGetChannelChinaAreaInfo
from cases.Zd.ipadApiGetOverview import IpadApiGetOverview





logger = myGlobal.getLogger()


class CommApi(IpadApiGetChannelChinaAreaInfo, IpadApiGetOverview):
    """战房ipad-API"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(CommApi, self).__init__(methodName, AllPirParams)

        self.myGetWebApiToken()


    # def testIpadApiGetWebToken(self):
    #     self.myGetWebToken()


    def testIpadApiGetChannelChinaAreaInfoOK(self):
        """用例：API GetChannelChinaAreaInfo"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        # self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        # self.mySysParameterValueReplaceJson(paramsIn, 'password')
        # userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadApiGetChannelChinaAreaInfoOK(paramsIn, checkPoint)


    def testIpadApiGetOverviewOK(self):
        """用例：API GetOverview"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        # self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        # self.mySysParameterValueReplaceJson(paramsIn, 'password')
        # userName, password = self.mySysParameterLoginEx(paramsIn, 'IpadUserAdminID', 'IpadUserAdminPassword')
        userName, password = self.ipadPbParameterDeal(paramsIn)

        self.ipadApiGetOverviewOK(paramsIn, checkPoint)



