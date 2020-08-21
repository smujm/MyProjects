# coding=utf-8

import base64
import os
import random
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据

import re
import requests
import xlwt
import xlrd
from lxml import etree
from PIL import Image
import parsel

headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'api_uid=CiWW2l8ZKUZHJABXxXWRAg==; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F84.0.4147.89%20Safari%2F537.36; _nano_fp=XpdbnpTJn0TJn5TaX9_UgZWWSkOGx9zF5qDHLLNT; PDDAccessToken=2H7VNDV5SMZEE7THVERQEZN6GV5QVL2A5TR7TO44U3VLCTXCMSDQ1114596; pdd_user_id=9965051753797; pdd_user_uin=SPJEITWABOMXO52OK5GXTFAMMM_GEXDA; webp=1; vds=gaKpVYJcvdqfzcFBMCVZZCVqqdpuHDXfWChBHhXdJZvfFhzhrfkDpqJevBMf; JSESSIONID=9DCFB06237C0DD9DD5BF9DC0F4B7901B',
	'DNT': '1',
	'Host': 'yangkeduo.com',
	'Referer': 'http://yangkeduo.com/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}

cookies = {
	'name': 'Cookie',
	'value': 'api_uid=CiWW2l8ZKUZHJABXxXWRAg==; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F84.0.4147.89%20Safari%2F537.36; _nano_fp=XpdbnpTJn0TJn5TaX9_UgZWWSkOGx9zF5qDHLLNT; webp=1; pdd_user_id=9965051753797; PDDAccessToken=V3JQSKJHB4EPZAD5ZXJCLHZR4SOCXEKZ4FQWPM5XEUQXMDZ2GJRA1114596; pdd_user_uin=SPJEITWABOMXO52OK5GXTFAMMM_GEXDA; JSESSIONID=37B492B33685F3FFCA80992242F87B04; vds=gaMLXIztcEZnqornzOCiCaYQvtcyvIHOrQXthQzoXGftYNfPYNpnpapPqmvP', }


# f = open(r'cookies.txt', 'r')  # 打开所保存的cookies内容文件
# cookies = {}  # 初始化cookies字典变量
# for line in f.read().split(';'):  # 按照字符：进行划分读取
# 	# 其设置为1就会把字符串拆分成2份
# 	name, value = line.strip().split('=', 1)
# 	cookies[name] = value  # 为字典cookies添加内容

class pdd:
	def __init__(self, good_name):
		# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
		# options = webdriver.ChromeOptions()
		options = webdriver.FirefoxOptions()
		# 代理ip地址
		# ip = 'http://127.0.0.1'
		# options.add_argument(('--proxy-server=' + ip))
		# options.add_experimental_option('excludeSwitches', ['enable-automation'])
		
		# 不加载图片,加快访问速度
		# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
		# ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
		self.driver = webdriver.Firefox()
		
		# 窗口最大化
		self.driver.maximize_window()
		# 打开登录页面
		self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
		
		self.driver.get(
			'http://yangkeduo.com/')
		# time.sleep(2.8)
		self.driver.delete_all_cookies()
		self.driver.add_cookie({
			# 'domain': '.yangkeduo.com',  # 此处xxx.com前，需要带点
			'name': cookies['name'],
			'value': cookies['value'],
			# 'path': '/',
			# 'expires': "",
			# 'httpOnly': False,
			# 'HostOnly': False,
			# 'Secure': False
		})
		self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
		self.driver.get(
			'http://yangkeduo.com/search_result.html?search_key=' + good_name)
	
	# 模拟向下滑动
	def swipe_down(self, second):
		for i in range(int(second / 0.1)):
			js = "var q = document.documentElement.scrollTop=" + str(300 + 200 * i)
			js2 = 'window.scrollTo(0,document.body.scrollHeight);'
			self.driver.execute_script(js)  # 使用js代码模拟滑动
			time.sleep(0.3)
		time.sleep(0.2)
	
	def get_info(self):
		try:
			html = self.driver.page_source
			print(html)
			selector = parsel.Selector(html)
			time.sleep(0.2)
			lis = selector.css('div._1yfk_Hvb._2bxXLRpP').getall()
			for li in lis:
				good_name = li.css('')
			goods_name = re.findall(
				'<div class="pHbSR-xp _1cP_KihG" style="margin-bottom:.03rem;height:.18rem">(.*?)</div>', html)
			goods_id = re.findall('goods_id=([0-9]*)', html)
			prices = re.findall('<span class="p-BSHpjB">(.*?)</span>', html)
			print(len(goods_name))
			m = 1
			for i in range(len(goods_name)):
				good_name = re.sub('<img class=.*>', '', goods_name[i])
				price = prices[i]
				good_id = 'http://yangkeduo.com/goods.html?goods_id=' + goods_id[i]
				# print(good_name, good_id, price)
				flag = True
				try:
					while flag:
						time.sleep(0.1)
						self.driver.get(good_id)
						self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
						good_html = self.driver.page_source
						time.sleep(0.4)
						if self.driver.current_url == good_id:  # 判断是否进入成功
							flag = False
							mall_name = re.findall('"mallName":"(.*?)"', good_html)
							mall_name = mall_name[0] if len(mall_name) > 0 else ''
							mall_id = re.findall('mall_id=([0-9]*)', good_html)
							mall_id = 'http://yangkeduo.com/mall_page.html?mall_id=' + mall_id[0] if len(
								mall_id) > 0 else ''
							
							print(m, mall_name, mall_id, good_name, good_id, price)
							m += 1
							time.sleep(0.6)
							self.driver.back()
							self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
						else:
							time.sleep(40)
							self.driver.back()
				except Exception as e:
					print("读取店铺失败", e)
		except Exception as e:
			print("进入网页失败", e)


if __name__ == '__main__':
	pd = pdd("8424西瓜")
	pd.swipe_down(3)
	pd.get_info()
