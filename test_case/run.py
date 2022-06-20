import os
import time
import unittest

import win32con
import win32gui

from config.config import Config
from framework.HTMLTestRunner_cn import HTMLTestRunner

project_path = Config.imgPath
project_logPath = Config.logPath
project = Config.project


def runGame():
    label = 'Google Chrome'  # pc客户端标题且无子句柄
    hwnd = win32gui.FindWindow(None, label)

    if label == 'Google Chrome':
        if hwnd <= 0:
            # 从系统环境变量打开应用
            filepath = os.path.join(os.environ.get('APP_PATH'), "xxx.bat")
            if os.path.isfile(filepath): os.system(filepath)
            time.sleep(10)
            hwnd = win32gui.FindWindow(None, label)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, None, 10, 10, 0, 0, win32con.SWP_NOSIZE)  # 设置client的窗口位置(10,10)以防窗口偏移出屏幕
        dlg = win32gui.GetClientRect(hwnd)  # 获取client的窗口大小


if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestLogin)
    runGame()
    suite, loade = unittest.TestSuite(), unittest.TestLoader()
    path = os.path.dirname(os.path.abspath(__file__))
    suite.addTest(loade.discover(path))
    if not os.path.exists(project_logPath):
        os.mkdir(project_logPath)
    with open(f"{project_logPath}\\testrulst.html", "wb") as f:
        runner = HTMLTestRunner(title="自动化测试报告", description="登录相关自动化测试", tester="柠檬果",
                                stream=f, verbosity=2, retry=1,
                                save_last_try=True)
        runner.run(suite)
