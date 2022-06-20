# -*- coding: utf-8 -*-
from datetime import time

import pyscreeze

from page.basePage import BasePage
from framework.action import Click
from page.pageData.parameter import PasteActionParameter, TypeActionParameter


class Login(BasePage):
    __loginPageData = None
    __loginInstance = None

    def __init__(self):
        super().__init__(self.__loginPageData)

    @classmethod
    def SetUP_ddt_DataInitialization(cls, use="test00111", pwd="21123"):
        """
        数据初始化
        :param use: 账号
        :param pwd: 密码
        """
        pasteAction_arg_use, pasteAction_arg_pwd = cls.SetAccount(use, pwd)
        cls.addPageData("username", pasteAction_arg_use)
        cls.addPageData("password", pasteAction_arg_pwd)
        cls.__loginInstance = Login()
        return cls.__loginInstance

    @classmethod
    def SetUP_ddt_RegisterDataInitialization(cls, **registerData):
        """
        注册数据初始化

        :param registerData: 参数字典
        """
        addregisterData = cls.SetRegisterAccount(registerData.get("username"), registerData.get("password"),
                                                 registerData.get("password1"))
        cls.addPageData("registerUse", addregisterData.get("use"))
        cls.addPageData("registerUsePwd", addregisterData.get("pwd"))
        cls.addPageData("registerAgainPwd", addregisterData.get("againPwd"))
        cls.__loginInstance = Login()
        return cls.__loginInstance

    @classmethod
    def SetUp_SetPageData(cls, PageData):
        """初始化字典"""
        cls.__loginPageData = PageData

    def page_AccountLogin(self, actionAutoList, MethodRunTimes=False, sleep=1):

        return self.AutoActionTask(actionAutoList, MethodRunTimes=MethodRunTimes, sleep=sleep)

    def page_RegisterAccount(self, actionAutoList, MethodRunTimes=False, sleep=1):
        """账号注册测试"""
        result = True
        for i in range(0, len(actionAutoList)):
            ListIndex = i + 1
            if not result:
                if MethodRunTimes:
                    return result, ListIndex
                return result
            if actionAutoList[i] == "btn_PasswordFrame":
                registerAgainPwdPoint = self.GetRegisterAgainPwdPoint()
            if actionAutoList[i] == "again":
                self.GetPyAutoGui().click(registerAgainPwdPoint, clicks=2)
                continue
            result = self.DetermineTheActionTypeAndCall(actionAutoList[i])
            time.sleep(sleep)
        if MethodRunTimes:
            return result, ListIndex
        return result

    def page_SwitchSeverList(self, actionList, MethodRunTimes=False, sleep=1):
        return self.AutoActionTask(actionList, MethodRunTimes=MethodRunTimes, sleep=sleep)

    def GetRegisterAgainPwdPoint(self):
        """获取注册页面二次密码的坐标位置"""
        click = Click(self.__loginPageData.get("btn_PasswordFrame"))
        pwdPoint = click.PointLocateOnScreen()
        return pyscreeze.Point(x=pwdPoint[0], y=pwdPoint[1] + 70)

    @classmethod
    def addPageData(cls, keyName, value):
        """
        往字典里加值

        :param keyName: 字典的key命名
        :param value: key对应的值
        :return:
        """
        if keyName in cls.__loginPageData.keys():
            cls.__loginPageData[keyName].update(value)
            return
        cls.__loginPageData[keyName] = value

    @classmethod
    def SetAccount(cls, use, pwd):
        """设置登录账号"""
        return PasteActionParameter(use), PasteActionParameter(pwd)

    @classmethod
    def SetRegisterAccount(cls, use, pwd, againPwd):
        """设置注册账号"""
        return {
            "use": PasteActionParameter(use),
            "pwd": PasteActionParameter(pwd),
            "againPwd": PasteActionParameter(againPwd)
        }

    @classmethod
    def SetType(cls, KeyboardButton):
        """设置键盘按键"""
        return TypeActionParameter(KeyboardButton)

    @classmethod
    def SetGm(cls, Gm):
        """设置键盘按键"""
        return PasteActionParameter(Gm)
