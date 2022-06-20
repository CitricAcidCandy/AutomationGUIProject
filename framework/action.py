# -*- coding: utf-8 -*-
import base64
import time
import traceback
import pyautogui
import pyperclip
import pyscreeze

from abc import ABCMeta, abstractmethod
from datetime import datetime
from config.config import Config
from framework.logger import Log
from utils.BaiDu_AI import BaiDu_CharacterRecognition
from utils.openCV2.PictureMatching import *


class Action(metaclass=ABCMeta):
    __logger = None
    __pyautogui = None

    def __init__(self, desc):
        self.loger = self.GetLoger()
        self.pyautogui = self.PyAutoGuiInstance()
        self.desc = desc

    @classmethod
    def PyAutoGuiInstance(cls):
        if not cls.__pyautogui:
            cls.__pyautogui = pyautogui
        return cls.__pyautogui

    @classmethod
    def GetLoger(cls):
        if not cls.__logger:
            cls.__logger = Log.Instance()
        return cls.__logger

    @classmethod
    def readImageForBase64(cls, imgSavePath=None, ):
        """截图并且返回Base64编码"""
        if imgSavePath is not None:
            log_ScreenshotPath = imgSavePath
        else:
            log_ScreenshotPath = Config.log_ScreenshotPath
        imgFile = f"{log_ScreenshotPath}\\ErroOrFail_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        cls.PyAutoGuiInstance().screenshot(imgFile, region=(18, 10, 1280, 720))
        with open(imgFile, "rb") as f:
            base64_data = base64.b64encode(f.read())
            base64_data_str = str(base64_data, encoding="utf-8"),
        return base64_data_str

    @abstractmethod
    def run(self):
        pass


class Click(Action):
    def __init__(self, desc="Pattern", **kwargs):
        """在屏幕上识别目标图片后点击该图片"""
        super(Click, self).__init__(desc)
        self.image = kwargs.get("image")
        self.min_confidence = kwargs.get("min_confidence")
        self.clicks = kwargs.get("clicks", 1)
        self.interval = kwargs.get("interval", 0.2)
        self.button = kwargs.get("button", 'right')
        self.duration = kwargs.get("duration", 0)
        self.saveImage = kwargs.get("saveImage", False)
        self.existElement = kwargs.get("existElement", False)
        self.cycledetection = kwargs.get("cycledetection", True)
        self.targetOffset = kwargs.get("targetOffset", None)
        self.failResponse = kwargs.get("failResponse", False)
        self.point = None

    def PointLocateOnScreen(self, screenshot=None):
        """
        获取识别图片在屏幕上的位置
        :return: 识别图片的位置
        """
        if screenshot is not None:
            image = screenshot
        else:
            image = self.image
        img_point = self.pyautogui.locateCenterOnScreen(image)
        confidence = 1
        if not img_point and self.cycledetection:
            while True:
                confidence = confidence - 0.05
                if not img_point:
                    img_point = self.pyautogui.locateCenterOnScreen(image, grayscale=False,
                                                                    confidence=confidence)
                else:
                    break
                if confidence < self.min_confidence:
                    break
        if img_point is not None:
            self.loger.debug(f"成功找到{self.desc}，坐标位置为：{img_point}")
        if self.targetOffset is not None:
            try:
                self.loger.debug(f"设置坐标偏移, {self.targetOffset}")
                img_point = pyscreeze.Point(x=img_point[0] + self.targetOffset[0],
                                            y=img_point[1] + self.targetOffset[1])
                # img_point = (img_point[0] + self.targetOffset[0], img_point[1] + self.targetOffset[1])
                return img_point
            except:
                self.loger.error("坐标偏移设置出错，错误原因：\n" + traceback.format_exc())
        return img_point

    def ExitImage(self):
        """
        检测目标是否存在
        :return:
        """
        img_point = self.PointLocateOnScreen()
        if img_point is not None:
            return False
        self.loger.debug(f"检测：{self.desc}在当前页面不存在，本次点击测试通过")

    @staticmethod
    def SetMousePoint(x, y):

        arg = {
            "start": (x, y)
        }
        mouseDrag = MouseDrag(desc="设置鼠标位置", **arg)
        mouseDrag.set_mouse_position()

    def run(self):
        self.loger.debug(f"开始执行 ClickAction : {self.desc}")
        img_point = self.PointLocateOnScreen()
        if img_point is None:
            self.loger.debug(f"{self.desc}查找失败")
            self.loger.debug("Click 执行结束")
            if self.failResponse:
                return True
            return False
        try:
            self.point = img_point
            time.sleep(1)
            self.loger.debug(f"点击{self.desc}, 坐标位置为：{img_point}")
            self.SetMousePoint(self.point[0], self.point[1])
            self.pyautogui.click(self.point, clicks=self.clicks, interval=self.interval, duration=0.0)
            if self.saveImage:
                self.loger.debug(f"对点击：{self.desc}后的页面进行截图")
                screenshotPath = self.loger.path + "\\" + self.loger.folderName + "\\" + f"点击{self.desc}之后的截图.png"
                self.pyautogui.screenshot(screenshotPath)
            if self.existElement:
                if not self.ExitImage():
                    self.loger.debug(f"点击后检测到：{self.desc}，本次点击失败")
                    self.loger.debug("Click 执行结束")
                    if self.failResponse:
                        return True
                    return False
            self.loger.debug("Click 执行结束")
            return True
        except:
            self.loger.error(f"点击事件：{self.desc} 发生错误！原因为：\n" + traceback.format_exc())
            self.loger.debug("Click 执行结束")
            return False


