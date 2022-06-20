# 自动化项目概要说明

 

## 项目文件夹说明

```python
config: 存放配置文件
framework：存放框架相关代码
img: 截图
    
log:
    test_case_N_Y_D_M_S:运行生成的日志文件夹
        screenshot:存放用例失败或者用例执行过程中需要截图
            
page:所有关于应用的页面元素的类都存放这个文件夹            
test_case:存放测试用例
utils:存放工具类
```

# 环境准备

需要安装的第三方库

**注：自动化测试项目路径不可有中文！**

```python
pip install pyautogui
pip install opencv-contrib-python
pip install pillow
pip install pyperclip
pip install pypiwin32
pip install unittestreport
pip insatll request
pip install pytest          （备选）
pip install allure-pytest   （备选）
```

# 自动化说明

## Action类说明

**类说明：**所有动作类的父类

### 具体方法

```python
@classmethod
def PyAutoGuiInstance(cls):
    if not cls.__pyautogui:
        cls.__pyautogui = pyautogui
        return cls.__pyautogui

```

**说明**：获取PyAutoGui的Class

**方法返回**：**<class>pyautogui**

#### **PyAutoGuiInstance方法实例**：

```python
pyAuto = Aciton.PyAutoGuiInstance() 
```

​											-----------------------------分割线------------------------------

```python
@classmethod
def readImageForBase64(cls, imgSavePath=None):
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
```

**方法说明**：截图并获取该图片的Base64编码格式字符串

**方法返回**：该图片的Base64编码格式字符串

**参数说明**：

| **参数名**      | **是否必选** | **参数说明**                                         |
| --------------- | ------------ | ---------------------------------------------------- |
| **imgSavePath** | **N**        | 允许自定义截图存放地址，注：**路径的文件夹需要存在** |

#### **readImageForBase64方法实例**：

```python
Aciton.readImageForBase64()
# 获取64编码字符串
base64_str = Aciton.readImageForBase64()
# 自定义存放路径
Aciton.readImageForBase64(imgSavePath=r"D:\xxx\xxx")
```

​											-----------------------------分割线------------------------------

```python
@classmethod
def GetLoger(cls):
    if not cls.__logger:
        cls.__logger = Log.Instance()
        return cls.__logger
```

**方法说明**：获取Logger对象

**方法返回**：返回Logger对象

**参数说明**：

​					**Pass**

#### **GetLoger方法实例**：

```python
log = Aciton.GetLoger()
# 日志生成
log.debug("这是一条debug类型日志")
log.info("这是一条info类型日志")
log.warning("这是一条warning类型日志")
log.error("这是一条error类型日志")
log.critical("这是一条critical类型日志")
```

​											-----------------------------分割线------------------------------

## Click类说明：

**类说明**：在屏幕上识别图片，并且执行点击

### 具体方法

```python
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
        self.point = None
```

**方法说明**：构造方法，除了desc参数外，其余参数用字典存放

**方法返回：**

**参数说明**：

| 参数名         | 是否必选 | 数据类型 | 说明                                |
| -------------- | -------- | -------- | ----------------------------------- |
| image          | Y        | str      | 需要识别图片的路径                  |
| desc           | N        | str      | 执行该动作的描述                    |
| min_confidence | Y        | float    | 最小识别精度,不允许超过1            |
| clicks         | N        | int      | 点击的次数，默认是1次               |
| interval       | N        | float    | 设置每次点击的时间间隔， 默认0.2秒  |
| button         | N        | str      | 设置点击鼠标点击的按键，默认是左键  |
| duration       | N        | float    | 点击持续时间，默认为0秒             |
| saveImage      | N        | bool     | 每次点击后是否需要截图，默认是False |
| existElement   | N        | bool     | 点击后判断元素是否存在，默认为False |
| cycledetection | N        | bool     | 循环检测，默认为False               |
| failResponse   | N        | bool     | 允许click动作失败时继续执行任务     |

#### **Click方法实例**：

```python
arg = {
    "clicks":3,
    "interval":0.5,
    "duration":0.5,
    "existElement":True,
    "cycledetection":True,
}
click = Click("D:\xx\xx.png", 0.7, desc="点击某某图片", **arg)
```

​											-----------------------------分割线------------------------------

```python
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
```
**方法说明**：识别图片在屏幕上的坐标，返回该图片的中心坐标

**方法返回**：目标截图在屏幕上的坐标位置，失败时返回 **False**

**参数说明**：

| 参数名     | 是否必选 | 数据类型 | 说明                       |
| ---------- | -------- | -------- | -------------------------- |
| screenshot | N        | str      | 需要重新设置识别图片的路径 |

