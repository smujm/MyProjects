# coding=utf-8
from io import BytesIO

from aip import AipOcr
from selenium import webdriver, common
import urllib2
import urllib
import json
import base64
import time
from PIL import Image


import requests

# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# options = webdriver.ChromeOptions()
# # 代理ip地址
# # ip = 'http://127.0.0.1'
# # options.add_argument(('--proxy-server=' + ip))
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# # 不加载图片,加快访问速度
# # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# # ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
# driver = webdriver.Chrome(chrome_options=options)
# # 窗口最大化
# driver.maximize_window()
# # 打开登录页面
# driver.get('https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2Fhome.action%3Bjsessionid%3D52B60B95758D576BA6D401A15B31D2EA')
# time.sleep(2.8)
#
# username = "201610311232"
# password = "hellozhanjinming"
# # 给输入框赋值''
# driver.find_element_by_xpath('//*[@id="username"]').clear()
# driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div[2]/form/section[3]/div/input').clear()
# driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
# time.sleep(0.1)
# driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div[2]/form/section[3]/div/input').send_keys(password)
# time.sleep(0.12)
#
# # 获取验证码在画布中的位置''
# img_obj = driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div[2]/form/section[4]/div/div/img')
# img_url = img_obj.get_attribute('src')
# print img_url
# try:
#     data = urllib.urlopen(img_url).read() #读取图片
#     with open('QR/324.jpg', 'wb') as f:
#         f.write(data)
# except urllib.error.HTTPError as err:
#     print err



APP_ID = '21577308'
API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('./QR/get_img.jfif')

options = {
    'detect_direction': 'true',
    'language_type': 'ENG',
}

# 调用通用文字识别接口
result = client.basicGeneral(image, options)
print result
# for word in result['words_result']:
#     print word['words']
try:
    code = result['words_result'][0]['words']
except:
    code = '验证码失败'
print code
