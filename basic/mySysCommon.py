# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.getcwd())
import time
import datetime
import random
import configparser
import basic.myGlobal as myGlobal
import traceback
import shutil
import json
import subprocess as sp
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from PIL import Image
import qrcode
import re
import urllib
from datetime import timedelta
import calendar
from io import StringIO
from io import open
import xlrd
import requests
import keyboard
import psutil
import threading
from multiprocessing import Process
import xml.dom.minidom
from xml.etree import ElementTree



import platform
platformSystem = platform.system()
if platformSystem == "Windows":
    import win32gui
    import win32con
    import win32api
    import win32print
    import win32clipboard
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, process_pdf
    import cx_Oracle
    from sshtunnel import SSHTunnelForwarder
    from win32clipboard import GetClipboardData, OpenClipboard, CloseClipboard, EmptyClipboard, SetClipboardData



VK_CODE = {
    'enter': 0x0D,
    'ctrl': 0x11,
    'v': 0x56
}


TIME_OUT = 8        #等待时长
POOL_FREQUENCY = 0.5    #检测时间间隔

logger = myGlobal.getLogger()





class myThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super(myThread, self).__init__()
        self.function = target
        self.args = args
        self.kwargs = kwargs
        self.exit_code = 0
        self.exception = None
        self.exc_traceback = ''


    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exit_code = 1
            self.exception = e
            self.exc_traceback = traceback.format_exc()


    def _run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception as e:
            raise e



