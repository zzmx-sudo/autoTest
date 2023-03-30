# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
import basic.myGlobal as myGlobal
from cases.Zd.dapingJiWang import DapingJiWang
from cases.Zd.dapingPingGuDanYe import DapingPingGuDanYe
from cases.Zd.dapingZhuChanYeLian import DapingZhuChanYeLian
from cases.Zd.dapingZhuWangZhanLue import DapingZhuWangZhanLue
from cases.Zd.dapingYouXianShiYe import DapingYouXianShiYe
from cases.Zd.dapingTaiGuoZhanFang import DapingTaiGuoZhanFang
from cases.Zd.dapingShuiChanShiYe import DapingShuiChanShiYe
from cases.Zd.dapingZhuChanYeShiJingJianKong import DapingZhuChanYeShiJingJianKong
from cases.Zd.dapingCTIZhuiZong import DapingCTIZhuiZong
from cases.Zd.dapingCTIZhuZhuiZong import DapingCTIZhuZhuiZong
from cases.Zd.dapingCTISiLiaoZhuiZong import DapingCTISiLiaoZhuiZong
from cases.Zd.dapingNonɡMuZhongGuoQu import DapingNongMuZhongGuoQu
from cases.Zd.dapingDanJiShiYe import DapingDanJiShiYe
from cases.Zd.dapingLianHuaShiYe import DapingLianHuaShiYe
from cases.Zd.dapingXianDaiShiPin import DapingXianDaiShiPin
from cases.Zd.dapingJiShiPinZhuiZong import DapingJiShiPinZhuiZong
from cases.Zd.dapingSiLiao import DapingSiLiao
from cases.Zd.daping100DaoCai import Daping100DaoCai
from cases.Zd.dapingQuanQiuMaiQuanQiuMai import DapingQuanQiuMaiQuanQiuMai
from cases.Zd.dapingYuShiFenXi import DapingYuShiFenXi
from cases.Zd.dapingQinShiYe import DapingQinShiYe



logger = myGlobal.getLogger()


class CommDaping(DapingJiWang, DapingPingGuDanYe, DapingZhuChanYeLian, DapingZhuWangZhanLue, DapingYouXianShiYe, DapingTaiGuoZhanFang, DapingShuiChanShiYe, DapingZhuChanYeShiJingJianKong, DapingCTIZhuiZong, DapingCTIZhuZhuiZong, DapingCTISiLiaoZhuiZong, DapingNongMuZhongGuoQu, DapingDanJiShiYe, DapingLianHuaShiYe, DapingXianDaiShiPin, DapingJiShiPinZhuiZong, DapingSiLiao, Daping100DaoCai, DapingQuanQiuMaiQuanQiuMai, DapingYuShiFenXi, DapingQinShiYe):
    """战房大屏-web"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(CommDaping, self).__init__(methodName, AllPirParams)


    def testDapingLoginOK(self):
        """用例：登录大屏成功"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        # self.mySysParameterValueReplaceJson(paramsIn, 'userName')
        # self.mySysParameterValueReplaceJson(paramsIn, 'password')
        # userName, password = self.mySysParameterLoginEx(paramsIn, 'DapingUserAdminID', 'DapingUserAdminPassword')
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)


    def testDapingLoginPasswordError(self):
        """用例：登录大屏失败"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginPasswordError(driver, userName, password, self.url)


    # def testDapingAllOK(self):
    #     """用例：大屏管理菜单中大屏冒烟"""
    #     # caseName = sys._getframe().f_code.co_name  #获取本函数名
    #     driver = self.driverWeb
    #     paramsIn = self.params_in
    #     checkPoint = self.checkPoint
    #     userName, password = self.dapingPbParameterDeal(paramsIn)
    #
    #     self.dapingPbLoginOK(driver, userName, password, self.url)
    #
    #     self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)


    def testDapingJiWangOK(self):
        """用例：鸡王"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '鸡王'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingJiWangOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingPingGuDanYeOK(self):
        """用例：平谷蛋业"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '平谷蛋业'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingPingGuDanYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingZhuChanYeLianOK(self):
        """用例：猪产业链"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '猪产业链'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingZhuChanYeLianOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingZhuWangZhanLueOK(self):
        """用例：猪王战略"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '猪王战略'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingZhuWangZhanLueOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingYouXianShiYeOK(self):
        """用例：优鲜事业"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '优鲜事业'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingYouXianShiYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingTaiGuoZhanFangOK(self):
        """用例：泰国战房"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '泰国战房'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingTaiGuoZhanFangOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingShuiChanShiYeOK(self):
        """用例：水产事业"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '水产事业'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingShuiChanShiYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingZhuChanYeShiJingJianKongOK(self):
        """用例：猪产业实景监控"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '猪产业实景监控'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingZhuChanYeShiJingJianKongOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingCTIZhuiZongOK(self):
        """用例：CTI追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = 'CTI追踪'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingCTIZhuiZongOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingCTIZhuZhuiZongOK(self):
        """用例：CTI猪追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = 'CTI猪追踪'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingCTIZhuZhuiZongOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingCTISiLiaoZhuiZongOK(self):
        """用例：CTI饲料追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = 'CTI饲料追踪'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingCTISiLiaoZhuiZongOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingNongMuZhongGuoQuOK(self):
        """用例：农牧中国区"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '农牧中国区'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingNongMuZhongGuoQuOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingDanJiShiYeOK(self):
        """用例：蛋鸡事业"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '蛋鸡事业'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingDanJiShiYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingLianHuaShiYeOK(self):
        """用例：莲花事业"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '莲花事业'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingLianHuaShiYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingXianDaiShiPinOK(self):
        """用例：现代食品"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '现代食品'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingXianDaiShiPinOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingJiShiPinZhuiZongOK(self):
        """用例：鸡食品追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '鸡食品追踪'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingJiShiPinZhuiZongOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingSiLiaoOK(self):
        """用例：饲料"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '饲料'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingSiLiaoOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDaping100DaoCaiOK(self):
        """用例：100道菜"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '100道菜'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.daping100DaoCaiOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingQuanQiuMaiQuanQiuMaiOK(self):
        """用例：全球买全球卖战略追踪"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '全球买全球卖战略追踪'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingQuanQiuMaiQuanQiuMaiOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingYuShiFenXiOK(self):
        """用例：预实分析"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        if '中国区预实利润' in self.myWtFindElement(driver, By.TAG_NAME, 'body').text:
            paramsIn['daPingTitleExpect'] = '中国区预实利润'
        else:
            paramsIn['daPingTitleExpect'] = '预实分析-开发版'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingYuShiFenXiOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


    def testDapingQinShiYeOK(self):
        """用例：禽事业改革-产业链"""
        # caseName = sys._getframe().f_code.co_name  #获取本函数名
        driver = self.driverWeb
        paramsIn = self.params_in
        checkPoint = self.checkPoint
        userName, password = self.dapingPbParameterDeal(paramsIn)

        self.dapingPbLoginOK(driver, userName, password, self.url)

        paramsIn['daPingTitleExpect'] = '禽事业改革-产业链-V1.0'
        self.dapingPbGuanliMaoyangBegin(driver, paramsIn, checkPoint)

        self.dapingQinShiYeOK(driver, paramsIn, checkPoint)

        self.dapingPbGuanliMaoyangEnd(driver, paramsIn, checkPoint)


