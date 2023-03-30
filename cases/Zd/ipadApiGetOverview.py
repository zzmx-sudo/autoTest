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
fileName = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0]
mybatisFile = fileName + '.xml'


class IpadApiGetOverview(PublicOperation):
    """API蛋鸡指标面板"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadApiGetOverview, self).__init__(methodName, AllPirParams)


    def ipadApiGetOverviewOK(self, paramsIn, checkPoint):
        """"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        apiname = "custom-zd/app/eggchicken/getOverview"
        apiInfo = self.paramsApi[apiname]
        requestMethod = apiInfo["requestMethod"]
        queryString = apiInfo["queryString"]
        datas = apiInfo["datas"]
        jsonsTmp = apiInfo["jsons"]
        pathTmp = apiInfo["path"]
        url = '{}{}{}'.format(self.url, apiname, queryString)
        jsons = self.myPbEvalStr(self.myPbEvalStr(str(jsonsTmp)).format('2022-05', 'Y'))
        result = self.myApi(url, requestMethod, datas, jsons)
        actualValue = result[pathTmp]
        logger.debug(result)
        logger.debug(result[pathTmp])

        params = {
            'paDate': '2022-05',
            'dateType': 'Y'
        }
        sql = self.myPbMybatis(mybatisFile, 'getRegionOverview', params)
        fetchall, listDictResult = self.myPbOracleExecute(sql)
        self.myPbOracleValueDictCheck(actualValue, mybatisFile, 'getRegionOverview', params)