class MySysCommon(object):
    def __init__(self):
        super(MySysCommon, self).__init__()
        self.maxNumberTimes = 3  # 最大重试次数
        self.maxWaittime = 20  # 最大等待时间（秒）


    def mySysAssert(self, text):
        """断言
        text：错误提示信息
        例：self.mySysAssert('没有找到数据')
        """
        # logger.error('{}： {}'.format(text, traceback.format_exc()))
        # assert 1 == 2, '{}： {}'.format(text, traceback.format_exc())
        logger.error('{}'.format(text))
        assert 1 == 2, '{}'.format(text)


    def mySysDialogOpenFile(self, filePathName):
        """打开windows文件对话框，选择文件
        filePathName:为包括目录的文件名
        例：self.mySysDialogOpenFile('C:\a.txt')
        """
        # time.sleep(2)
        dialog = 0
        d1 = datetime.datetime.now()
        while dialog == 0:
            dialog = win32gui.FindWindow(0, '打开')
            if self.mySysTimeGapSec(d1) >= self.maxWaittime:
                logger.debug('no open dialog')
                return None
            time.sleep(0.5)
        logger.debug(dialog)
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, str(filePathName))  # 往输入框输入绝对地址
        time.sleep(0.5)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
        logger.debug('文件：{}'.format(filePathName))
        time.sleep(2)


    ###############################
    """系统"""
    ###############################

    def mySysGetDatetime(self):
        """ 获得当前日期时间，返回格式 %Y-%m-%d %H:%M:%S """
        now = datetime.datetime.now()
        # 转换为指定的格式:
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    def mySysGetDate(self, year=0, day=0, hour=0, minute=0, second=0):
        """ 获得当前日期 ， 格式为%Y-%m-%d
        year：-1为减1年，1为加1年，其它同理，都为可选参数
        例：mySysGetDate()
        例：mySysGetDate(year=1, day=-2, hour=-3, minute=-4, second=-6)
        """
        now = datetime.datetime.now()
        if year != 0:
            return (now + relativedelta(years=year)).strftime("%Y-%m-%d")
        elif day != 0:
            return (now + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        elif hour != 0:
            return (now + datetime.timedelta(hours=hour)).strftime("%Y-%m-%d")
        elif minute != 0:
            return (now + datetime.timedelta(minutes=minute)).strftime("%Y-%m-%d")
        elif second != 0:
            return (now + datetime.timedelta(seconds=second)).strftime("%Y-%m-%d")
        else:
            # 转换为指定的格式:
            otherStyleTime = now.strftime("%Y-%m-%d")
            return otherStyleTime


    def mySysGetLocalTime(self):
        """ 获得当前日期时间，返回格式%Y%m%d_%H%M%S """
        now = datetime.datetime.now()
        timeStr = now.strftime("%Y%m%d_%H%M%S")
        return timeStr


    def mySysGetLocalMillisecond(self):
        """ 获得当前日期时间毫秒级，返回格式%Y%m%d_%H%M%S_%f """
        now = datetime.datetime.now()
        timeStr = now.strftime("%Y%m%d_%H%M%S_%f")
        return timeStr


    def mySysintTodatetime(self, intValue):
        """ 把参数intValue时间戳，转换并返回格式%Y-%m-%d %H:%M:%S.%f """
        if len(str(intValue)) == 10:
            # 精确到秒
            timeValue = time.localtime(intValue)
            tempDate = time.strftime("%Y-%m-%d %H:%M:%S", timeValue)
            datetimeValue = datetime.datetime.strptime(tempDate, "%Y-%m-%d %H:%M:%S")
        elif 10 < len(str(intValue)) and len(str(intValue)) < 15:
            # 精确到毫秒
            k = len(str(intValue)) - 10
            timetamp = datetime.datetime.fromtimestamp(intValue / (1 * 10 ** k))
            datetimeValue = timetamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            return -1
        return datetimeValue


    def mySysParameterLogin(self, paramsIn):
        """处理登录参数，取字典返回paramsIn['userName'], paramsIn['password']"""
        userName = paramsIn['userName']
        password = paramsIn['password']
        return userName, password


    def mySysParameterLoginEx(self, paramsIn, ParName, ParPassword, iFForce=0):
        """取登录参数值
        默认iFForce=0时，如果paramsIn['userName']和paramsIn['password']存在则取对应值，不存在则取paramsIn[ParName]和paramsIn[ParPassword]
        否则取paramsIn[ParName]和paramsIn[ParPassword]，并返回"""
        userName = ''
        password = ''
        userNameTmp = paramsIn[ParName]
        passwordTmp = paramsIn[ParPassword]
        if iFForce == 0:
            userName = self.mySysParameterDefault(paramsIn, 'userName', userNameTmp)
            password = self.mySysParameterDefault(paramsIn, 'password', passwordTmp)
        else:
            userName = userNameTmp
            password = passwordTmp
        return userName, password


    def mySysParameterAssignment(self, paramsIn, ParNameA, ParNameB):
        """参数赋值
        paramsIn[ParNameA] = paramsIn[ParNameB]"""
        paramsIn[ParNameA] = paramsIn[ParNameB]


    def mySysParameterValueReplaceJson(self, paramsIn, paramsKey):
        """参数值在json中查找，如果paramsKey存在，则paramsIn[paramsKey] = paramsIn[paramsIn[paramsKey]]"""
        if paramsKey in paramsIn:
            paramsValue = paramsIn[paramsKey]
            paramsIn[paramsKey] = paramsIn[paramsValue]


    def mySysParameterDefault(self, paramsIn, paramsKey, defaultValue):
        """处理默认参数，paramsKey存在，则返回paramsIn[paramsKey]，否则返回defaultValue"""
        if paramsKey in paramsIn:
            return paramsIn[paramsKey]
        else:
            return defaultValue


    def mySysParameterSplit(self, paramsIn, type):
        """拆分新旧参数"""
        myDict = {}
        if str(type) == "New":
            for ikey, value in paramsIn.items():
                if str(ikey[-3:]) == str(type):
                    myDict[ikey] = value
        else:
            for ikey, value in paramsIn.items():
                if str(ikey[-3:]) != "New":
                    myDict[ikey] = value
        logger.debug(myDict)
        return myDict


    def mySysParameterGetValue(self, paramsIn, paramsKey):
        """取参数值，paramsKey存在则返回str(paramsIn[paramsKey])，否则返回None"""
        if paramsKey in paramsIn:
            return str(paramsIn[paramsKey])
        else:
            return None


    def mySysParameterIfNew(self, paramsIn):
        """判断是否New参数"""
        for ikey in paramsIn.keys():
            if str(ikey[-3:]) == "New":
                return True
        return None


    def mySysGetRandChineseName(self):
        """随机生成中文姓名,返回"""
        firstNames = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '程', '褚', '卫', '蒋',
                      '韩', '杨', '商', '刘', '曾', '叶', '方', '牛', '马', '黄', '胡', '杜', '谢', '梁',
                      '徐', '邹', '陈', '邓', '龙', '涂', '夏', '桂', '苗']
        middleNames = ['万', '振', '有', '中', '国', '之', '凌', '德', '曼', '孺', '陆', '红', '泽',
                       '思', '晓', '子', '海', '大', '小', '文', '梦', '志', '梓', '紫']
        lastNames = ['华', '旭', '锋', '超', '强', '雪', '才', '露', '冰', '芬', '娟', '东', '荣', '棋',
                     '雨', '蕊', '芝', '丰', '里', '菲', '彤', '炎', '玲', '生', '军', '海', '靖', '凌', '平', '萍',
                     '晶', '鑫', '磊', '健', '伟']

        fistNameLen = len(firstNames)
        pos = random.randint(0, fistNameLen - 1)
        randFirstName = firstNames[pos]

        middleNameLen = len(middleNames)
        pos = random.randint(0, middleNameLen * 2)
        if pos > middleNameLen - 1:
            randMiddleName = ''
        else:
            randMiddleName = middleNames[pos]

        lastNameLen = len(lastNames)
        pos = random.randint(0, lastNameLen - 1)
        randLastName = lastNames[pos]

        name = '{}{}{}'.format(randFirstName, randMiddleName, randLastName)
        return name


    def mySysGetPhoneNum(self):
        """生成手机号，返回"""
        birthday = datetime.datetime.now() + datetime.timedelta(days=-10950)
        phoneNum = '1' + str(birthday.strftime("%Y%m%d%H%M"))[2:]
        return phoneNum


    def mySysGetPhoneRandomNum(self):
        """随机生成手机号,返回"""
        headNums = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '158', '180', '181',
                    '182', '189']
        randHead = headNums[random.randint(0, len(headNums) - 1)]
        num = '{}{:>04}{:>04}'.format(randHead, random.randint(0, 9999), random.randint(0, 9999))
        return num


    def mySysGetIdCardNum(self):
        """生成身份证，返回"""
        birthday = datetime.datetime.now() + datetime.timedelta(days=-10950)
        idNumber = '620981' + birthday.strftime("%Y%m%d%H%M")# + '8625'
        return idNumber


    def mySysGetIdCardRandomNum(self):
        """随机生成身份证号,返回"""
        fixedNum = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        IdDict = {0: 1, 1: 0, 2: 'X', 3: 9, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2}
        headList = [410883, 330382, 441882, 421127, 421182]

        head = headList[random.randint(0, len(headList) - 1)]
        tail = random.randint(100, 999)
        year = random.randint(1970, 1992)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        code = '{}{}{:02d}{:02d}{}'.format(head, year, month, day, tail)
        sumNum = 0
        for y, z in zip(code, fixedNum):
            sumNum += (int(y) * z)
        checkCode = sumNum % 11
        IdCode = '{}{}'.format(code, IdDict[checkCode])
        return IdCode


    def mySysCopyFile(self, oldFilename, newFilename):
        """函数说明：复制文件
        输入参数：老文件名，新文件名
        返回参数：True成功，None失败
        例：mySysCopyFile('C:\oldFilename', 'C:\newFilename')"""
        try:
            shutil.copy(oldFilename, newFilename)
            if os.path.isfile(newFilename):
                return True
            else:
                return None
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysMoveFile(self, oldFilename, newFilename):
        """函数说明：移动文件
        输入参数：老文件名，新文件名
        返回参数：True成功，None失败
        例：mySysMoveFile('C:\oldFilename', 'C:\newFilename')"""
        try:
            shutil.move(oldFilename, newFilename)
            if os.path.isfile(newFilename):
                return True
            else:
                return None
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysRemoveFile(self, filename):
        """函数说明：删除文件
        输入参数：文件名
        返回参数：True成功，None失败
        例：mySysRemoveFile('C:\ofilename')"""
        NumberTimes = 1
        while 1 == 1:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    logger.debug('删除文件：{}'.format(filename))
                    return True
                else:
                    logger.debug('不存在文件：{}'.format(filename))
                    return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                NumberTimes = NumberTimes + 1
                time.sleep(0.5)


    def mySysRemoveFileInDir(self, targetDir):
        """函数说明：删除一级目录中所有文件，不处理子目录
        输入参数：目录
        返回参数：无
        例：mySysRemoveFileInDir('E:\abc')"""
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)


    def mySysWriteFile(self, textStr, FileName='D:/order.txt'):
        """函数说明：写文件
        输入参数：写入文件的内容，文件名
        返回参数：无
        例：mySysWriteFile('顶号', 'E:\abc.txt')"""
        try:
            FileName = self.mySysProcessFileName(FileName)
            f = open(FileName, 'a', encoding='utf-8')
            tmpstr = textStr + "\n"
            f.write(tmpstr)
            f.close()
        except:
            logger.error(traceback.format_exc())
            return


    def mySysProcessFileName(self, fileName):
        """处理输入的文件名，返回处理后的文件名"""
        try:
            # fileName = fileName.replace(":", "")
            fileName = fileName.replace("*", "")
            fileName = fileName.replace("?", "")
            fileName = fileName.replace("\"", "")
            fileName = fileName.replace("<", "")
            fileName = fileName.replace(">", "")
            fileName = fileName.replace("|", "")
            fileName = fileName.replace(" ", "")
            fileName = fileName.replace("\r\n", "")
            fileName = fileName.replace("\r", "")
            fileName = fileName.replace("\n", "")
            return fileName
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysJsonLoad(self, FileName):
        """函数说明：读json文件
        输入参数：文件名
        返回参数：文件内容"""
        try:
            FileName = self.mySysProcessFileName(FileName)
            with open(FileName, 'r', encoding='UTF-8') as json_file:
                data = json.load(json_file)
                logger.debug('读取json文件：{}'.format(FileName))
                return data
        except:
            logger.error(traceback.format_exc())
            return


    def mySysJsonWrite(self, data, FileName):
        """函数说明：写json文件
        输入参数：FileName为文件名，data为写入文件的内容
        返回参数：无"""
        try:
            FileName = self.mySysProcessFileName(FileName)
            with open(FileName, 'w', encoding='UTF-8') as json_file:
                json_file.write(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            logger.error(traceback.format_exc())
            return


    def mySysStringCleanup(self, textStr):
        """函数说明：字符串清理，去除\r和\n
        输入参数：字符串
        返回参数：处理后的字符串"""
        textStr = textStr.strip()
        textStr = textStr.replace("\r\n", "")
        textStr = textStr.replace("\r", "")
        textStr = textStr.replace("\n", "")
        return textStr


    def mySysCloseProcess(self, processName):
        """ 杀进程
        processName为进程名"""
        try:
            os.system("taskkill /f /im " + processName)
        except:
            logger.error(traceback.format_exc())
            #return False


    def mySysProcessExist(self, processName):
        """ 查进程是否存在
        processName为进程名
        返回进程个数和pid列表
        """
        pl = psutil.pids()
        num = 0
        pidList = []
        for pid in pl:
            if psutil.Process(pid).name() == processName:
                num = num + 1
                pidList.append(pid)
        return num, pidList


    def mySysGetPathEachFile(self, filePath):
        """ 遍历指定目录，显示目录下的所有文件名 """
        return os.listdir(filePath)


    def mySysReadFileLines(self, fileName):
        """ 读取文件，返回内容 """
        try:
            if os.path.exists(fileName):
                f = open(fileName, 'r', encoding='utf-8')
                readLines = f.readlines()
                f.close()
                return readLines
            else:
                return ""
        except:
            return None


    def mySysDateDifference(self, startDate, endDate):
        """日期相减"""
        textStr = startDate.replace("\r\n", "")
        textStr = textStr.replace("\r", "")
        startDate = textStr.replace("\n", "")
        textStr = endDate.replace("\r\n", "")
        textStr = textStr.replace("\r", "")
        endDate = textStr.replace("\n", "")
        logger.debug("开始日期：{} 结果日期：{}".format(startDate, endDate))
        d1 = datetime.datetime.strptime(startDate.replace('/', '-'), '%Y-%m-%d')
        d2 = datetime.datetime.strptime(endDate.replace('/', '-'), '%Y-%m-%d')
        deleTmp = d2 - d1
        return deleTmp.days


    def mySysListAddLimit(self, list, newMember, maxNum):
        """列表添加成员
        maxNum为最大数量限制
        newMember为要添加的内容
        返回添加后的list"""
        if len(list) == maxNum:
            list.pop(0)
            list.append(newMember)
        else:
            list.append(newMember)
        return list


    def mySysTimeGapSec(self, d1):
        """计算时间差"""
        try:
            d2 = datetime.datetime.now()
            SleepTime = d2 - d1
            return SleepTime.seconds
        except:
            return False


    def mySysDownloadFile(self, urlStr, saveFilename):
        """网络下载文件
        urlStr为url
        saveFilename为保存文件名，例C:/a.txt"""
        NumberTimes = 1
        while 1 == 1:
            try:
                # savename = MyDownloadPath + UrlStr[UrlStr.rindex("/") + 1:]
                saveFilename = self.mySysProcessFileName(saveFilename)
                logger.debug(urlStr)
                if os.path.exists(saveFilename):
                    logger.debug("文件存在：{}".format(saveFilename))
                else:
                    conn = urllib.request.urlopen(urlStr)
                    f = open(saveFilename, 'wb')
                    f.write(conn.read())
                    f.close()
                    logger.debug("文件保存本地成功：{}".format(saveFilename))
                    time.sleep(0.5)
                return True
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysPing(self, ip):
        """ping ip
        如果丢包则返回None，正常返回True"""
        if platformSystem == "Windows":
            try:
                status, result = sp.getstatusoutput("ping " + ip + " -w 2000")
                # if "请求超时" in result or "传输中过期" in result or "无法访问目标主机" in result:
                if status != 0:
                    logger.info("ping {} packet loss".format(ip))
                    return None
                else:
                    logger.info("ping {} ok".format(ip))
                    return True
            except:
                logger.error('ping {} :{}'.format(ip, traceback.format_exc()))
                return None
        else:
            try:
                response = os.system("ping " + ip)
                if response == 0:
                    logger.info("ping {} ok".format(ip))
                    return True
                else:
                    logger.info("ping {} packet loss".format(ip))
                    return None
            except:
                logger.error('ping {} :{}'.format(ip, traceback.format_exc()))
                return None


    def mySysSendEmail(self, smtpserver="smtp.sohu.com", sender="ocean@sohu.com", username="ocean@sohu.com", password="123456", receivers=["jianghy003@qianhai.com.cn", "52@qq.com"], textSubject=None, textBody=None, attachmentList=None):
        """发邮件
        smtpserver为邮箱地址，如smtp.qq.com和smtp.sohu.com
        sender为邮件发送人
        username为邮件发送人用户
        password为密码
        receivers为收件人列表
        textSubject为邮件标题
        textBody为邮件内容
        attachmentList为邮件附件"""
        try:
            subject = "{}".format(textSubject)

            # 如名字所示： Multipart就是多个部分
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = sender
            msg['To'] = ','.join(receivers)

            # 下面是文字部分，也就是纯文本
            if textBody is not None:
                puretext = MIMEText(textBody)
                msg.attach(puretext)

            # 附件
            if attachmentList is not None:
                for attachment in attachmentList:
                    filePart = MIMEApplication(open(attachment, 'rb').read())
                    (filepath, tempfilename) = os.path.split(attachment)
                    filePart.add_header('Content-Disposition', 'attachment', filename=tempfilename)
                    msg.attach(filePart)

            #  下面开始真正的发送邮件了
            smtp = smtplib.SMTP(timeout=self.maxWaittime)
            smtp.connect(smtpserver)
            smtp.login(username, password)
            smtp.sendmail(sender, receivers, msg.as_string())
            smtp.quit()
            logger.info('邮件发送成功！')
            return True
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysImagePaste(self, toImage, fileName, loc):
        """图片指定位置替换
        toImage中，loc位置粘贴fileName
        loc = ((int(i/2) * 200), (i % 2) * 200)
        toImage = Image.new('RGBA',(400,400))
        http://www.py3study.com/Article/details/id/17157.html"""
        # img1 = Image.open("E:/Studio/python/Chenhui/log/2018-06-08.jpg")
        # img1 = img1.convert('RGBA')
        #
        # img2 = Image.open("E:/Studio/python/Chenhui/log/OA.jpg")
        # img2 = img2.convert('RGBA')
        #
        # img = Image.blend(img1, img2, 0.3)
        # img.show()
        # img.save("E:/Studio/python/Chenhui/log/aaa.jpg")

        fromImge = Image.open(fileName)
        toImage.paste(fromImge, loc)


    def mySysMakeQRCode(self, fileName, data, logo=None):
        """生成带logo的二维码图片"""
        # 参数配置
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,  # 25%的字码可被容错
            box_size=8,  # 二维码里每个格子的像素大小
            border=4  # 边框的格子厚度是多少（默认是4）
        )
        # img = qrcode.make(codeStr)
        # img.save(codeFileName)
        # 添加转换内容
        qr.add_data(data)
        #
        qr.make(fit=True)
        # 生成二维码
        img = qr.make_image()
        #
        img = img.convert("RGBA")

        # 添加logo
        if logo and os.path.exists(logo):
            icon = Image.open(logo)
            # 获取二维码图片的大小
            img_w, img_h = img.size

            factor = 4
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)

            # logo图片的大小不能超过二维码图片的1/4
            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
            # 详见：http://pillow.readthedocs.org/handbook/tutorial.html

            # 计算logo在二维码图中的位置
            w = int((img_w - icon_w) / 2)
            h = int((img_h - icon_h) / 2)
            icon = icon.convert("RGBA")
            img.paste(icon, (w, h), icon)
            # 详见：http://pillow.readthedocs.org/reference/Image.html#PIL.Image.Image.paste

        # 保存处理后图片
        img.save(fileName)
        # img.show()  # 显示二维码图片
        return img


    def mySysReadPdf(self, pdf):
        """读pdf文件，返回文件内容"""
        # resource manager
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        # device
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        process_pdf(rsrcmgr, device, pdf)
        device.close()
        content = retstr.getvalue()
        retstr.close()
        # 获取所有行
        lines = str(content).split("\n")
        return lines


    def mySysDatePmtAgt(self):
        """日期集合"""
        now = datetime.datetime.now()
        todayStr =  self.mySysGetDate()  # 今天
        yesterdayStr = self.mySysGetDate(day=-1)  # 昨天
        tomorrowStr = self.mySysGetDate(day=1)  # 明天
        # logger.debug("昨天{} 今天{} 明天{}".format(yesterdayStr, todayStr, tomorrowStr))

        # 本周第一天和最后一天
        this_week_start = now - timedelta(days=now.weekday())
        this_week_startStr = this_week_start.strftime("%Y-%m-%d")
        this_week_end = now + timedelta(days=6 - now.weekday())
        this_week_endStr = this_week_end.strftime("%Y-%m-%d")
        # logger.debug("本周第一天和最后一天{} {}".format(this_week_startStr, this_week_endStr))

        # 上周第一天和最后一天
        last_week_start = now - timedelta(days=now.weekday() + 7)
        last_week_startStr = last_week_start.strftime("%Y-%m-%d")
        last_week_end = now - timedelta(days=now.weekday() + 1)
        last_week_endStr = last_week_end.strftime("%Y-%m-%d")
        # logger.debug("上周第一天和最后一天{} {}".format(last_week_startStr, last_week_endStr))

        # 近八周第一天和最后一天
        last2_week_start = last_week_start - timedelta(days=7)
        last2_week_startStr = last2_week_start.strftime("%Y-%m-%d")
        last2_week_end = last_week_start - timedelta(days=1)
        last2_week_endStr = last2_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last2_week_startStr, last2_week_endStr))
        last3_week_start = last2_week_start - timedelta(days=7)
        last3_week_startStr = last3_week_start.strftime("%Y-%m-%d")
        last3_week_end = last2_week_start - timedelta(days=1)
        last3_week_endStr = last3_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last3_week_startStr, last3_week_endStr))
        last4_week_start = last3_week_start - timedelta(days=7)
        last4_week_startStr = last4_week_start.strftime("%Y-%m-%d")
        last4_week_end = last3_week_start - timedelta(days=1)
        last4_week_endStr = last4_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last4_week_startStr, last4_week_endStr))
        last5_week_start = last4_week_start - timedelta(days=7)
        last5_week_startStr = last5_week_start.strftime("%Y-%m-%d")
        last5_week_end = last4_week_start - timedelta(days=1)
        last5_week_endStr = last5_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last5_week_startStr, last5_week_endStr))
        last6_week_start = last5_week_start - timedelta(days=7)
        last6_week_startStr = last6_week_start.strftime("%Y-%m-%d")
        last6_week_end = last5_week_start - timedelta(days=1)
        last6_week_endStr = last6_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last6_week_startStr, last6_week_endStr))
        last7_week_start = last6_week_start - timedelta(days=7)
        last7_week_startStr = last7_week_start.strftime("%Y-%m-%d")
        last7_week_end = last6_week_start - timedelta(days=1)
        last7_week_endStr = last7_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last7_week_startStr, last7_week_endStr))
        last8_week_start = last7_week_start - timedelta(days=7)
        last8_week_startStr = last8_week_start.strftime("%Y-%m-%d")
        last8_week_end = last7_week_start - timedelta(days=1)
        last8_week_endStr = last8_week_end.strftime("%Y-%m-%d")
        # logger.debug("近八周第一天和最后一天{} {}".format(last8_week_startStr, last8_week_endStr))

        # 本月第一天和最后一天
        this_month_start = datetime.datetime(now.year, now.month, 1)
        this_month_startStr = this_month_start.strftime("%Y-%m-%d")
        # this_month_end = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=1)
        this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
        this_month_endStr = this_month_end.strftime("%Y-%m-%d")
        # logger.debug("本月第一天和最后一天{} {}".format(this_month_startStr, this_month_endStr))

        # 下月第一天
        next_month_start = this_month_end + timedelta(days=1)
        next_month_startStr = next_month_start.strftime("%Y-%m-%d")
        # logger.debug("下月第一天{}".format(next_month_startStr))

        # 上月第一天和最后一天
        last_month_end = this_month_start - timedelta(days=1)
        last_month_endStr = last_month_end.strftime("%Y-%m-%d")
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_startStr = last_month_start.strftime("%Y-%m-%d")
        # logger.debug("上月第一天和最后一天{} {}".format(last_month_startStr, last_month_endStr))

        # 前12个月第一天和最后一天
        last2_month_end = last_month_start - timedelta(days=1)
        last2_month_endStr = last2_month_end.strftime("%Y-%m-%d")
        last2_month_start = datetime.datetime(last2_month_end.year, last2_month_end.month, 1)
        last2_month_startStr = last2_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last2_month_startStr, last2_month_endStr))
        last3_month_end = last2_month_start - timedelta(days=1)
        last3_month_endStr = last3_month_end.strftime("%Y-%m-%d")
        last3_month_start = datetime.datetime(last3_month_end.year, last3_month_end.month, 1)
        last3_month_startStr = last3_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last3_month_startStr, last3_month_endStr))
        last4_month_end = last3_month_start - timedelta(days=1)
        last4_month_endStr = last4_month_end.strftime("%Y-%m-%d")
        last4_month_start = datetime.datetime(last4_month_end.year, last4_month_end.month, 1)
        last4_month_startStr = last4_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last4_month_startStr, last4_month_endStr))
        last5_month_end = last4_month_start - timedelta(days=1)
        last5_month_endStr = last5_month_end.strftime("%Y-%m-%d")
        last5_month_start = datetime.datetime(last5_month_end.year, last5_month_end.month, 1)
        last5_month_startStr = last5_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last5_month_startStr, last5_month_endStr))
        last6_month_end = last5_month_start - timedelta(days=1)
        last6_month_endStr = last6_month_end.strftime("%Y-%m-%d")
        last6_month_start = datetime.datetime(last6_month_end.year, last6_month_end.month, 1)
        last6_month_startStr = last6_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last6_month_startStr, last6_month_endStr))
        last7_month_end = last6_month_start - timedelta(days=1)
        last7_month_endStr = last7_month_end.strftime("%Y-%m-%d")
        last7_month_start = datetime.datetime(last7_month_end.year, last7_month_end.month, 1)
        last7_month_startStr = last7_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last7_month_startStr, last7_month_endStr))
        last8_month_end = last7_month_start - timedelta(days=1)
        last8_month_endStr = last8_month_end.strftime("%Y-%m-%d")
        last8_month_start = datetime.datetime(last8_month_end.year, last8_month_end.month, 1)
        last8_month_startStr = last8_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last8_month_startStr, last8_month_endStr))
        last9_month_end = last8_month_start - timedelta(days=1)
        last9_month_endStr = last9_month_end.strftime("%Y-%m-%d")
        last9_month_start = datetime.datetime(last9_month_end.year, last9_month_end.month, 1)
        last9_month_startStr = last9_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last9_month_startStr, last9_month_endStr))
        last10_month_end = last9_month_start - timedelta(days=1)
        last10_month_endStr = last10_month_end.strftime("%Y-%m-%d")
        last10_month_start = datetime.datetime(last10_month_end.year, last10_month_end.month, 1)
        last10_month_startStr = last10_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last10_month_startStr, last10_month_endStr))
        last11_month_end = last10_month_start - timedelta(days=1)
        last11_month_endStr = last11_month_end.strftime("%Y-%m-%d")
        last11_month_start = datetime.datetime(last11_month_end.year, last11_month_end.month, 1)
        last11_month_startStr = last11_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last11_month_startStr, last11_month_endStr))
        last12_month_end = last11_month_start - timedelta(days=1)
        last12_month_endStr = last12_month_end.strftime("%Y-%m-%d")
        last12_month_start = datetime.datetime(last12_month_end.year, last12_month_end.month, 1)
        last12_month_startStr = last12_month_start.strftime("%Y-%m-%d")
        # logger.debug("前12个月第一天和最后一天{} {}".format(last12_month_startStr, last12_month_endStr))

        this_year_start = datetime.datetime(now.year, 1, 1)  # 今年第一天
        this_year_startStr = this_year_start.strftime("%Y-%m-%d")
        this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)  # 今年最后一天
        this_year_endStr = this_year_end.strftime("%Y-%m-%d")
        # logger.debug("今年第一天{} 今年最后一天{}".format(this_year_startStr, this_year_endStr))

        last_year_end = this_year_start - timedelta(days=1)  # 去年最后一天
        last_year_endStr = last_year_end.strftime("%Y-%m-%d")
        last_year_start = datetime.datetime(last_year_end.year, 1, 1)  # 去年第一天
        last_year_startStr = last_year_start.strftime("%Y-%m-%d")
        # logger.debug("去年第一天{} 去年最后一天{}".format(last_year_startStr, last_year_endStr))

        next_year_start = datetime.datetime(now.year + 1, 1, 1)  # 明年第一天
        next_year_startStr = next_year_start.strftime("%Y-%m-%d")
        # logger.debug("明年第一天{}".format(next_year_startStr))

        Format = "%d-%02d-%02d"
        year = datetime.datetime.now().year
        i = 1
        p_thisyear_month01_start = Format % (year, i, 1)
        p_thisyear_month01_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 2
        p_thisyear_month02_start = Format % (year, i, 1)
        p_thisyear_month02_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 3
        p_thisyear_month03_start = Format % (year, i, 1)
        p_thisyear_month03_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 4
        p_thisyear_month04_start = Format % (year, i, 1)
        p_thisyear_month04_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 5
        p_thisyear_month05_start = Format % (year, i, 1)
        p_thisyear_month05_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 6
        p_thisyear_month06_start = Format % (year, i, 1)
        p_thisyear_month06_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 7
        p_thisyear_month07_start = Format % (year, i, 1)
        p_thisyear_month07_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 8
        p_thisyear_month08_start = Format % (year, i, 1)
        p_thisyear_month08_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 9
        p_thisyear_month09_start = Format % (year, i, 1)
        p_thisyear_month09_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 10
        p_thisyear_month10_start = Format % (year, i, 1)
        p_thisyear_month10_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 11
        p_thisyear_month11_start = Format % (year, i, 1)
        p_thisyear_month11_end = Format % (year, i, calendar.monthrange(year, i)[1])
        i = 12
        p_thisyear_month12_start = Format % (year, i, 1)
        p_thisyear_month12_end = Format % (year, i, calendar.monthrange(year, i)[1])

        dateDict = {
            "p_endDate": todayStr,
            "p_yesterday": yesterdayStr,
            "p_tomorrow": tomorrowStr,

            "p_this_week_start": this_week_startStr,
            "p_this_week_end": this_week_endStr,
            "p_last_week_start": last_week_startStr,
            "p_last_week_end": last_week_endStr,
            "p_last2_week_start": last2_week_startStr,
            "p_last3_week_end": last3_week_endStr,
            "p_last4_week_end": last4_week_endStr,
            "p_last5_week_end": last5_week_endStr,
            "p_last6_week_end": last6_week_endStr,
            "p_last7_week_end": last7_week_endStr,
            "p_last8_week_end": last8_week_endStr,

            "p_this_month_start": this_month_startStr,
            "p_this_month_end": this_month_endStr,
            "p_next_month_start": next_month_startStr,
            "p_last_month_end": last_month_endStr,
            "p_last_month_start": last_month_startStr,
            "p_last2_month_end": last2_month_endStr,
            "p_last2_month_start": last2_month_startStr,
            "p_last3_month_end": last3_month_endStr,
            "p_last3_month_start": last3_month_startStr,
            "p_last4_month_end": last4_month_endStr,
            "p_last4_month_start": last4_month_startStr,
            "p_last5_month_end": last5_month_endStr,
            "p_last5_month_start": last5_month_startStr,
            "p_last6_month_end": last6_month_endStr,
            "p_last6_month_start": last6_month_startStr,
            "p_last7_month_end": last7_month_endStr,
            "p_last7_month_start": last7_month_startStr,
            "p_last8_month_end": last8_month_endStr,
            "p_last8_month_start": last8_month_startStr,
            "p_last9_month_end": last9_month_endStr,
            "p_last9_month_start": last9_month_startStr,
            "p_last10_month_end": last10_month_endStr,
            "p_last10_month_start": last10_month_startStr,
            "p_last11_month_end": last11_month_endStr,
            "p_last11_month_start": last11_month_startStr,
            "p_last12_month_end": last12_month_endStr,
            "p_last12_month_start": last12_month_startStr,

            "p_thisyear_month01_start": p_thisyear_month01_start,
            "p_thisyear_month01_end": p_thisyear_month01_end,
            "p_thisyear_month02_start": p_thisyear_month02_start,
            "p_thisyear_month02_end": p_thisyear_month02_end,
            "p_thisyear_month03_start": p_thisyear_month03_start,
            "p_thisyear_month03_end": p_thisyear_month03_end,
            "p_thisyear_month04_start": p_thisyear_month04_start,
            "p_thisyear_month04_end": p_thisyear_month04_end,
            "p_thisyear_month05_start": p_thisyear_month05_start,
            "p_thisyear_month05_end": p_thisyear_month05_end,
            "p_thisyear_month06_start": p_thisyear_month06_start,
            "p_thisyear_month06_end": p_thisyear_month06_end,
            "p_thisyear_month07_start": p_thisyear_month07_start,
            "p_thisyear_month07_end": p_thisyear_month07_end,
            "p_thisyear_month08_start": p_thisyear_month08_start,
            "p_thisyear_month08_end": p_thisyear_month08_end,
            "p_thisyear_month09_start": p_thisyear_month09_start,
            "p_thisyear_month09_end": p_thisyear_month09_end,
            "p_thisyear_month10_start": p_thisyear_month10_start,
            "p_thisyear_month10_end": p_thisyear_month10_end,
            "p_thisyear_month11_start": p_thisyear_month11_start,
            "p_thisyear_month11_end": p_thisyear_month11_end,
            "p_thisyear_month12_start": p_thisyear_month12_start,
            "p_thisyear_month12_end": p_thisyear_month12_end,

            "p_this_year_start": this_year_startStr,
            "p_this_year_end": this_year_endStr,
            "p_last_year_end": last_year_endStr,
            "p_last_year_start": last_year_startStr,
            "p_next_year_start": next_year_startStr
        }

        return dateDict


    def mySysIsChinese(self, ch):
        """判断一个unicode是否汉字"""
        if '\u4e00' <= ch <= '\u9fff':
            return True
        else:
            return False


    def mySysIsExistChinese(self, word):
        """判断字符串是否包含汉字"""
        for ch in word:
            if self.mySysIsChinese(ch):
                return True
        return False


    def mySysIsAllChinese(self, word):
        """判断字符串是否全汉字"""
        for ch in word:
            if self.mySysIsChinese(ch) is False:
                return False
        return True


    def mySysGetChineseNum(self, word):
        """计算中文个数"""
        num = 0
        for ch in word:
            if self.mySysIsChinese(ch):
                num = num + 1
        return num

    def mySysIsNumber(self, uchar):
        """判断一个unicode是否是数字"""
        if uchar >= '\u0030' and uchar <= '\u0039':
            return True
        else:
            return False


    def mySysIsExistNumber(self, word):
        """判断字符串是否包含数字"""
        for ch in word:
            if self.mySysIsNumber(ch):
                return True
        return False


    def mySysIsAllNumber(self, word):
        """判断字符串是否全数字"""
        for ch in word:
            if self.mySysIsNumber(ch) is False:
                return False
        return True


    def mySysIsAllNumberExclude(self, word):
        """判断字符串除了","和"."是否全数字"""
        tmp = str(word).replace(',', '').replace('.', '')
        for ch in tmp:
            if self.mySysIsNumber(ch) is False:
                return False
        return True


    def mySysGetNumberNum(self, word):
        """计算数字个数"""
        num = 0
        for ch in word:
            if self.mySysIsNumber(ch):
                num = num + 1
        return num


    def mySysIsAlphabet(self, uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= '\u0041' and uchar <= '\u005a') or (uchar >= '\u0061' and uchar <= '\u007a'):
            return True
        else:
            return False


    def mySysIsExistAlphabet(self, word):
        """判断字符串是否包含英文字母"""
        for ch in word:
            if self.mySysIsAlphabet(ch):
                return True
        return False


    def mySysIsAllAlphabet(self, word):
        """判断字符串是否全英文字母"""
        for ch in word:
            if self.mySysIsAlphabet(ch) is False:
                return False
        return True


    def mySysGetAlphabetNum(self, word):
        """计算英文字母个数"""
        num = 0
        for ch in word:
            if self.mySysIsAlphabet(ch):
                num = num + 1
        return num


    def mySysIsother(self, uchar):
        """判断是否非汉字，数字和英文字符"""
        if not (self.mySysIsChinese(uchar) or self.mySysIsNumber(uchar) or self.mySysIsAlphabet(uchar)):
            return True
        else:
            return False


    def mySysIsFullwidthChar(self, uchar):
        """判断是否是全角字符"""
        ordchar = ord(uchar)
        if (ordchar >= 65281 and ordchar <= 65374) or (ordchar == 12288):
            return True
        else:
            return False


    def mySysIsExistFullwidthChar(self, word):
        """判断字符串是否包含全角字符"""
        for ch in word:
            if self.mySysIsFullwidthChar(ch):
                return True
        return False


    def mySysIsAllFullwidthChar(self, word):
        """判断字符串是否全全角字符"""
        for ch in word:
            if self.mySysIsFullwidthChar(ch) is False:
                return False
        return True


    def mySysGetFullwidthCharNum(self, word):
        """计算全角字符个数"""
        num = 0
        for ch in word:
            if self.mySysIsFullwidthChar(ch):
                num = num + 1
        return num


    def mySysGetAllCharacterNum(self, word):
        """计算中文、全角字符、数字、英文字母个数"""
        numFu = 0
        numCh = 0
        numAlp = 0
        numNumber = 0
        for ch in word:
            if self.mySysIsFullwidthChar(ch):
                numFu = numFu + 1
            elif self.mySysIsNumber(ch):
                numNumber = numNumber + 1
            elif self.mySysIsAlphabet(ch):
                numAlp = numAlp + 1
            elif self.mySysIsChinese(ch):
                numCh = numCh + 1
        return numCh, numFu, numAlp, numNumber


    def mySysSetClipboardText(self, clipboard):
        """设置剪切板"""
        # win32clipboard.OpenClipboard()
        # win32clipboard.EmptyClipboard()
        # win32clipboard.SetClipboardText(clipboard)
        # win32clipboard.CloseClipboard()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(win32con.CF_UNICODETEXT, clipboard)
        CloseClipboard()
        time.sleep(1)


    def mySysGetClipboardText(self):
        """读取剪贴板的数据"""
        OpenClipboard()
        d = GetClipboardData(win32con.CF_TEXT)
        CloseClipboard()
        # print(d.decode("GBK"))
        return d.decode('GBK')


    def mySysReadExcelSheetName(self, filename):
        """读Excel，返回所有sheet name
        filename为文件名"""
        try:
            # 打开文件
            workbook = xlrd.open_workbook(filename)
            # 获取所有sheet
            sheetnames = workbook.sheet_names()
            # logger.debug(sheetnames)
            return sheetnames
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysReadExcelRow(self, filename, sheetname, rowNum):
        """读Excel，返回某行所有内容
        filename为文件名
        sheetname为sheet名
        rowNum为行号"""
        try:
            # 打开文件
            workbook = xlrd.open_workbook(filename)
            # # 获取sheet2
            # sheet2_name = workbook.sheet_names()[1]
            # 根据sheet索引或者名称获取sheet内容
            sheet = workbook.sheet_by_name(sheetname)
            rowvalues = sheet.row_values(rowNum)
            # logger.debug(rowvalues)
            return rowvalues
            # sheet的名称，行数，列数
            # print(sheet.name, sheet2.nrows, sheet2.ncols)
            # rows = sheet.row_values(3)  # 获取第四行内容
            # cols = sheet.col_values(2)  # 获取第三列内容
            # # 获取单元格内容的三种方法
            # sheet2.cell(1, 0).value.encode('utf-8')
            # sheet2.cell_value(1, 0).encode('utf-8')
            # sheet2.row(1)[0].value.encode('utf-8')
            # # 获取单元格内容的数据类型
            # sheet2.cell(1, 3).ctype
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysReadExcelCol(self, filename, sheetname, colNum):
        """读Excel，返回某列所有内容
        filename为文件名
        sheetname为sheet名
        rowNum为列号"""
        try:
            # 打开文件
            workbook = xlrd.open_workbook(filename)
            # 获取所有sheet
            # logger.debug(workbook.sheet_names())
            # # 获取sheet2
            # sheet2_name = workbook.sheet_names()[1]
            # 根据sheet索引或者名称获取sheet内容
            sheet = workbook.sheet_by_name(sheetname)
            colvalues = sheet.col_values(colNum)
            # logger.debug(colvalues)
            return colvalues
        except:
            logger.error(traceback.format_exc())
            return None


    def mySysApi(self, url, requestMethod, header, datas, jsons):
        """接口API
        requestMethod为get和post"""
        # requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        # s.keep_alive = False  # 关闭多余连接
        login = None
        NumberTimes = 1
        while 1 == 1:
            try:
                logger.debug("datas:{}".format(datas))
                logger.debug("jsons:{}".format(jsons))
                if requestMethod.lower() == "get":
                    login = s.get(url, headers=header, data=datas, json=jsons)
                else:
                    login = s.post(url, headers=header, data=datas, json=jsons)
                login.encoding = 'utf8'
                logger.debug(url)
                # logger.debug(login.text)
                return login.text, login
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)
            # finally:
            #     login.close()


    def mySysOracleExecute(self, oracleIP, oraclePort, oracleUsername, oraclePassword, serviceName, sql, sshIP=None, sshPort=None, sshUsername=None, sshPassword=None):
        """oracle操作
        参数：
        oracleIP为数据库ip
        oraclePort为数据库端口
        oracleUsername为数据库用户名
        oraclePassword为数据库密码
        serviceName为service名
        sql为要执行的SQL
        sshIP为跳板ssh的IP
        sshPort为跳板ssh的端口
        sshUsername为跳板ssh用户名
        sshPassword为跳板ssh密码
        返回参数：
        fetchall数据库查询结束列表
        listDictResult为数据库查询结束列表字典，带列表名，如[{'a':1, 'b':2, 'c':3},{'a':4, 'b':5, 'c':6}]
        sqlType为sql类型'not select'和'select'
        rowcount为操作记录条数"""
        # requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        # s.keep_alive = False  # 关闭多余连接
        conn = None
        NumberTimes = 1
        while 1 == 1:
            try:
                listDictResult = []
                sqlType = None
                rowcount = None
                fetchall = []
                if sshIP is not None:
                    LOCAL_PORT = 11521  # 指定映射出来的端口
                    with SSHTunnelForwarder(
                        (sshIP, sshPort),  # 跳板服务器ip，ssh端口
                        ssh_username=sshUsername,  # 跳板ssh用户名
                        ssh_password=sshPassword,  # 跳板ssh密码
                        # ssh_pkey=r"F:\test\test.pem",  # 跳板数据库密钥
                        remote_bind_address=(oracleIP, oraclePort),  # 数据库ip，端口
                        local_bind_address=("127.0.0.1", LOCAL_PORT)  # 映射,默认即可
                    ) as server:

                        conn = cx_Oracle.connect("{}/{}@127.0.0.1:{}/{}".format(oracleUsername, oraclePassword, LOCAL_PORT, serviceName))

                        mycursor = conn.cursor()  # 新建游标

                        # mycursor.prepare(sql)
                        mycursor.execute(sql)  # 执行sql语句

                        title = None
                        # lowerSql = sql.lower()
                        description = mycursor.description
                        # 如果是select语句
                        # if 'update ' not in lowerSql and 'insert ' not in lowerSql and 'delete ' not in lowerSql:
                        if description is not None:
                            fetchall = mycursor.fetchall()   # sql查询输出方式所有，list
                            title = [i[0] for i in description]   # 获取表的列名，list
                            sqlType = 'select'
                            logger.debug('title:{}'.format(title))
                            logger.debug('fetchall:{}'.format(fetchall))
                        else:
                            fetchall = []
                            title = []
                            sqlType = 'not select'

                        conn.commit()  # sql修改提交保存

                        rowcount = mycursor.rowcount  # 发生修改数量
                        log = "oracle数据库：操作{}条记录\n{}".format(rowcount, sql)

                        conn.close()  # 数据库连接关闭，不关闭无法退出
                        conn = None

                        if rowcount <= 0:
                            logger.debug(log)
                        else:
                            logger.debug(log)
                            # 如果是select语句, 打包为元组的列表，再转换为字典
                            if description is not None:
                                for li in fetchall:
                                    dict_result = dict(zip(title, li))
                                    listDictResult.append(dict_result)  # 将字典添加到列表中
                else:
                    conn = cx_Oracle.connect(oracleUsername, oraclePassword, '{}:{}/{}'.format(oracleIP, oraclePort, serviceName))

                    mycursor = conn.cursor()  # 新建游标

                    mycursor.execute(sql)  # 执行sql语句

                    description = mycursor.description
                    # 如果是select语句
                    if description is not None:
                        fetchall = mycursor.fetchall()  # sql查询输出方式所有，list
                        title = [i[0] for i in description]  # 获取表的列名，list
                        sqlType = 'select'
                        logger.debug('title:{}'.format(title))
                        logger.debug('fetchall:{}'.format(fetchall))
                    else:
                        fetchall = []
                        title = []
                        sqlType = 'not select'

                    conn.commit()  # sql修改提交保存

                    rowcount = mycursor.rowcount  # 发生修改数量
                    log = "oracle数据库：操作{}条记录\n{}".format(rowcount, sql)

                    conn.close()  # 数据库连接关闭，不关闭无法退出
                    conn = None

                    if rowcount <= 0:
                        logger.debug(log)
                    else:
                        logger.debug(log)
                        # 如果是select语句, 打包为元组的列表，再转换为字典
                        if description is not None:
                            for li in fetchall:
                                dict_result = dict(zip(title, li))
                                listDictResult.append(dict_result)
                            logger.debug('listDictResult:{}'.format(listDictResult))

                return fetchall, listDictResult, sqlType, rowcount
            except:
                if NumberTimes >= self.maxNumberTimes:
                    self.mySysAssert(traceback.format_exc())
                    return None, None, None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)
            finally:
                if conn is not None:
                    conn.close()


    def mySysTextCheck(self, actualText, expectText, ifFuzzy=0):
        """函数说明：text检查
        ifFuzzy为0则为完全匹配，为1则为模糊匹配"""
        logger.debug('预期text内容：{}'.format(expectText))
        if ifFuzzy == 0:
            if expectText == actualText:
                logger.debug('实际text内容：{}'.format(actualText))
                return True
            else:
                err = '内容不相符，实际text内容：{}  预期text内容：{}'.format(actualText, expectText)
                self.mySysAssert(err)
                return None
        else:
            if expectText in actualText:
                logger.debug('实际text内容：{}'.format(actualText))
                return True
            else:
                err = '内容不相符，实际text内容：{}  预期text内容：{}'.format(actualText, expectText)
                self.mySysAssert(err)
                return None


    def mySysHsv2Rgb(self, h, s, v):
        """函数说明：hsv to rgb
        参数h, s, v
        返回r, g, b"""
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        logger.debug('rgb {}, {}, {}'.format(r, g, b))
        return r, g, b


    def mySysRgb2Hsv(self, r, g, b):
        """函数说明：rgb to hsv
        参数r, g, b
        返回h, s, v"""
        h = None
        s = None
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        logger.debug('hsv {}, {}, {}'.format(h, s, v))
        return h, s, v


    def mySysKeyboardListener(self, key):
        """函数说明：键盘监听
        参数key为设置当按下某按键时结束监听
        返回无
        例：mySysKeyboardListener('esc')"""
        logger.debug('键盘监听中，当按下按键{}时结束监听'.format(key))
        recorded = keyboard.record(until=key)
        logger.debug(recorded)


    def mySysGetRealScreenSize(self):
        """函数说明：获取真实的分辨率
        参数无
        返回真实分辨率w, h
        例：mySysKeyboardListener('esc')"""
        hDC = win32gui.GetDC(0)
        # 横向分辨率
        w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        # 纵向分辨率
        h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        logger.debug("显示分辨率:({},{})".format(w, h))
        return w, h


    def mySysGetScreenSize(self):
        """函数说明：获取缩放后的分辨率
        参数无
        返回缩放后的分辨率w, h
        例：mySysKeyboardListener('esc')"""
        w = win32api.GetSystemMetrics(0)
        h = win32api.GetSystemMetrics(1)
        logger.debug("缩放后的分辨率:({},{})".format(w, h))
        return w, h


    def mySysGetEpWeChatToken(self, corpid, corpsecret):
        """获取企业微信token
        https://work.weixin.qq.com/wework_admin/frame
        https://work.weixin.qq.com/api/doc
        """
        NumberTimes = 1
        while 1 == 1:
            try:
                tokenUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corpid, corpsecret)
                logger.debug(tokenUrl)
                text = json.loads(requests.get(tokenUrl).text)
                logger.debug(text)
                errcode = text['errcode']
                if errcode == 0:
                    token = str(text['access_token'])
                    return token
                else:
                    return None
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysGetEpWeChatGroupId(self, token):
        """企业微信查看部门与成员"""
        NumberTimes = 1
        while 1 == 1:
            try:
                url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={}'.format(token)
                text = json.loads(requests.get(url).text)['department']
                logger.debug(text)
                # 获取部门信息
                for item in text:
                    logger.debug("[部门id]:"+str(item['id'])+" [部门名称]:"+str(item[ 'name'])+" [父部门]:"+str(item['parentid'])+" [序号]:"+str(item['order']))
                # 获取成员信息
                # for i in range(len(text)):
                #     i = i + 1
                #     url_member = "https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token={}&department_id={}&fetch_child=FETCH_CHILD".format(token, i)
                #     r_member = requests.get(url_member)
                #     result_member = r_member.json()
                #     result_member_no = result_member['userlist']
                #     for item in result_member_no:
                #         logger.debug("[成员id]:"+str(item['userid'])+" [成员名称]:"+str(item['name'])+" [所属部门]:"+str(item['department']))
                return text
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysSendGroupMessageEpWeChat(self, token, media_id, weixinQunId):
        """企业微信发送群信息"""
        NumberTimes = 1
        while 1 == 1:
            try:
                values = {
                    "chatid": str(weixinQunId),
                    "msgtype": "image",
                    "image": {
                        "media_id": media_id
                    },
                    "safe": 0  # 表示是否是保密消息，0表示否，1表示是，默认0
                }
                datas = (bytes(json.dumps(values), 'utf-8'))
                url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token={}'.format(token)
                text = json.loads(requests.post(url, data=datas).text)
                logger.debug(text)
                json_result = eval(str(text))
                logger.info("发企业微信成功！('errcode':{})".format(json_result['errcode']))
                return True
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysSendPerMessageEpWeChat(self, token, agentid, textStr, touser="JiangHaiYang"):
        """企业微信发送个人信息"""
        NumberTimes = 1
        while 1 == 1:
            try:
                values = {
                    "touser": touser, #"jsh-jianghy003",
                    # "toparty": "2147",
                    "msgtype": "text",
                    "agentid": agentid,
                    "text": {
                        "content": str(textStr)
                    },
                    "safe": 0  # 表示是否是保密消息，0表示否，1表示是，默认0
                }
                datas = (bytes(json.dumps(values), 'utf-8'))
                url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(token)
                logger.debug(url)
                text = json.loads(requests.post(url, data=datas).text)
                logger.debug(text)
                json_result = eval(str(text))
                logger.info("发企业微信成功！('errcode':{})".format(json_result['errcode']))
                return True
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysSendPerMessageServerChan(self, token, textStr):
        """Server酱发送个人信息
        https://blog.csdn.net/bruce_6/article/details/81983387
        http://sc.ftqq.com/3.version
        """
        NumberTimes = 1
        while 1 == 1:
            try:
                datas = {
                    "text": "注",
                    "desp": str(textStr)
                }
                # datas = (bytes(json.dumps(values), 'utf-8'))
                url = 'http://sc.ftqq.com/{}.send?text=股票&desp={}'.format(token, str(textStr))
                logger.debug(url)
                text = json.loads(requests.get(url, timeout=10).text)
                # text = requests.get(url, timeout=10).text
                logger.debug(text)
                json_result = eval(str(text))
                if json_result['errmsg'] == 'success':
                    logger.info("发消息成功！('errcode':{})".format(json_result['errno']))
                    return True
                else:
                    logger.error(text)
            except:
                if NumberTimes >= self.maxNumberTimes:
                    logger.error(traceback.format_exc())
                    return None
                logger.error('第{}次发起请求失败'.format(NumberTimes))
                NumberTimes = NumberTimes + 1
                time.sleep(3)


    def mySysThreading(self, func, *args):
        """多线程"""
        # t1 = threading.Thread(target=func, args=(*args,))
        t1 = myThread(target=func, args=(*args, ), kwargs={})
        t1.start()
        return t1


    def mySysMultiprocessingProcess(self, func, *args):
        """多进程，建议linux使用"""
        p1 = Process(target=func, args=(*args, ))
        p1.start()
        return p1


    def mySysKeyboardkeyDown(self, keyName):
        """按下按键"""
        win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)


    def mySysKeyboardkeyUp(self, keyName):
        """释放按键"""
        win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)


    def mySysKeyboardOneKey(self, key):
        """模拟单个按键"""
        self.mySysKeyboardkeyDown(key)

        self.mySysKeyboardkeyUp(key)


    def mySysKeyboardtwoKeys(self, key1, key2):
        """模拟两个组合键"""
        self.mySysKeyboardkeyDown(key1)

        self.mySysKeyboardkeyDown(key2)

        self.mySysKeyboardkeyUp(key2)

        self.mySysKeyboardkeyUp(key1)


    def mySysXmlCreateDocument(self, rootDoc):
        """建立根节点"""
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, rootDoc, None)  # 建立根节点
        root = dom.documentElement  # 获取对象
        return dom, root


    def mySysXmlCreateElement(self, dom, father, elementDoc):
        """创建子节点"""
        employee = dom.createElement(elementDoc)
        element = father.appendChild(employee)  # 创建子节点
        return element


    def mySysXmlCreateAttribute(self, element, name, value):
        """建立属性"""
        element.setAttribute(name, value)


    def mySysXmlCreateTextNode(self, dom, element, value):
        """节点赋值"""
        textNode = dom.createTextNode(value)
        element.appendChild(textNode)  # 赋值


    def mySysXmlReadFile(self, fileName):
        """读xml"""
        dom = xml.dom.minidom.parse(fileName)
        root = dom.documentElement  # 获取文档根元素
        return dom, root


    def mySysXmlWriteFile(self, dom, fileName):
        """写xml"""

        f = open(fileName, 'w')
        dom.writexml(f, addindent='  ', newl='\n', encoding='UTF-8')
        f.close()

        # tree = ElementTree.parse(fileName)  # 解析test.xml这个文件
        # root = tree.getroot()  # 得到根元素，Element类
        # self.myXmlXiuGai(root, '\t', '\n')  # 执行美化方法
        # tree.write(fileName, encoding='utf-8')  # 保存文件


    def mySysXmlXiuGai(self, element, indent, newline, level=0):
        """xml文档格式整理"""
        # 判断element是否有子元素
        if element:
            # 如果element的text没有内容
            if element.text == None or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        temp = list(element)  # 将elemnt转成list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):
                subelement.tail = newline + indent * (level + 1)
            else:
                subelement.tail = newline + indent * level
            self.mySysXmlXiuGai(subelement, indent, newline, level=level + 1)

