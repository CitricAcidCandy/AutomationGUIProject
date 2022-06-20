# -*- coding: utf-8 -*-

from framework.action import *
import pyperclip

class BasePage:

    def __init__(self, dataDict):
        self.actionFunctionDict = None
        self.DataInitialization(dataDict)
        self.CreateFunctionDict()

    @classmethod
    def DataInitialization(cls, dataDict):
        cls.__actionDict = dataDict

    @staticmethod
    def GetPyAutoGui():
        return Action.PyAutoGuiInstance()

    @classmethod
    def GetLoger(cls):
        return Action.GetLoger

    def AutoActionTask(self, actionAutoList, MethodRunTimes=False, sleep=1):
        """
        根据测试数据中的自动化步骤列表执行自动化任务

        :param sleep: 每次自动化运行后休眠时间
        :param MethodRunTimes: 自动化步骤列表下标
        :param actionAutoList: 自动化步骤列表
        :return:
        """
        result = None
        ListIndex = 0
        for i in range(0, len(actionAutoList)):
            ListIndex += i + 1
            result = self.DetermineTheActionTypeAndCall(actionAutoList[i])
            if not result:
                if MethodRunTimes:
                    return result, i
                return result
            time.sleep(sleep)
        if MethodRunTimes:
            return result, ListIndex
        return result

    def CreateFunctionDict(self):
        if self.actionFunctionDict is None:
            self.actionFunctionDict = {
                "click": self.ClickAction,
                "detect": self.DetectAction,
                "type": self.TypeAction,
                "paste": self.PasteAction,
                "drag": self.MouseDrag
            }

    def DetermineTheActionTypeAndCall(self, dictKeyName, desc=""):
        """
        通过字典的type的值获取动作的类型，并调用相应的自动化action

        :param desc: 描述
        :param dictKeyName: dict的Key值
        """
        actionType = self.__actionDict.get(dictKeyName).get("type")
        actionFuction = self.actionFunctionDict.get(actionType)
        if desc != "" or desc is not None:
            return actionFuction(dictKeyName, desc=desc)
        return actionFuction(dictKeyName, desc=dictKeyName)

    def ClickAction(self, dict_KeyName, desc="", ) -> bool:
        """
        点击页面按钮

        :param dict_KeyName: dict的Key值
        :param desc: 描述
        :return: 返回运行结果
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = Click(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def DetectAction(self, dict_KeyName, desc=""):
        """
        在大图中找小图的位置

        :param dict_KeyName: dict的Key值
        :param desc: 描述
        :return: 失败时返回False，成功则放回坐标
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = DetectAction(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def MouseDrag(self, dict_KeyName, desc="") -> bool:
        """
        鼠标移动

        :param dict_KeyName: dict的Key值
        :param desc: 描述
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = MouseDrag(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def PasteAction(self, dict_KeyName, desc=""):
        """
        粘贴文本

        :param dict_KeyName: dict的Key值
        :param desc: 描述
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = PasteAction(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def TypeAction(self, dict_KeyName, desc=""):
        """
        键盘按键响应

        :param dict_KeyName: dict的Key值
        :param desc: 描述
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = TypeAction(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def TmageRecognitionAction(self, dict_KeyName, desc=""):
        """
        图像识别——文字识别
        :param dict_KeyName: dict的Key值
        :param desc: 描述
        """
        arg = self.__actionDict.get(dict_KeyName)
        act = TmageRecognitionAction(desc=self.Set_desc(dict_KeyName, desc), **arg)
        return act.run()

    def SetGmInstructions(self, GM: str):
        """pass"""
        ...
        pyperclip.copy(GM)
        self.GetPyAutoGui().press(['ctrl', 'v'])
        self.GetPyAutoGui().press('enter', interval=0.25, presses=2)

    @staticmethod
    def Set_desc(keyName, desc):
        if desc == "" or desc is None:
            return keyName
        return desc
