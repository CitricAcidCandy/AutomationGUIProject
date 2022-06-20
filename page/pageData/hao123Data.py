# -*- coding: utf-8 -*-
from config.config import Config
from page.pageData.parameter import *

Hao123Param = {
    "btn_hao123": ClickActionParameters(Config.imgPath + "\\hao123\\btn_hao123.png", 0.7, cycledetection=True),
    "btn_bilibili": ClickActionParameters(Config.imgPath + "\\hao123\\btn_bilibili.png", 0.7, cycledetection=True),
    "btn_bilibili_login": ClickActionParameters(Config.imgPath + "\\hao123\\btn_bilibili_login.png", 0.7,
                                                cycledetection=True),
    "icon_bilibili_account": ClickActionParameters(Config.imgPath + "\\hao123\\icon_bilibili_account.png", 0.7,
                                                   cycledetection=True, targetOffset=(80, 0), interval=0.5, clicks=1),
    "icon_bilibili_password": ClickActionParameters(Config.imgPath + "\\hao123\\icon_bilibili_password.png", 0.7,
                                                    cycledetection=True, targetOffset=(80, 0), interval=0.5, clicks=1),
    "btn_login": ClickActionParameters(Config.imgPath + "\\hao123\\btn_login.png", 0.7, cycledetection=True),
    "key_f5": TypeActionParameter("f5"),
    "key_tab": TypeActionParameter("tab"),
}

# 登录的账号数据
ddt_LoginData = [
    {"username": "是否是打发士大夫", "password": "123123", "expected_Results": False},
    {"username": "123123", "password": "123123", "expected_Results": False},
]

# 登录的自动化步骤
login_ActionLsit = ["btn_hao123", "btn_bilibili", "btn_bilibili_login", "icon_bilibili_account", "username", "key_tab",
                    "icon_bilibili_password", "password", "btn_login"]