#### **PointLocateOnScreen实列：**

```python
click = Click("D:\xx\xx.png", 0.7, desc="点击某某图片")
# 获取图片在屏幕上的位置
imgPoin = click.PointLocateOnScreen()
# 获取新图片在屏幕上的位置
imgPoin = click.PointLocateOnScreen(screenshot="E:\xx\xx.png")
```

​											-----------------------------分割线------------------------------

```python
def ExitImage(self):
```

**方法说明**：检测目标是否存在。该方法配合获取坐标用，忽略

**方法返回**：存在返回：**True**，否则返回：**False**。

**参数说明**：

**实列：**

```python
pass
```

​											-----------------------------分割线------------------------------

```python
def run(self):
```

**方法说明**：启动自动化点击，当该动作失败时返回False，否则返回True

**方法返回**：返回动作运行的结果，**True**   or   **False**

**参数说明**：

```python
pass
```

**实列：**

```python
click = Click("D:\xx\xx.png", 0.7, desc="点击某某图片")
# 需要获取点击结果
rulst = click.run()
# 不需要
click.run()
```

## DetectAction类

**类说明：**在截图中检测目标，判断该元素是否存在

### 具体方法

```python
def __init__(self, desc="", **kwargs):
    super(DetectAction, self).__init__(desc)
    try:
        self.image = load_image_file(kwargs.get("image"))
        self.screenshot = load_image_file(kwargs.get("screenshot"))
        except:
            self.loger.error("CV2读取图片发生异常，异常原因是:\n" + traceback.format_exc())
            self.saveImage = kwargs.get("saveImage", False)
            self.min_confidence = kwargs.get("min_confidence", 0.7)
            self.cycledetection = kwargs.get("cycledetection", False)
```

**方法说明**：构造方法，除了desc参数外，其余参数用字典存放

**参数说明**：

| 参数名         | 是否必选 | 数据类型 | 说明                                |
| -------------- | -------- | -------- | ----------------------------------- |
| image          | Y        | str      | 需要识别小图片的路径                |
| screenshot     | Y        | str      | 被匹配识别的大图片的路径            |
| min_confidence | N        | float    | 最小识别精度,不允许超过1            |
| desc           | N        | int      | 描述                                |
| saveImage      | N        | bool     | 每次点击后是否需要截图，默认是False |
| cycledetection | N        | bool     | 循环检测，默认为False               |

#### **DetectAction方法实例**：

```python
arg = {
    "min_confidence":0.7,
    "cycledetection":True
}
image = "E:\XXX\XX.png"
screenshot = "D:\XXX\XX.png"
act = DetectAction(image, screenshot, desc="在大图片中找小图片的位置", **arg)
```

​											-----------------------------分割线------------------------------

```python
def ImageRecognition(self):
    points = None
    process = MatchImg(self.image, self.screenshot, threshod=self.min_confidence)
    if not self.cycledetection:
        points = process.get_img_center()
        if points is not None:
            self.loger.debug(f"图片识别成功，该图片在屏幕的位置是：{points[0] + 18},{points[1] + 61}")
            return points
        self.loger.debug("图片识别失败，无法找到该图片在屏幕的位置")
        return False
    confidence = 1
    while True:
        confidence = confidence - 0.1
        if points is None:
            process.set_confidence(confidence)
            points = process.get_img_center()
            else:
                self.loger.debug(f"图片识别成功，该图片在屏幕的位置是：{points[0] + 18},{points[1] + 61}")
                return points
            if confidence < self.min_confidence:
                self.loger.debug("图片识别失败，无法找到该图片在屏幕的位置")
                break
                return False
```

**方法说明**：图片对比，存在则返回该图片在目标图片中的位置的中心点

**参数说明**：Pass

#### ImageRecognition方法实例：

```python
image = "E:\XXX\XX.png"
screenshot = "D:\XXX\XX.png"
act = DetectAction(image, screenshot, desc="在大图片中找小图片的位置")
img_points = act.ImageRecognition()
```

​											-----------------------------分割线------------------------------

```python
def run(self):
```

**方法说明**：DetectAction类的启动方法

**参数说明**：

```python
pass
```

**方法实例**：

```python
参上
```

​											-----------------------------分割线------------------------------

## MouseDrag类说明

**类说明：**用于操作或者移动鼠标位置

### 具体方法

```python
def __init__(self, desc="页面", **kwargs):
```

**方法说明**：构造方法，参数用字典存放

**参数说明**：

