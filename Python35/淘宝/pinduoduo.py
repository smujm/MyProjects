# coding=utf-8
import base64
import os
import random
import sys
import time
import datetime
import parsel
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据

import re
import requests
import xlwt
import xlrd
import execjs
from lxml import etree
from PIL import Image


class taobao:
	def __init__(self):
		print('启动拼多多爬虫!')
	
	def getHTMLText(self, url):
		
		f_headers1 = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': 'api_uid=CiWW2l8ZKUZHJABXxXWRAg==; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F84.0.4147.89%20Safari%2F537.36; _nano_fp=XpdbnpTJn0TJn5TaX9_UgZWWSkOGx9zF5qDHLLNT; webp=1; pdd_user_id=9965051753797; PDDAccessToken=TV5GCU2GOAHE3HJ64CCUAB3NOX3O7JGL3Z2GNC7YF3XRZYVHICMA1114596; pdd_user_uin=SPJEITWABOMXO52OK5GXTFAMMM_GEXDA; vds=gaLLNImyyaoPyGbaQnaNitEItLnitnGIIEiPybEItQGQmmNObmQIyPEbIGQI; JSESSIONID=4819FB3E6A67D856369DE4CC62EF2344',
			'DNT': '1',
			'Host': 'yangkeduo.com',
			'Referer': 'http://yangkeduo.com/',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
		}
		
		try:
			r = requests.get(url=url, headers=f_headers1, timeout=20)
			r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
			# print(r.raise_for_status())
			r.encoding = r.apparent_encoding
			return r.text
		except:
			return ""
	
	def parsePage(self, html):
		try:
			data = xlrd.open_workbook('pinduoduo.xls')
			table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件一般都至少有一个table
			rowCount = table.nrows  # 获取行数，下次从这一行开始
			m = 0  # 计数
			
			shops = re.findall(r'"nick":"(.*?)"', html)
			# 'http://store.taobao.com/shop/view_shop.htm?id=3012860579%22'
			# 'https://store.taobao.com/shop/view_shop.htm?user_number_id=3012860579'
			shops_href = re.findall(r'"user_id":"([0-9]+)"', html)
			titles = re.findall(r'"raw_title":".*?"', html)
			# goods_href = re.findall(r'"detail_url":"//[^/:]+\/item.htm\?id\\u003d[0-9]*', html)
			goods_href = re.findall(r'"nid":"([0-9]+)"', html)
			prices = re.findall(r'"view_price":"[\d.]*"', html)
			
			for i in range(len(titles)):
				data = []
				shop = shops[i]
				shop_href = 'https://store.taobao.com/shop/view_shop.htm?user_number_id=' + shops_href[i]
				good_href = 'https://item.taobao.com/item.htm?id=' + goods_href[i]
				title = eval(titles[i].split(':')[1])
				price = eval(prices[i].split(':')[1])  # eval去除两端的单引号
				try:
					while (True):
						good_html = self.getHTMLText(good_href)
						if good_html == '':
							time.sleep(10)
							continue
						else:
							break
					
					if good_html.find('净重') != -1:
						weight = re.findall('净重<\/span>([0-9]*)g', good_html)
					elif good_html.find('净含量') != -1:
						weight = re.findall('<dd>([0-9]*)g<\/dd>', good_html)
					elif good_html.find('重量') != -1:
						weight = float(re.findall('<dd><em>(.*?)<\/em>kg<\/dd>', good_html)) * 1000
					else:
						weight = ''
				
				except Exception as e:
					print('重量出错', e)
				if weight == '':
					unit_price = ''
				else:
					weight = weight[0] if len(weight) > 0 else '1000'
					unit_price = float(price) / (float(weight) / 500)
					unit_price = round(unit_price, 2)
					weight = weight + 'g'
				
				curr_time = datetime.datetime.now()  # 获取当前时间
				time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
				data.append(rowCount + m)
				data.append('淘宝')
				data.append(shop)
				data.append(shop_href)
				data.append(title)
				data.append(good_href)
				data.append(price)
				data.append(weight)
				data.append(unit_price)
				data.append(time_str)
				# 写入数据
				for j in range(len(data)):
					self.sheet_info.write(rowCount + m, j, data[j])
				m += 1
				
				print(shop, shop_href, title, good_href, price, weight, unit_price)
		except:
			print("error")
		finally:
			self.f.save('taobao.xls')
	
	def search(self, good_name):
		goods = good_name  # 商品名称
		start_url = 'http://yangkeduo.com/search_result.html?search_key=' + goods
		home_page = self.getHTMLText(start_url)
		print(home_page)
		# total_page = re.findall('"totalPage":([0-9]*)', home_page)
		# total_page = int(total_page[0])
		# # print(total_page)[]
		# for i in range(total_page):
		# 	try:
		# 		url = start_url + '&s=' + str(44 * i)
		# 		html = self.getHTMLText(url)
		# 		print('=================================正在爬取第{}页数据================================='.format(i + 1))
		# 		self.parsePage(html)
		# 	except:
		# 		continue


if __name__ == '__main__':
	tb = taobao()
	taobao_name = '8424西瓜'
	rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
	tb.create_excel(taobao_name, rowTitle)
	tb.search(taobao_name)
	
