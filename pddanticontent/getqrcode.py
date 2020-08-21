#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re
import requests
import json
import time
import ssl
from requests.auth import HTTPBasicAuth

BaseUrl_anticontent = "http://127.0.0.1:8000/get_anti_content"
BaseUrl_main = "https://mms.pinduoduo.com/login?redirectUrl=https%3A%2F%2Fmms.pinduoduo.com%2Fhome%2F"
BaseUrl_servertime = "https://api.pinduoduo.com/api/server/_stm"
BaseUrl_qrcode = "https://mms.pinduoduo.com/janus/api/scan/login/qrcode"
BaseUrl_query = "https://mms.pinduoduo.com/janus/api/scan/login/query"
def get_anti_content():
    anticontent_response = requests.get(BaseUrl_anticontent)
    anticontent = json.loads(anticontent_response.text)['anti_result']
    return anticontent
    print(anticontent)

headers1 = {
    "Host": "mms.pinduoduo.com",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://mms.pinduoduo.com/login?redirectUrl=https%3A%2F%2Fmms.pinduoduo.com%2Fhome%2F",
    "Content-Type": "application/json;charset=UTF-8",
    "Anti-Content":get_anti_content(),
    "Origin": "https://mms.pinduoduo.com",
    "Content-Length": "2",
    "Connection": "keep-alive",
    "Cookie": "api_uid=rBQRx16NJkUiGhjWWf0kAg==; _nano_fp=XpdJn5Xol0E8l0donC_MOhWvjHE5vwY5Jt~SAoVJ",
    "TE": "Trailers"
}

def get_query_new_header():
    header = {
        "Host": "mms.pinduoduo.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://mms.pinduoduo.com/login?redirectUrl=https%3A%2F%2Fmms.pinduoduo.com%2Fhome%2F",
        "Content-Type": "application/json;charset=UTF-8",
        "Anti-Content":get_anti_content(),
        "Origin": "https://mms.pinduoduo.com",
        "Content-Length": "59",
        "Connection": "keep-alive",
        "Cookie": "api_uid=rBQRx16NJkUiGhjWWf0kAg==; _nano_fp=XpdJn5Xol0E8l0donC_MOhWvjHE5vwY5Jt~SAoVJ",
        "TE": "Trailers"
    }
    return header



time.sleep(1)

#获取登录二维码

#qrcode_response = requests.get(BaseUrl_servertime , headers = headers4)
#print(qrcode_response.text)
qrcode_response = requests.post(BaseUrl_qrcode  , headers = headers1,data =json.dumps({}))
print("-----------------获取登录二维码地址-------------------")
print(qrcode_response.text)
print("----------------------------------------------------")
#查询二维码登录状态

qrcode_url = json.loads(qrcode_response.text)['result']['uri']
mydatas = qrcode_url.split("data=")
mydata = json.dumps({"data":mydatas[1]})

time.sleep(3)

while True:
    query_response = requests.post(BaseUrl_query  ,headers = get_query_new_header() ,data =mydata)
    print(query_response.text)
    time.sleep(3)


#qrcode_response = requests.post(BaseUrl_qrcode  , headers = headers3,data = data,verify=False)
#print(qrcode_response.text)

#ssl._create_default_https_context = ssl._create_unverified_context
#qrcode_response = requests.post(BaseUrl_qrcode  , headers = headers,data = data,verify=False)
#print(qrcode_response.text)

