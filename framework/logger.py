# -*- coding: utf-8 -*-
import logging  # 引入logging模块
import os.path
import time
from config.config import Config
import os

path = Config.logPath
imgPath = Config.log_ScreenshotPath
logerFile = path + "\\log.txt"
logger = logging.getLogger()


class Log(object):
    __Instance = None

    @classmethod
    def Create_LogFolderAndFile(cls):
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(imgPath):
            os.mkdir(imgPath)
        open(logerFile, 'w')

    @classmethod
    def settings(cls):
        logger.setLevel(logging.DEBUG)
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        fh = logging.FileHandler(logerFile, mode='w')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)

    @classmethod
    def Instance(cls):
        """获取对象"""
        if not cls.__Instance:
            cls.__Instance = Log()
            cls.Create_LogFolderAndFile()
            cls.settings()
        return cls.__Instance

    @staticmethod
    def debug(msg):
        logger.debug(msg)

    @staticmethod
    def info(msg):
        logger.info(msg)

    @staticmethod
    def warning(msg):
        logger.warning(msg)

    @staticmethod
    def error(msg):
        logger.error(msg)

    @staticmethod
    def critical(msg):
        logger.critical(msg)
