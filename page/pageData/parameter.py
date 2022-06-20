# -*- coding: utf-8 -*-  ##设置编码方式


def ClickActionParameters(image, min_confidence: float, clicks=1, interval=0.2, button='right', duration=0,
                          saveImage=False, existElement=False, cycledetection=True, targetOffset=None,
                          failResponse=False):
    """
    点击动作必备参数组

    :param image: 图片地址
    :param clicks: 点击次数
    :param interval: 每次点击的间隔
    :param min_confidence: 最小识别精度,不允许超过1
    :param button: 鼠标按键，默认为左键
    :param duration: 点击持续时间
    :param saveImage: 每次点击后是否需要截图
    :param existElement: 判断元素是否存在，默认为False
    :param targetOffset: 坐标偏移设置
    :param cycledetection: 循环检测，默认为False
    :param failResponse: 当该操作执行失败或循环次数下未满足跳出条件时终止任务，True则忽视失败继续执行
    """
    return {
        "image": image,
        "min_confidence": min_confidence,
        "clicks": clicks,
        "interval": interval,
        "button": button,
        "duration": duration,
        "saveImage": saveImage,
        "existElement": existElement,
        "cycledetection": cycledetection,
        "targetOffset": targetOffset,
        "failResponse": failResponse,
        "type": "click",
    }


def DetectActionParameters(image, screenshot, min_confidence=0.7, saveImage=False, cycledetection=False):
    """
    在截图中检测目标，判断该元素是否存在

    :param image: 要匹配的目标
    :param screenshot: 大截图
    :param min_confidence: 识别精度
    :param saveImage: 是否要保存该当前截图
    :param cycledetection: 循环检测
    """
    return {"image": image,
            "screenshot": screenshot,
            "min_confidence": min_confidence,
            "saveImage": saveImage,
            "cycledetection": cycledetection,
            "type": 'detect',
            }


def TypeActionParameter(KeyboardButton):
    """
       自动化输入键盘按钮方法需要的内容，KeyboardButton:对应键盘的按钮，例如回车键：Key.ENTER。
       """
    return {
        "key": KeyboardButton,
        "type": "type",
    }


def PasteActionParameter(contents):
    """
       自动化粘贴文本内容方法所需参数。\n contents:需要粘贴的内容。
       """
    return {
        "contents": contents,
        "type": "paste",
    }


def DragActionParameter(start, end, time=1):
    """
    拖动鼠标动作所需参数

    :param start: 起始坐标
    :param end: 终点坐标
    :param time: 拖动所需时长
    :return:
    """
    return {
        "start": start,
        "end": end,
        "time": time,
        "type": "drag",
    }


def TmageRecognitionAction(urlName, imgFile, failResponse=False):
    """
    使用百度Ai接口进行OCR识别
    :param urlName: 接口路径名字：通用文字识别， 数字识别
    :param imgFile: 需要识别的图片路径
    :param failResponse: 当该操作执行失败或循环次数下未满足跳出条件时终止任务，True则忽视失败继续执行
    :return:
    """
    return {
        "urlName": urlName,
        "imgFile": imgFile,
        "failResponse": failResponse
    }
