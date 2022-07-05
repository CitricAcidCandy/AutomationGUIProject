# -*- coding: utf-8 -*-
import os
import time

import unittest

from framework.HTMLTestRunner_cn import HTMLTestRunner
from framework.action import Action
from page.pageData.hao123Data import *

from page.Page_BiliLogin import Login

project_path = Config.imgPath
project_logPath = Config.logPath


class Test_Login(unittest.TestCase):
    """数据驱动测试——登录与注册"""

    @classmethod
    def setUpClass(cls):
        Login.SetUp_SetPageData(Hao123Param)
        Login.addPageData("刷新客户端", Login.SetType("F5"))
        Login.addPageData("f1", Login.SetType("f1"))
        cls.pyautogui = Action.PyAutoGuiInstance()

    def setUp(self) -> None:
        self.imgs = []

    def tearDown(self) -> None:
        self.login.TypeAction("key_f5", desc="刷新客户端")
        time.sleep(1)

    def test_AccountLogin(self):
        """自动化登录"""
        self.login = Login.SetUP_ddt_DataInitialization()
        result = self.login.page_AccountLogin(login_ActionLsit)
        self.assertEqual(True, result)


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Login)

    # path = os.path.dirname(os.path.abspath(__file__))
    # suite.addTest(loade.discover(path))
    if not os.path.exists(project_logPath):
        os.mkdir(project_logPath)
    with open(f"{project_logPath}\\testrulst.html", "wb") as f:
        runner = HTMLTestRunner(title="自动化测试报告", description="登录相关自动化测试", tester="柠檬果",
                                stream=f, verbosity=2, retry=1,
                                save_last_try=False)
        runner.run(suite)