| 参数名     | 是否必选 | 数据类型 | 说明           |
| ---------- | -------- | -------- | -------------- |
| starPoints | Y        | tuple    | 鼠标起始位置   |
| endPoints  | Y        | tuple    | 鼠标终点位置   |
| time       | N        | float    | 鼠标移动的时长 |
| desc       | N        | str      | 描述           |

#### **MouseDrag方法实例**：

```python
arg = {
    "star": (450,198),
    "end": (700,123),
    "time": 2.0
}
act = MouseDrag(desc="移动鼠标", **arg)
act.run()
```

​											-----------------------------分割线----------------------------

```python
def run(self):
```

**方法说明**：DetectAction类的启动方法

**参数说明**：

```python
pass
```

**方法实例**：

```python
参上
```

​											-----------------------------分割线------------------------------

## PasteAction类说明

**类说明：**粘贴文本

### 具体方法

```python
def __init__(self, desc="页面", **kwargs):
```

**方法说明**：构造方法，参数用字典存放

**参数说明**：

| 参数名   | 是否必选 | 数据类型 | 说明                                  |
| -------- | -------- | -------- | ------------------------------------- |
| contents | Y        | dict     | 文本内容格式为：{”contents“："xxxxx"} |
| desc     | N        | str      | 动作描述                              |

#### **PasteAction方法实例**：

```python
arg = {
    "contents": "自动化测试",
}
act = PasteAction(desc="描述", **arg)
act.run()
```

​											-----------------------------分割线----------------------------

```python
def run(self):
```

**方法说明**：DetectAction类的启动方法

**参数说明**：

```python
pass
```

**方法实例**：

```python
参上
```

​											-----------------------------分割线------------------------------

## TypeAction类说明

**类说明：**自动化按下键盘按键

### 具体方法

```python
def __init__(self, desc="页面", **kwargs):
```

**方法说明**：构造方法，参数用字典存放

**参数说明**：

**<span id="jump">额外说明</span>**：键盘映射对应的值如下
```python
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
```

| 参数名 | 是否必选 | 数据类型 | 说明                          |
| ------ | -------- | -------- | ----------------------------- |
| key    | Y        | dict     | 文本内容格式为：{”key“："f5"} |
| desc   | N        | str      | 动作描述                      |

#### **TypeAction方法实例**：

```python
arg = {
    "key": "f5",
}
act = TypeAction(desc="描述", **arg)
act.run()
```

​											-----------------------------分割线----------------------------

​											-----------------------------分割线------------------------------

```python
def run(self):
```

**方法说明**：DetectAction类的启动方法

**参数说明**：

```python
pass
```

**方法实例**：

```python
参上
```

​											-----------------------------分割线------------------------------

## TmageRecognitionAction类说明

**类说明：**使用百度Ai接口做文字识别

### 具体方法

```python
def __init__(self, desc="defunl", **kwargs):
    """
        使用百度Ai接口进行OCR识别
        :param desc: 描述
        """
    super(TmageRecognitionAction, self).__init__(desc)
    self.urlName = kwargs.get('urlName')
    self.imgFile = kwargs.get('imgFile')
    self.failResponse = kwargs.get('failResponse', False)
```

**方法说明**：构造方法，参数用字典存放

**参数说明**：

| 参数名       | 是否必选 | 数据类型 | 说明                              |
| ------------ | -------- | -------- | --------------------------------- |
| urlName      | Y        | str      | 接口名字：通用文字识别， 数字识别 |
| desc         | N        | str      | 动作描述                          |
| imgFile      | Y        | str      | 需要识别的图片的路径              |
| failResponse | N        | bool     | 允许失败时继续执行任务默认为False |

#### **TmageRecognitionAction方法实例**：

```python
arg = {
    "urlName": "数字识别",
    "imgFile": "XXX\XXX\XXX.png"
    "failResponse": True
}
act = TmageRecognitionAction(desc="描述", **arg)
```

​											-----------------------------分割线----------------------------

```python
def run(self):
    try:
        self.loger.debug(f"开始执行 图像识别Action: {self.desc}")
        image_text = BaiDu_CharacterRecognition.get_img_str(self.urlName , self.imgFile)
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

```

**方法说明**：TmageRecognitionAction类的启动方法

**方法返回：**识别成功时**返回图像中的文字**，失败时返回**True**或者**Fakse**

**参数说明**：

```python
pass
```

**方法实例**：

```python
arg = {
    "urlName": "数字识别",
    "imgFile": "XXX\XXX\XXX.png"
    "failResponse": True
}
act = TmageRecognitionAction(desc="描述", **arg)
result = act.run()
```

