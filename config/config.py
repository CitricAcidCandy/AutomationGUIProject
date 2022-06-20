# -*- coding: utf-8 -*-
from datetime import datetime
import os


class Config:
    project = os.path.abspath(os.path.abspath(os.getcwd()) + os.path.sep + "..")  # 项目路径
    logPath = project + r'\log' + "\\testCase_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # log存放路径
    log_ScreenshotPath = logPath + "\\screenshot"  # log截图存放路径
    imgPath = project + r'\img'  # 截图存放路径