class DetectAction(Action):
    def __init__(self, desc="", **kwargs):
        """
        在截图中检测目标，判断该元素是否存在
        """
        super(DetectAction, self).__init__(desc)
        try:
            self.image = load_image_file(kwargs.get("image"))
            self.screenshot = load_image_file(kwargs.get("screenshot"))
        except:
            self.loger.error("CV2读取图片发生异常，异常原因是:\n" + traceback.format_exc())
        self.saveImage = kwargs.get("saveImage", False)
        self.min_confidence = kwargs.get("min_confidence", 0.7)
        self.cycledetection = kwargs.get("cycledetection", False)

    def ImageRecognition(self):
        """图片对比，存在则返回该图片在目标图片中的位置的中心点"""
        point = None
        process = MatchImg(self.image, self.screenshot, threshod=self.min_confidence)
        if not self.cycledetection:
            point = process.get_img_center()
            if point is not None:
                self.loger.debug(f"图片识别成功，该图片在屏幕的位置是：{point[0] + 18},{point[1] + 61}")
                return point
            self.loger.debug("图片识别失败，无法找到该图片在屏幕的位置")
            return False
        confidence = 1
        while True:
            confidence = confidence - 0.1
            if point is None:
                process.set_confidence(confidence)
                point = process.get_img_center()
            else:
                self.loger.debug(f"图片识别成功，该图片在屏幕的位置是：{point[0] + 18},{point[1] + 61}")
                return point
            if confidence < self.min_confidence:
                self.loger.debug("图片识别失败，无法找到该图片在屏幕的位置")
                break
        return False

    def run(self):
        self.loger.debug(f"开始执行 DetectAction : {self.desc}")
        points = self.ImageRecognition()
        if self.saveImage:
            self.loger.debug("执行截图操作")
            screenshotPath = self.loger.path + "\\" + self.loger.folderName + "\\" + f"检测{self.desc}之后的截图.png"
            self.pyautogui.screenshot(screenshotPath)
        self.loger.debug("DetectAction 执行结束")
        return points


class MouseDrag(Action):
    def __init__(self, desc="页面", **kwargs):
        """
        鼠标拖动
        :param starPoints: 起始位置
        :param endPoints: 终止位置
        :param desc:该动作的描述
        :param time:执行拖动的时长，默认为1秒内拖动结束
        """
        super(MouseDrag, self).__init__(desc)
        self.starPoints = kwargs.get("start")
        self.endPoints = kwargs.get("end", None)
        self.time = kwargs.get("time", 1)

    def set_mouse_position(self):
        """
        设置鼠标初始位置
        """
        try:
            x, y = self.starPoints
            self.pyautogui.moveTo(x, y)
            return True
        except:
            self.loger.error("设置鼠标初始位置异常，异常原因：\n" + traceback.format_exc())
            return False

    def DragTo(self):
        """鼠标拖动"""
        try:
            x, y = self.endPoints
            self.pyautogui.dragTo(x, y, self.time)
            return True
        except:
            self.loger.error("拖动鼠标到指定位置异常，异常原因：\n" + traceback.format_exc())
            return False

    def run(self):
        self.loger.debug(f"开始执行 鼠标拖动Action: {self.desc}")
        if self.set_mouse_position():
            if self.DragTo():
                self.loger.debug("Action 执行成功")
                self.loger.debug("Action 执行执行结束")
                return True
        self.loger.debug("Action 执行执行结束")
        return False


class PasteAction(Action):
    def __init__(self, desc="defunl", **kwargs):
        """
        粘贴文本
        :param contents: 需要粘贴的文本内容
        :param desc: 描述
        """
        super(PasteAction, self).__init__(desc)
        self.content = kwargs.get("contents")

    def run(self):
        self.loger.debug(f"开始执行 文本粘贴Action：{self.desc}")
        pyperclip.copy(self.content)
        self.pyautogui.hotkey('ctrl', 'v')
        self.loger.debug(f"Action 执行结束")
        return True


class TypeAction(Action):
    def __init__(self, desc="defunl", **kwargs):
        """
        键盘按键响应
        :param key: 键盘上各个按键的key值
        :param desc:
        """
        super(TypeAction, self).__init__(desc)
        self.key = kwargs.get("key")

    def run(self):
        self.loger.debug(f"开始执行 键盘响应Action: {self.desc}")
        self.pyautogui.press(self.key)
        self.loger.debug("Action 执行结束")
        return True


class TmageRecognitionAction(Action):
    def __init__(self, desc="defunl", **kwargs):
        """
        使用百度Ai接口进行OCR识别
        :param desc: 描述
        """
        super(TmageRecognitionAction, self).__init__(desc)
        self.urlName = kwargs.get('urlName')
        self.imgFile = kwargs.get('imgFile')
        self.failResponse = kwargs.get('failResponse', False)

    def run(self):
        try:
            self.loger.debug(f"开始执行 图像识别Action: {self.desc}")
            image_text = BaiDu_CharacterRecognition.get_img_str(self.urlName, self.imgFile)
            if image_text:
                self.loger.debug(f"成功获取百度AI识别接口返回数据，识别结果为：{image_text}")
                self.loger.debug("Aciton执行结束")
                return image_text
        except:
            self.loger.debug("识别失败出现错误，异常原因为\n" + traceback.format_exc())
            if self.failResponse:
                self.loger.debug("忽略错误，继续执行自动化步骤")
                self.loger.debug("Aciton执行结束")
                return True
            self.loger.debug("Aciton执行结束")
            return False
