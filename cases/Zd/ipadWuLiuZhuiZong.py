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
# mybatisFile = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0] + '.xml'
fileName = re.findall(r'[\.\\]?(\w+)\.py$', __file__)[0]
mybatisFile = fileName + '.xml'


class IpadWuLiuZhuiZong(PublicOperation):
    """物流追踪"""
    def __init__(self, methodName='runTest', AllPirParams={}):
        super(IpadWuLiuZhuiZong, self).__init__(methodName, AllPirParams)


    def ipadWuLiuZhuiZongOK(self, driver, paramsIn, checkPoint):
        """物流追踪"""
#        caseName = sys._getframe().f_code.co_name  #获取本函数名
        menuStr1 = self.ipadLeftMenu[0]
        menuStr2 = self.ipadShouYeMenu[9]
        self.ipadPbSelectMainMenu(driver, menuStr1=menuStr1, menuStr2=menuStr2)

        uiPath = '{}-{}'.format(menuStr1, menuStr2)
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPath, tagList=['div', 'span'])

        # 中国港口、中转仓、卜蜂进出口一级库、SVC冷库、门店
        classList = ['gangkou', 'cang', 'imgC']
        for cla in classList:
            eltList = self.myWtFindElements(driver, By.XPATH, "//img[contains(@class, '{}')]/..".format(cla))
            for elt in eltList:
                son = self.myWtFindElement(elt, By.XPATH, ".//img[contains(@class, '{}')]".format(cla))
                eltclass = elt.get_attribute("class")
                logger.debug('{} {}'.format(cla, eltclass))
                if 'box_gary' in eltclass:
                    continue
                self.myWtClick(son, 0, 0.5)
                self.ipadWuliuCangku(driver, paramsIn, checkPoint, uiPath)

        # 点击小车，进入订单列表（采购单，调拨单、销售单）
        srcList = ['./dayunshuche.135c9ab.png']
        for src in srcList:
            eltList = self.myWtFindElements(driver, By.XPATH, "//img[contains(@src, '{}')]".format(src))
            for elt in eltList:
                self.myWtClick(elt, 0, 0.5)
                self.ipadWuliuOrder(driver, paramsIn, checkPoint, uiPath)

        self.ipadPbLeftBack(driver)


    def ipadWuliuCangku(self, driver, paramsIn, checkPoint, uiPath):
        """中国港口、中转仓、卜蜂进出口一级库、SVC冷库"""
        self.ipadPbRefreshWaiting(driver)

        # 检查
        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '名称:')]")
        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '位置:')]")
        title = self.myWtFindElement(driver, By.XPATH, "//span[contains(@class, 'title')]")  # 获取左上角标题
        text = str(title.text)
        paramsIn['title'] = text
        logger.debug('当前窗口：{}'.format(text))

        # 单击下拉框
        right1_t = 'right1_t'
        self.myWtClickEx(driver, By.CLASS_NAME, right1_t)
        time.sleep(1)

        if ("中国港口" in text) or ("中转仓" in text) or ("卜蜂进出口一级库" in text) or ("SVC冷库" in text):
            wrapper = self.myWtFindElement(driver, By.CLASS_NAME, 'wrapper')
            itemList = self.myWtFindElements(wrapper, By.CLASS_NAME, 'item')
            itemListNum = len(itemList)
            logger.debug('下拉框选项个数：{}'.format(itemListNum))
            if itemListNum >= 1:
                num = 1
                for item in itemList:
                    if num <= 2:
                        if num >= 2:
                            self.myWtClickEx(driver, By.CLASS_NAME, right1_t)
                            time.sleep(1)
                        itemText = item.text
                        self.myWtClick(item)
                        time.sleep(1)
                        logger.debug('当前下拉框选项{}：{}'.format(num, itemText))
                        self.ipadWuliuCangkuCheck(driver, paramsIn, checkPoint, uiPath)
                    num = num + 1
                    if num == 3:
                        break
            else:
                logger.debug('下拉框选项为空')
        elif "门店" in text:
            list2 = self.myWtFindElement(driver, By.CLASS_NAME, 'list2')
            itemList = self.myWtFindElements(list2, By.CLASS_NAME, 'store')
            itemListNum = len(itemList)
            logger.debug('下拉框选项个数：{}'.format(itemListNum))
            if itemListNum >= 1:
                num = 1
                for item in itemList:
                    if num <= 2:
                        itemText = ''
                        if num >= 2:
                            self.myWtClickEx(driver, By.CLASS_NAME, right1_t)
                            time.sleep(1)
                            itemText = item.text
                            self.myWtClick(item)
                            time.sleep(1)
                        else:
                            itemText = item.text
                            driver.execute_script("document.querySelector('.{}').click()".format(right1_t))
                            time.sleep(1)
                        logger.debug('当前下拉框选项{}：{}'.format(num, itemText))
                        self.ipadWuliuMendianCheck(driver, paramsIn, checkPoint, uiPath)
                    num = num + 1
                    if num == 3:
                        break
            else:
                logger.debug('下拉框选项为空')

        self.ipadPbLeftBack(driver)


    def ipadWuliuCangkuCheck(self, driver, paramsIn, checkPoint, uiPath):
        """中国港口、中转仓、卜蜂进出口一级库、SVC冷库检查"""
        # 检查当前温度颜色
        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '当前值：')]")
        elt = self.myWtFindElement(driver, By.CLASS_NAME, 'right3')
        temp = elt.text
        temperature = re.findall(r'当前值：(.*?)°C', temp)[0]
        logger.debug(temperature)
        if temperature != '-':
            logger.debug(temperature)
            paramsIn['currentTemperature'] = temperature
            self.ipadWuliuCheckTemperature(elt, float(temperature))
        else:
            paramsIn['currentTemperature'] = '-'
            logger.debug('显示原色：{}'.format(temperature))

        self.ipadWuliuCangkuMendianCheck(driver, paramsIn, checkPoint, uiPath)


    def ipadWuliuMendianCheck(self, driver, paramsIn, checkPoint, uiPath):
        """门店检查"""
        # 检查当前温度颜色
        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '当前值')]")
        eltList = self.myWtFindElements(driver, By.CLASS_NAME, 'chartrow')
        paramsIn['currentTemperature'] = {}
        for elt in eltList:
            eltTemp = self.myWtFindElement(elt, By.CLASS_NAME, 'temp')
            eltName = self.myWtFindElement(elt, By.CLASS_NAME, 'name')
            temp = eltTemp.text
            name = eltName.text
            temperature = temp.replace('℃', '')
            logger.debug(temperature)
            if temperature != '-':
                temperatureFloat = float(temperature)
                logger.debug(temperature)
                paramsIn['currentTemperature']['{}'.format(format(name))] = temperature
                # 不区分颜色
                # self.ipadWuliuCheckTemperature(eltTemp, temperatureFloat)
            else:
                paramsIn['currentTemperature']['{}'.format(format(name))] = '-'
                logger.debug('显示原色：{}'.format(temperature))

        self.ipadWuliuCangkuMendianCheck(driver, paramsIn, checkPoint, uiPath)


    def ipadWuliuCangkuMendianCheck(self, driver, paramsIn, checkPoint, uiPath):
        """中国港口、中转仓、卜蜂进出口一级库、SVC冷库检查"""
        # 检查
        text = paramsIn['title']
        maincontent = self.myWtFindElements(driver, By.CLASS_NAME, "van-sticky")
        if maincontent is not None:
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, '{}-{}(列表标题)'.format(uiPath, text), maincontent, tagList=['span'])

        maincontent = self.myWtFindElements(driver, By.CLASS_NAME, "van-list")
        if maincontent is not None:
            # self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, '{}-{}(列表内容)'.format(uiPath, text), maincontent, By.CLASS_NAME, 'itemBox', tagList=['div'])
            self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, '{}-{}(列表内容)'.format(uiPath, text), maincontent, By.CLASS_NAME, 'itemBox', By.TAG_NAME, 'div', tagList=[])

        # 界面数据与数据库对比
        self.ipadWuliuCangkuDBCheck(driver, paramsIn, checkPoint)


    def ipadWuliuCangkuDBCheck(self, driver, paramsIn, checkPoint):
        """界面数据与数据库对比(中国港口、中转仓、卜蜂进出口一级库、SVC冷库)"""
        # 左上角，港口名称、港口位置检查
        text = paramsIn['title']
        cangkuName = None
        city = None
        right1_t = self.myWtFindElement(driver, By.CLASS_NAME, 'right1_t')
        if "门店" in text:
            cangkuName = right1_t.text.split('-')[1]
            city = right1_t.text.split('-')[0]
        else:
            cangkuName = right1_t.text
        params = {
            'wareName': cangkuName,
            'storeRegion': city,
            'storeName': cangkuName
        }
        sql = self.myPbMybatis(mybatisFile, 'getBasicWareInfoList', params)
        fetchall, listDictResult = self.myPbOracleExecute(sql)
        if fetchall is None:
            return
        wareCode = None
        type = None
        logger.debug(fetchall)
        for fetch in fetchall:
            logger.debug(fetch)
            wareCode = fetch[2]
            type = fetch[3]
            break

        if "门店" in text:
            info = self.myWtFindElement(driver, By.CLASS_NAME, 'info')
            # 仓库名称
            name = self.myWtFindElement(info, By.CLASS_NAME, 'name').text
            logger.debug(name)
            # 仓库位置
            addr = self.myWtFindElement(info, By.CLASS_NAME, 'loc').text
            logger.debug(addr)

            actualValue = {
                1: name,
                2: addr
            }
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'loadStoreDetail', params)

            # 当前温度
            for current in paramsIn['currentTemperature']:
                temperature = paramsIn['currentTemperature'][current]
                actualValue = {
                    1: temperature
                }
                params['rownum'] = 'max'
                params['iceCode'] = current
                logger.debug('当前{}温度:{}℃'.format(current, temperature))
                self.myPbOracleValueListCheck(actualValue, mybatisFile, 'loadStoreTemp', params)
        else:
            div1 = self.myWtFindElement(driver, By.CLASS_NAME, 'div1')
            # 仓库名称
            nameTmp = self.myWtFindElement(div1, By.CLASS_NAME, 'name').text
            logger.debug(nameTmp)
            # name = re.findall(r'\: (\w+)$', nameTmp)[0]
            name = nameTmp.split(': ')[1]
            # 仓库位置
            addr = self.myWtFindElement(div1, By.CLASS_NAME, 'addr').text
            logger.debug(addr)

            actualValue = {
                1: name,
                2: addr
            }
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'getBasicWareInfoList', params)

            # 当前温度
            temperature = paramsIn['currentTemperature']
            actualValue = {
                1: temperature
            }
            params['rownum'] = 'max'
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'getTwentyFourTemp', params)



        # 最下方，列表数据检查
        params = {
            'type': type,
            'wareCode': wareCode,
            'storeRegion': city,
            'storeName': cangkuName
        }
        if ("中国港口" in text) or ("中转仓" in text):
            actualValue = {'tabList': []}
            itemBoxList = self.myWtFindElements(driver, By.CLASS_NAME, 'itemBox')
            for itemBox in itemBoxList:
                c1 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c1').text
                c2 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c2').text
                c3 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c3').text
                c4 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c4').text
                c5 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c5').text
                listtmp = [c1, c2, c3, c4, c5]
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'getWDGkDown', params)
        elif ("卜蜂进出口一级库" in text):
            actualValue = {'tabList': []}
            itemBoxList = self.myWtFindElements(driver, By.CLASS_NAME, 'itemBox')
            for itemBox in itemBoxList:
                c2 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c2').text
                c3 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c3').text
                listtmp = [c2, c3]
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'getWDSvcDown', params)
        elif ("SVC冷库" in text):
            actualValue = {'tabList': []}
            itemBoxList = self.myWtFindElements(driver, By.CLASS_NAME, 'itemBox')
            for itemBox in itemBoxList:
                c2 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c2').text
                c3 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c3').text
                c4 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c4').text
                c5 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c5').text
                listtmp = [c2, c3, c4, c5]
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'getWDSvcDown', params)
        elif "门店" in text:
            actualValue = {'tabList': []}
            itemBoxList = self.myWtFindElements(driver, By.CLASS_NAME, 'itemBox')
            for itemBox in itemBoxList:
                c2 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c2').text
                c3 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c3').text
                c4 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c4').text
                c5 = self.myWtFindElement(itemBox, By.CLASS_NAME, 'c5').text
                listtmp = [c2, c3, c4, c5]
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueListCheck(actualValue, mybatisFile, 'loadGoods', params)
        else:
            self.mySysAssert("没有对应的类型")


    def ipadWuliuOrder(self, driver, paramsIn, checkPoint, uiPath):
        """订单列表（采购单，调拨单、销售单）"""
        self.ipadPbRefreshWaiting(driver)
        # 检查
        self.myWtFindElement(driver, By.XPATH, "//div[contains(text(), '状态')]")
        vantabactive = None
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'spanTitle', 0, 0.5) is None:
            vantabactive = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'van-tab--active')]")
        else:
            vantabactive = self.myWtFindElement(driver, By.CLASS_NAME, 'spanTitle')
        orderType = vantabactive.text
        paramsIn['orderType'] = orderType
        # logger.debug(orderType)

        uiPathT = '{}-{}'.format(uiPath, orderType)
        list = self.myWtFindElement(driver, By.CLASS_NAME, "list")
        maincontent = self.myWtFindElements(list, By.CLASS_NAME, "head")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(列表标题)', maincontent, tagList=['div'])

        maincontent = self.myWtFindElements(list, By.CLASS_NAME, "content")
        self.ipadPbGetCheckTextSize(driver, paramsIn, checkPoint, uiPathT+'(列表内容)', maincontent, By.CLASS_NAME, 'rowboy', By.CLASS_NAME, 'boy', tagList=['div'])

        # 界面数据与数据库对比
        self.ipadWuliuOrderDBCheck(driver, paramsIn, checkPoint)

        # vanList = self.myWtFindElements(driver, By.XPATH, "//div[contains(@class, 'van-list')]")
        # for van in vanList:
        van = self.myWtFindElement(driver, By.XPATH, "//div[contains(@class, 'van-list')]")
        if van is not None:
            rowList = self.myWtFindElements(van, By.XPATH, ".//div[contains(@class, 'rowboy')]")
            for elt in rowList:
                text = elt.text
                if '已审核' not in text and '已调度' not in text:
                    self.myWtClick(elt, 0, 0.5)
                    self.ipadWuliuOrderWuliu(driver, paramsIn, checkPoint, uiPathT)

                    if self.tabClickNumOfTimes == 1:
                        break

        self.ipadPbLeftBack(driver)


    def ipadWuliuOrderDBCheck(self, driver, paramsIn, checkPoint):
        """界面数据与数据库对比，订单列表（采购单，调拨单、销售单）数据"""
        orderType = paramsIn['orderType']
        mid = self.myWtFindElement(driver, By.CLASS_NAME, 'mid')
        spanList = self.myWtFindElements(mid, By.TAG_NAME, 'span')
        spanNum = 1
        beginDate = None
        endDate = None
        for span in spanList:
            if spanNum == 1:
                beginDate = span.text.replace(" ", "")
            elif spanNum == 3:
                endDate = span.text.replace(" ", "")
            spanNum = spanNum + 1

        params = {
            'beginDate': beginDate,
            'endDate': endDate
        }
        if orderType == "采购单":
            params['type'] = "采购单"
            actualValue = {'tabList': []}
            rowboyList = self.myWtFindElements(driver, By.CLASS_NAME, 'rowboy')
            for rowboy in rowboyList:
                boyList = self.myWtFindElements(rowboy, By.CLASS_NAME, 'boy')
                listtmp = {}
                boyNum = 1
                for boy in boyList:
                    if boyNum == 1:
                        listtmp['ORDER_STATUS_NAME'] = boy.text
                    elif boyNum == 2:
                        listtmp['ORDER_NO'] = boy.text
                    elif boyNum == 3:
                        listtmp['ORDER_DATE'] = boy.text
                    elif boyNum == 4:
                        listtmp['GOODS'] = boy.text
                    elif boyNum == 5:
                        listtmp['QUANTITY'] = boy.text
                    elif boyNum == 6:
                        listtmp['PURCHASE_AMOUNT'] = boy.text
                    elif boyNum == 7:
                        listtmp['RECEIVER_SVC_NAME'] = boy.text
                    elif boyNum == 8:
                        listtmp['RECEIVER'] = boy.text
                    elif boyNum == 9:
                        listtmp['SUPPLIER'] = boy.text
                    boyNum = boyNum + 1
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueDictCheck(actualValue, mybatisFile, 'getSalesOrderList', params)

        elif orderType == "调拨单":
            params['type'] = "调拨单"
            actualValue = {'tabList': []}
            rowboyList = self.myWtFindElements(driver, By.CLASS_NAME, 'rowboy')
            for rowboy in rowboyList:
                boyList = self.myWtFindElements(rowboy, By.CLASS_NAME, 'boy')
                listtmp = {}
                boyNum = 1
                for boy in boyList:
                    if boyNum == 1:
                        listtmp['ORDER_STATUS_NAME'] = boy.text
                    elif boyNum == 2:
                        listtmp['ORDER_NO'] = boy.text
                    elif boyNum == 3:
                        listtmp['ORDER_DATE'] = boy.text
                    elif boyNum == 4:
                        listtmp['GOODS'] = boy.text
                    elif boyNum == 5:
                        listtmp['QUANTITY'] = boy.text
                    elif boyNum == 6:
                        listtmp['PURCHASE_AMOUNT'] = boy.text
                    elif boyNum == 7:
                        listtmp['SEND_SVC_NAME'] = boy.text
                    elif boyNum == 8:
                        listtmp['RECEIVER'] = boy.text
                    elif boyNum == 9:
                        listtmp['RECEIVER_SVC_NAME'] = boy.text
                    elif boyNum == 10:
                        listtmp['SUPPLIER'] = boy.text
                    boyNum = boyNum + 1
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueDictCheck(actualValue, mybatisFile, 'getSalesOrderList', params)

        elif orderType == "销售单":
            params['type'] = "调拨单"
            actualValue = {'tabList': []}
            rowboyList = self.myWtFindElements(driver, By.CLASS_NAME, 'rowboy')
            for rowboy in rowboyList:
                boyList = self.myWtFindElements(rowboy, By.CLASS_NAME, 'boy')
                listtmp = {}
                boyNum = 1
                for boy in boyList:
                    if boyNum == 1:
                        listtmp['ORDER_STATUS_NAME'] = boy.text
                    elif boyNum == 2:
                        listtmp['ORDER_NO'] = boy.text
                    elif boyNum == 3:
                        listtmp['ORDER_DATE'] = boy.text
                    elif boyNum == 4:
                        listtmp['GOODS'] = boy.text
                    elif boyNum == 5:
                        listtmp['QUANTITY'] = boy.text
                    elif boyNum == 6:
                        listtmp['PURCHASE_AMOUNT'] = boy.text
                    elif boyNum == 7:
                        listtmp['RECEIVER'] = boy.text
                    elif boyNum == 8:
                        listtmp['RECEIVER_SVC_CODE'] = boy.text
                    elif boyNum == 9:
                        listtmp['SUPPLIER'] = boy.text
                    boyNum = boyNum + 1
                actualValue['tabList'].append(listtmp)
            self.myPbOracleValueDictCheck(actualValue, mybatisFile, 'getSalesOrderList', params)


    def ipadWuliuOrderWuliu(self, driver, paramsIn, checkPoint, uiPath):
        """物流详情"""
        self.ipadPbRefreshWaiting(driver)
        # 检查
        orderType = paramsIn['orderType']
        if orderType == "采购单":
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '采购单号:')]")
        elif orderType == "调拨单":
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '调拨单号:')]")
        elif orderType == "销售单":
            self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '销售单号:')]")

        self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '出发地:')]")

        # 界面数据与数据库对比
        # 单号
        orderNoElt = self.myWtFindElement(driver, By.CLASS_NAME, 'orderNo')
        orderNo = self.mySysStringCleanup(orderNoElt.text.replace(" ", ""))
        # LOGISTICS_CODE
        logisticsCode = None
        if self.myWtEltNonexiContinue(driver, By.CLASS_NAME, 'van-cell__title') is not None:
            vancelltitleList = self.myWtFindElements(driver, By.CLASS_NAME, 'van-cell__title')
            for vancelltitle in vancelltitleList:
                pList = self.myWtFindElements(vancelltitle, By.TAG_NAME, 'p')
                for p in pList:
                    logisticsCode = p.text
                    break
                break
        # 车牌
        carNum = self.myWtFindElement(driver, By.CLASS_NAME, 'dataHead').text
        # 出发地:
        startAdd = self.myWtFindElement(driver, By.XPATH, "//span[contains(text(), '出发地:')]/following-sibling::span").text
        # 目的地:
        endAdd = self.myWtFindElement(driver, By.XPATH, '//span[contains(text(), "目的地:")]/following-sibling::span').text
        # 货物量:
        goods = self.myWtFindElement(driver, By.XPATH, '//span[contains(text(), "货物量:")]/following-sibling::span').text
        # 出发时间:
        startDate = self.myWtFindElement(driver, By.XPATH, '//span[contains(text(), "出发时间:")]/following-sibling::span').text
        # 完成时间:
        endDate = self.myWtFindElement(driver, By.XPATH, '//span[contains(text(), "完成时间:")]/following-sibling::span').text
        # 司机:
        driveName = self.myWtFindElement(driver, By.XPATH, '//span[contains(text(), "司机:")]/following-sibling::span').text
        params = {
            # 'carNum': carNum,
            # 'logisticsCode': logisticsCode,
            'ORDER_NO': orderNo
        }
        if carNum == '-' and '-; -' in startAdd and '-; -' in endAdd and '-kg; -' in goods and '-' in driveName:
            actualValue = {'tabList': []}
        else:
            actualValue = {'tabList': [{
                'carNum': carNum,
                'logisticsCode': logisticsCode,
                'startAdd': startAdd,
                'endAdd': endAdd,
                'goods': goods,
                'startDate': startDate,
                'endDate': endDate,
                'driveName': driveName
            }
                                       ]
                           }
        self.myPbOracleValueDictCheck(actualValue, mybatisFile, 'getDetails', params)

        self.ipadPbLeftBack(driver)


    def ipadWuliuCheckTemperature(self, elt, temperature):
        """物流温度数值（当前值）判断：＞标准值标红，≤标准值标绿，其他显示原色"""
        if temperature > -18:
            self.ipadPbCheckTextColor(elt)
        else:
            self.ipadPbCheckTextColor(elt, 'green')