​											-----------------------------分割线------------------------------

# page说明

**文件夹说明：**页面类文件存放路径

### **页面类说明：**

用于封装需要执行自动化的页面元素，例如页面上的UI按钮，Tips，icon和描述等，方便调用

## 相关规则：

.py**文件命名**：**Page_Xxxx.py**

可供调用执行的页面元素**方法命名**：**def Page_Xxx(self):**

调用该类必须要执行的前置**方法命名**: **def SetUp_Xxx(self):**

## BasePage类说明

**类说明：**所有页面类应继承的父类，该类提供封装好的所有自动化方法可供便捷调用

### 具体方法

```python
def __init__(self, dataDict):
    self.DataInitialization(dataDict)
```

**方法说明**：构造方法

**参数说明**：

| 参数名   | 是否必选 | 数据类型 | 说明                                                         |
| -------- | -------- | -------- | ------------------------------------------------------------ |
| dataDict | Y        | dict     | 继承该父类要求在子类的构造函数中，给父类构造方法传递数据字典 |

#### **BasePage方法实例**：

```python
# 编写继承该父类的子类
class page_login(BasePage):
    def __init__():
        # 创建一个实例的字典变量
        self.__loginPageData = {"项目": "自动化", "人员":"柠檬果"}
        # 实例化父类构造方法，并将数据字典传递过去
        super().__init__(self.__loginPageData)
```

​											-----------------------------分割线----------------------------

```python
@classmethod
def GetLoger(cls):
    return Action.GetLoger
```

**方法说明**：返回Logger的实例对象

**方法返回**：<object>Logger

**参数说明**：

​		**Pass**

#### **GetLoger方法实例**：

```python
# 直接调用
loger = BasePage.GetLoger()
# 子类调用
class page_login(BasePage):
    def __init__(self):
        # 创建一个实例的字典变量
        self.__loginPageData = {"项目": "自动化", "人员":"柠檬果"}
        # 实例化父类构造方法，并将数据字典传递过去
        super().__init__(self.__loginPageData)
        # 调用父类GetLoger方法，获取Loger的实例对象
        self.GetLoger()

```

​											-----------------------------分割线----------------------------

```python
def DetermineTheActionTypeAndCall(self, dictKeyName, desc=""):
    self.CreateFunctionDict(dictKeyName)
    actionType = self.__actionDict.get(dictKeyName).get("type")
    actionFuction = self.ActionFunctionDict(actionType)
    if desc != "" or desc is not None:
        return actionFuction(dictKeyName, desc=desc)
    return actionFuction(dictKeyName, desc=dictKeyName)
```

**方法说明**：通过字典的type的值获取动作的类型，并对其进行相应的调用

**方法返回**：自动化动作运行的结果：**True || False**

**参数说明**：

| 参数名      | 是否必选 | 数据类型 | 说明                  |
| ----------- | -------- | -------- | --------------------- |
| dictKeyName | Y        | str      | 子类传递的字典的Key值 |
| desc        | N        | str      | 描述                  |

#### **DetermineTheActionTypeAndCall方法实例**：

```python
# 子类调用
class page_login(BasePage):
    def __init__(self):
        # 创建一个实例的字典变量
        self.__loginPageData = {"项目": "自动化", "人员":"柠檬果"}
        # 实例化父类构造方法，并将数据字典传递过去
        super().__init__(self.__loginPageData)
        # 调用父类DetermineTheActionTypeAndCall方法,并将self.__loginPageData具体的Key传进去
        self.DetermineTheActionTypeAndCall("项目", desc="自动执行项目")
```

​											-----------------------------分割线----------------------------



# **pageData说明**

### **文件夹说明：**

页面类的数据文件存放路径

### 命名规则：

**PageData_xxx.py**

## parameter.py文件说明

**文件说明**：将所有自动化动作所需的所有参数封装成方法以供便捷调用

### 具体方法

```python
def ClickActionParameters(image, min_confidence: float, clicks=1, interval=0.2, button='right', duration=0,saveImage=False, existElement=False, cycledetection=True, targetOffset=None, failResponse=False):

    parameters = {
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
    return parameters
```

**方法说明**：生成点击动作所需参数组

**方法返回**：点击动作必备参数组， <dict>parameters

**参数说明**：

