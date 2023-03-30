# -*- coding:utf-8 -*-

import sys,os
import logging
import ctypes
import time
import datetime
import configparser
# import myGlobal
import platform

platformSystem = platform.system()

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01 # text color contains blue. 
FOREGROUND_GREEN= 0x02 # text color contains green. 
FOREGROUND_RED = 0x04 # text color contains red. 
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN 
FOREGROUND_PURPLE = FOREGROUND_RED | FOREGROUND_BLUE 

STD_OUTPUT_HANDLE= -11

if platformSystem == "Windows":
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_color(color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool


class Logger(object):
    """docstring for Logger"""
    def __init__(self):

        super(Logger, self).__init__()
        self.log_cmd_level = logging.DEBUG
        self.log_file_level = logging.DEBUG
        self.logName = 'log'
        self.localDatatime = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.__getConfig()
        nowTime = time.localtime()
        logPath = '{}/log/{}{}{:0>2}{:0>2}.log'.format(os.getcwd(),self.logName, nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday)    #设置日志路径

        logLevel = logging.DEBUG                     #设置日志级别
        self.logger = logging.getLogger(logPath)     #创建日志
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')    #设置日志格式

        #设置CMD日志
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(fmt)

        self.sh.setLevel(self.log_cmd_level)

        #设置文件日志
        self.fh = logging.FileHandler(logPath)
        self.fh.setFormatter(fmt)
        self.fh.setLevel(self.log_file_level)

        self.logger.addHandler(self.sh)        #添加handler
        self.logger.addHandler(self.fh)



    def __del__(self):
        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)


    def debug(self, message, color = FOREGROUND_BLUE):
        self.__updateFilename()
        if platformSystem == "Windows":
            set_color(color)
        self.logger.debug(message)
        if platformSystem == "Windows":
            set_color(FOREGROUND_WHITE)


    def info(self,message,color = FOREGROUND_GREEN):
        self.__updateFilename()
        if platformSystem == "Windows":
            set_color(color)
        self.logger.info(message)
        if platformSystem == "Windows":
            set_color(FOREGROUND_WHITE)


    def warning(self,message,color=FOREGROUND_YELLOW):
        self.__updateFilename()
        if platformSystem == "Windows":
            set_color(color)
        self.logger.warning(message)
        if platformSystem == "Windows":
            set_color(FOREGROUND_WHITE)


    def error(self,message,color=FOREGROUND_RED):
        self.__updateFilename()
        if platformSystem == "Windows":
            set_color(color)
        self.logger.error(message)
        if platformSystem == "Windows":
            set_color(FOREGROUND_WHITE)


    def critical(self,message, color = FOREGROUND_PURPLE):
        if platformSystem == "Windows":
            set_color(color)
        self.logger.critical(message)
        if platformSystem == "Windows":
            set_color(FOREGROUND_WHITE)



    def __updateFilename(self):
        if self.localDatatime == str(datetime.datetime.now().strftime("%Y-%m-%d")):
            return None

        self.localDatatime = str(datetime.datetime.now().strftime("%Y-%m-%d"))

        self.logger.removeHandler(self.sh)
        self.logger.removeHandler(self.fh)

        self.log_cmd_level = logging.DEBUG
        self.log_file_level = logging.DEBUG
        self.logName = 'log'
        self.__getConfig()
        nowTime = time.localtime()
        logPath = '{}/log/{}{}{:0>2}{:0>2}.log'.format(os.getcwd(),self.logName, nowTime.tm_year, nowTime.tm_mon, nowTime.tm_mday)    #设置日志路径

        logLevel = logging.DEBUG                     #设置日志级别
        self.logger = logging.getLogger(logPath)     #创建日志
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')    #设置日志格式

        #设置CMD日志
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(fmt)

        self.sh.setLevel(self.log_cmd_level)

        #设置文件日志
        self.fh = logging.FileHandler(logPath)
        self.fh.setFormatter(fmt)
        self.fh.setLevel(self.log_file_level)

        self.logger.addHandler(self.sh)        #添加handler
        self.logger.addHandler(self.fh)


    def __getConfig(self):
        levelDict = {
            'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL
        }
        fileName = '{}/conf/config.ini'.format(os.getcwd())

        cf = configparser.ConfigParser()

        cf.read(fileName)

        level = cf.get('LOG', 'log_file_level')    #读取日志文件的日志级别
        if level in levelDict.keys():
            self.log_file_level = levelDict[level]


        level = cf.get('LOG', 'log_cmd_level')        #读取cmd的日志级别
        if level in levelDict.keys():
            self.log_cmd_level = levelDict[level]





