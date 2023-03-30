# -*- coding:utf-8 -*-
from basic.logger import Logger
import time

def getLogger():
    global logger
    return logger


logger = Logger()


def myFuncRunningTime(*args, **kwargs):
    """"""

    def handle_func(func):
        def inner(*args, **kwargs):
            startTime = time.perf_counter()  # datetime.datetime.now()
            func(*args, **kwargs)
            stopTime = time.perf_counter()  # datetime.datetime.now()
            totalTime = str(stopTime - startTime)
            logger.debug('{}函数运行用时间(秒): {} '.format(func, totalTime))

        return inner

    return handle_func