| 参数名         | 数据类型 | 是否必选 | 说明                                                         |
| -------------- | -------- | -------- | ------------------------------------------------------------ |
| image          | str      | Y        | 截图的文件路径                                               |
| min_confidence | float    | Y        | 图像识别最小精度                                             |
| clicks         | int      | N        | 点击次数                                                     |
| interval       | float    | N        | 每次点击的间隔                                               |
| button         | str      | N        | 鼠标按键，默认为左键                                         |
| duration       | float    | N        | 点击持续时间                                                 |
| saveImage      | bool     | N        | 每次点击后是否需要截图                                       |
| existElement   | bool     | N        | 判断元素是否存在，默认为False                                |
| targetOffset   | tuple    | N        | 坐标偏移设置                                                 |
| cycledetection | bool     | N        | 循环检测，默认为False                                        |
| failResponse   | bool     | N        | 当操作失败或循环次数未满足跳出条件时终止任务，True则忽视失败继续执行 |

#### **ClickActionParameters方法实例**：

```python
clickActionParameters = ClickActionParameters("XXX\\XXX\\XXX.png", 0.7, cycledetection=True)
```

​											-----------------------------分割线----------------------------

```python
def DetectActionParameters(image, screenshot, min_confidence=0.7, saveImage=False, cycledetection=False):
    parameters = {"image": image,
                  "screenshot": screenshot,
                  "min_confidence": min_confidence,
                  "saveImage": saveImage,
                  "cycledetection": cycledetection,
                  "type": 'detect',
                  }
    return parameters
```

**方法说明**：生成截图中检测目标动作所需参数组

**方法返回**：截图中检测目标动作必备参数组， **<dict>parameters**

**参数说明**：

| 参数名         | 数据类型 | 是否必选 | 说明                 |
| -------------- | -------- | -------- | -------------------- |
| image          | str      | Y        | 要匹配的目标         |
| screenshot     | str      | Y        | 大截图               |
| min_confidence | int      | N        | 识别精度             |
| saveImage      | float    | N        | 是否要保存该当前截图 |
| cycledetection | str      | N        | 循环检测             |

#### **DetectActionParameters方法实例**：

```python
detectActionParameters = DetectActionParameters("XXX\\XXX\\XXX.png", "XXX\\XXX\\XXX.png", 0.7, cycledetection=True)
```

​											-----------------------------分割线----------------------------

```python
def TypeActionParameter(KeyboardButton):
    """
       自动化输入键盘按钮方法需要的内容
       """
    parameter = {
        "key": KeyboardButton,
        "type": "type",
    }
    return parameter
```

**方法说明**：自动化输入键盘按钮

**方法返回**：自动化输入键盘动作必备参数组， **<dict>parameters**

**参数说明**：

| 参数名         | 数据类型 | 是否必选 | 说明                  |
| -------------- | -------- | -------- | --------------------- |
| KeyboardButton | str      | Y        | [键盘的映射值](#jump) |

#### **TypeActionParameter方法实例**：

```python
TypeActionParameter = TypeActionParameter("enter")
```

​											-----------------------------分割线----------------------------

#### **DetectActionParameters方法实例**：

```python
detectActionParameters = DetectActionParameters("XXX\\XXX\\XXX.png", "XXX\\XXX\\XXX.png", 0.7, cycledetection=True)
```

​											-----------------------------分割线----------------------------

```python
def PasteActionParameter(contents):
    """
       自动化粘贴文本内容方法所需参数。\n contents:需要粘贴的内容。
       """
    parameter = {
        "contents": contents,
        "type": "paste",
    }
    return parameter
```

**方法说明**：生成自动化粘贴文本内容方法所需参数

**方法返回**：自动化粘贴文本内容动作必备参数组， **<dict>parameters**

**参数说明**：

| 参数名   | 数据类型 | 是否必选 | 说明               |
| -------- | -------- | -------- | ------------------ |
| contents | str      | Y        | 需要粘贴的文本内容 |

#### **PasteActionParameter方法实例**：

```python
pasteActionParameter = PasteActionParameter("自动化")
```

​											-----------------------------分割线----------------------------



```python
def DragActionParameter(start, end, time=1):
    parameters = {
        "start": start,
        "end": end,
        "time": time,
        "type": "drag",
    }
    return parameters

```

**方法说明**：生成自动化拖动鼠标动作所需参数

**方法返回**：自动化拖动鼠标动作必备参数组， **<dict>parameters**

**参数说明**：

| 参数名 | 数据类型 | 是否必选 | 说明         |
| ------ | -------- | -------- | ------------ |
| start  | tuple    | Y        | 起始坐标     |
| end    | tuple    | Y        | 终点坐标     |
| time   | float    | N        | 拖动所需时长 |

#### **PasteActionParameter方法实例**：

```python
dragActionParameter = DragActionParameter((100,101), (20,204), time=1.5)
```

​											-----------------------------分割线----------------------------





