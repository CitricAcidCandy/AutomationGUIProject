# -*- coding: utf-8 -*-
# encoding:utf-8
import requests
import base64

request_url = {
    "通用文字识别": "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic",
    "数字识别": "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
}


def get_access_token():
    headers = {
        b'Content-Type': 'application/json;charset=UTF-8'
    }
    params = {
        'client_id': 'xxx',
        'client_secret': 'xxx',
        'grant_type': 'xxx',
    }

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    url = f'https://aip.baidubce.com/oauth/2.0/token'
    response = requests.post(url, params=params, headers=headers)
    if response:
        return response.json()


def get_img_str(urlName, imgfile):
    url = request_url.get(urlName)
    # 二进制方式打开图片文件
    f = open(imgfile, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_access_token().get('access_token')
    url = url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=params, headers=headers)
    if response:
        return response.json().get('words_result')

