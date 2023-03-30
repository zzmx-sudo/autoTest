# -*- coding:utf-8 -*-
import sys
import os
import time,random
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from cases.Zd.publicOperation import PublicOperation
import basic.myGlobal

logger = basic.myGlobal.getLogger()


class IpadApiGetChannelChinaAreaInfo(PublicOperation):
    """API进口水果渠道"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadApiGetChannelChinaAreaInfo, self).__init__(methodName, AllPirParams)


    def ipadApiGetChannelChinaAreaInfoOK(self, paramsIn, checkPoint):
        """API GetChannelChinaAreaInfo"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        apiname = "custom-zd/app/cm/fruit/pad/getChannelChinaAreaInfo"
        apiInfo = self.paramsApi[apiname]
        requestMethod = apiInfo["requestMethod"]
        queryString = apiInfo["queryString"]
        datas = apiInfo["datas"]
        jsons = apiInfo["jsons"]
        pathTmp = apiInfo["path"]
        urlTmp = '{}{}{}'.format(self.url, apiname, queryString)
        url = str(urlTmp).format('2021-11-23', 'LONGAN', 'salamt', 'desc', 'CNY', 'zh-CN')
        result = self.myApi(url, requestMethod, datas, jsons)
        logger.debug(result)
        logger.debug(result[pathTmp])


