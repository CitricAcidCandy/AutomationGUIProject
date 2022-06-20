# -*- coding: utf-8 -*-
import random

from page.pageData.parameter import *
from config.config import Config

LoginPageData = {
    "btn_account": ClickActionParameters(Config.imgPath + "\\Login\\btn_account.png", 0.7, cycledetection=True),
    "btn_Enter": ClickActionParameters(Config.imgPath + "\\Login\\btn_Enter.png", 0.7, cycledetection=True,
                                       failResponse=True),
    "btn_UsernameFrame": ClickActionParameters(Config.imgPath + "\\Login\\UsernameFrame.png", 0.7,
                                               cycledetection=True, targetOffset=(50, 0), interval=0.5, clicks=1),
    "btn_PasswordFrame": ClickActionParameters(Config.imgPath + "\\Login\\PasswordFrame.png", 0.7,
                                               cycledetection=True, targetOffset=(50, 0), interval=0.5, clicks=1),
    "StartGame_You": ClickActionParameters(Config.imgPath + "\\Login\\btn_StartGame_You.png", 0.7,
                                           cycledetection=True),
    "btn_register": ClickActionParameters(Config.imgPath + "\\Login\\btn_register.png", 0.7,
                                          cycledetection=True),
    "btn_register_OrdinaryAccount": ClickActionParameters(Config.imgPath + "\\Login\\btn_register_OrdinaryAccount.png",
                                                          0.7, cycledetection=True),
    "btn_register_finish": ClickActionParameters(Config.imgPath + "\\Login\\btn_register_finish.png",
                                                 0.7, cycledetection=True),
    "btn_PropZoom": ClickActionParameters(Config.imgPath + "\\Login\\btn_PropZoom.png",
                                          0.7, cycledetection=True),
    "btn_Settings": ClickActionParameters(Config.imgPath + "\\Login\\btn_Settings.png",
                                          0.7, cycledetection=True),
    "btn_ChangeRole": ClickActionParameters(Config.imgPath + "\\Login\\btn_ChangeRole.png",
                                            0.7, cycledetection=True),
    "btn_Role_4019_019": ClickActionParameters(Config.imgPath + "\\Login\\btn_Role_4019_019.png",
                                               0.7, cycledetection=True),
    "btn_SeverList": ClickActionParameters(Config.imgPath + "\\Login\\btn_SeverList.png",
                                           0.7, cycledetection=True, failResponse=True),
    "btn_NetworkStatus": ClickActionParameters(Config.imgPath + "\\Login\\btn_NetworkStatus.png",
                                               0.7, cycledetection=True),
    "tips_NetworkStatus_Info": ClickActionParameters(Config.imgPath + "\\Login\\tips_NetworkStatus_Info.png",
                                                     0.7, cycledetection=True),
    "btn_SeverList_TestSever": ClickActionParameters(Config.imgPath + "\\Login\\btn_SeverList_TestSever.png",
                                                     0.7, cycledetection=True),
    "btn_SeverList_TestSever_41": ClickActionParameters(Config.imgPath + "\\Login\\btn_SeverList_TestSever_41.png",
                                                        0.7, cycledetection=True),
    "tips_TmageRecognition_NetworkInfo": TmageRecognitionAction("通用文字识别",
                                                                Config.log_ScreenshotPath + "\\NetworkInfo.png"),
    "key_enter": TypeActionParameter("enter"),
    "key_f5": TypeActionParameter("f5"),

}

# 登录的账号数据
ddt_LoginData = [
    {"username": "test004019", "password": "123456", "expected_Results": True},
    {"username": "", "password": "12346", "expected_Results": False},
    {"username": "test004019", "password": "", "expected_Results": False},
    {"username": "是否是打发士大夫", "password": "123123", "expected_Results": False},
    {"username": "", "password": "", "expected_Results": False}
]

# 注册的账号数据
ddt_registerData = [
    {"username": "test" + str(random.randint(100000, 900000)), "password": "123456", "password1": "123456",
     "expected_Results": True},
    {"username": "test004019", "password": "123456", "password1": "123456", "expected_Results": False},
    {"username": "", "password": "", "password1": "", "expected_Results": False},
    {"username": "test004019", "password": "123456", "password1": "", "expected_Results": False},
    {"username": "test004019", "password": "", "password1": "123456", "expected_Results": False},
    {"username": "阿凡达士大夫", "password": "123456", "password1": "123456", "expected_Results": False},
    {"username": "", "password": "123456", "password1": "123456", "expected_Results": False},
]

# 登录的自动化步骤
login_ActionLsit = ["btn_account", "btn_UsernameFrame", "username", "key_enter", "btn_PasswordFrame", "password",
                    "key_enter", "StartGame_You"]
# 切换角色自动化步骤
login_ChangeRoleActionLsit = login_ActionLsit + ["btn_PropZoom", "btn_Settings", "btn_ChangeRole", "btn_SeverList",
                                                 "btn_Role_4019_019"]
# 登录的自动化步骤_DDT
ddt_login_ActionLsit = ["btn_account", "btn_UsernameFrame", "username", "key_enter", "btn_PasswordFrame", "password",
                        "key_enter", "StartGame_You"]
# 注册的自动化步骤_DDT
ddt_register_ActionLsit = ["btn_account", "btn_register", "btn_register_OrdinaryAccount",
                           "btn_UsernameFrame", "registerUse", "key_enter", "btn_PasswordFrame", "registerUsePwd",
                           "key_enter", "again", "registerAgainPwd", "key_enter", "btn_register_finish",
                           "StartGame_You"]

# 自动选择体服41的步骤配置
login_SwitchSever_Test41 = ["btn_SeverList", "btn_SeverList_TestSever", "btn_SeverList_TestSever_41"]
