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
from lxml import etree
from PIL import Image



class taobao:
	def __init__(self):
		print('启动淘宝爬虫!')
	
	def create_excel(self, sheet_name, row_title):
		self.f = xlwt.Workbook()
		self.sheet_info = self.f.add_sheet(sheet_name, cell_overwrite_ok=True)
		for i in range(0, len(row_title)):
			self.sheet_info.write(0, i, row_title[i])
		self.f.save('taobao.xls')
	
	def getHTMLText(self, url):
		f_headers = {
			'authority': 's.taobao.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
			'sec-fetch-user': '?1',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'referer': 'https://www.taobao.com/?spm=a230r.1.1581860521.1.44436fbeX7fwH0',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cookie': 'cna=88pKFuAt2QMCAWVY2F3T01h1; cookie2=17b6ac1692df0c736e28c4efcb5ee79a; t=447830b48ce5b736833b764b92809ff2; _tb_token_=715e9a3b15e9; v=0; thw=cn; unb=2082742785; uc3=id2=UUjZcE2LH1EDaQ%3D%3D&vt3=F8dBxdgrdaJJ5KSVCHo%3D&nk2=3RdKdRwto8z8PA%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D; csg=4e1f7957; lgc=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; cookie17=UUjZcE2LH1EDaQ%3D%3D; dnk=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; skt=ec673df4ff6e43ac; existShop=MTU3Nzk1NTE4OQ%3D%3D; uc4=nk4=0%4035zQA7TpoK2iybOgdcGoulv7b5aB&id4=0%40U2o7m3X6u2tj46bVVY%2FxUsnfO1hN; tracknick=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; _cc_=UtASsssmfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E5%A4%8F5b; _nk_=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; cookie1=VvaIEm24hLue5D5qhr2avxolnb%2FaZNMx4VbmE815fEA%3D; enc=PrShuTMeEH7c84JZDvhxe%2BofqKPYVhiahZMb778yWEXwjAX4aS4mDthKut6ysn9Le5wPLAhqNs6w80YwVrDGZw%3D%3D; mt=ci=46_1; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie14=UoTbmhmo%2BDP65Q%3D%3D; JSESSIONID=17E0512B44E7C08C2078A64DE1792A91; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; l=dBrD7EMqqZ0JhEKsBOCwnurza77tsIRAguPzaNbMi_5aZ6LsLT7OoX_6cFp6cjWfTLTB4cPM8Rp9-etkmEy06Pt-g3fPixDc.; isg=BMjIpqdQAuYKqW2s7p0pvmNimTbacSx7WbTdyIJ5EsM2XWjHKobICwRf0XWI7eRT',
		}
		f_headers1 = {
			'authority': 's.taobao.com',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
			'sec-fetch-user': '?1',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'navigate',
			'referer': 'https://www.taobao.com/?spm=a230r.1.1581860521.1.44436fbeX7fwH0',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cookie': 'thw=cn; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=EC4y8pYcHKNH3mt4PaC2B; mt=ci=0_0; tracknick=; cna=LBaDF7fMtlkCAWVQzVmZadAL; t=016e01511eed975d01ca996d95a5b0de; v=0; _m_h5_tk=c021e6e7411203add8dd2ee4dc8cc4a9_1596426267345; _m_h5_tk_enc=3cc04de7740cb561ea73f98413c1cae4; cookie2=1c383cec613c946bfdfbda77c2bb87aa; _samesite_flag_=true; UM_distinctid=173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4; _tb_token_=eea13e13e6b3d; tfstk=cCxFBo29hDneUzSSkMszAOcvFP1dC75h1uXV-EEUYfw3Sfncgp50w7BiC7BlIsnG-; l=eBSNAONVOE6zAMIkBOfanurza77OSIRYmuPzaNbMiOCPOu5e5ONFWZou6jTwC3GVh6yMR3oIr-vbBeYBqI2wsWRKe5DDwQHmn; isg=BCUlE26JlgP8SvJmu8QfL40VNOFfYtn0cwz99icK4dxrPkWw77LpxLPcyKJIOvGs',
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
			data = xlrd.open_workbook('taobao.xls')
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
		start_url = 'https://s.taobao.com/search?q=' + goods
		home_page = self.getHTMLText(start_url)
		total_page = re.findall('"totalPage":([0-9]*)', home_page)
		total_page = int(total_page[0])
		# print(total_page)[]
		for i in range(total_page):
			try:
				url = start_url + '&s=' + str(44 * i)
				html = self.getHTMLText(url)
				print('=================================正在爬取第{}页数据================================='.format(i + 1))
				self.parsePage(html)
			except:
				continue


class jd:
	def __init__(self):
		
		print('启动京东爬虫!')
	
	def create_excel(self, sheet_name, row_title):
		self.f = xlwt.Workbook()
		self.sheet_info = self.f.add_sheet(sheet_name, cell_overwrite_ok=True)
		for i in range(0, len(row_title)):
			self.sheet_info.write(0, i, row_title[i])
		self.f.save('taobao_jd.xls')
	
	def getHTMLText(self, url):
		f_headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
		}
		
		try:
			r = requests.get(url=url, headers=f_headers)
			r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
			r.encoding = r.apparent_encoding
			return r.text
		except:
			return ""
	
	def parsePage(self, html):
		try:
			tds = html.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div/li/div')
			# 打开excel文件
			data = xlrd.open_workbook('taobao_jd.xls')
			table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件一般都至少有一个table
			rowCount = table.nrows  # 获取行数，下次从这一行开始
			m = 0  # 计数
			for td in tds:
				data = []
				shop_name = td.xpath('./div[5]/span/a/@title')
				shop_name = shop_name[0] if len(shop_name) > 0 else ''
				shop_href = td.xpath('./div[5]/span/a/@href')
				shop_href = 'https:' + shop_href[0] if len(shop_href) > 0 else ''
				good_name = td.xpath('./div[3]/a/em')
				good_name = good_name[0].xpath('string(.)') if len(good_name) > 0 else ''
				good_name = good_name.replace(' ', '').replace("\n", "").replace("\r", "")
				good_href = td.xpath('./div[3]/a/@href')
				good_href = 'https:' + good_href[0] if len(good_href) > 0 else ''
				price = td.xpath('./div[2]/strong/i/text()')
				price = price[0] if len(price) > 0 else ''
				good_html = self.getHTMLText(good_href)
				# s_good_html = etree.HTML(good_html)
				weight = re.findall('商品毛重：(.*?)</li>', good_html)  # <dt>净含量</dt><dd>(.*?)</dd>
				# print(good_href, weight)
				if len(weight) > 0:
					weight = weight[0]
				else:
					weight = re.findall('<dt>净含量</dt><dd>(.*?)</dd>', good_html)
					weight = weight[0] if len(weight) > 0 else 1
				
				if weight.find('kg') == -1:  # 没找到
					unit = float(weight.replace('kg', '').replace('g', ''))
				else:
					unit = float(weight.replace('kg', '').replace('g', '')) * 1000  # kg-->g
				unit_price = float(price) / (unit / 500)
				unit_price = round(unit_price, 2)  # 保留两位小数
				curr_time = datetime.datetime.now()  # 获取当前时间
				time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
				
				data.append(rowCount + m)
				data.append('京东')
				data.append(shop_name)
				data.append(shop_href)
				data.append(good_name)
				data.append(good_href)
				data.append(price)
				data.append(weight)
				data.append(unit_price)
				data.append(time_str)
				
				# 写入数据
				for j in range(len(data)):
					self.sheet_info.write(rowCount + m, j, data[j])
				m += 1
				
				print(shop_name, shop_href, good_name, good_href, price, weight, unit_price)
			
		except:
			print("error---警告")
		finally:
			self.f.save('taobao_jd.xls')
	
	def search(self, good_name):
		goods = good_name  # 商品名称
		start_url = 'https://search.jd.com/Search?keyword={}'.format(goods)
		start_html = self.getHTMLText(start_url)
		depth = int(re.findall('page_count:"([0-9]*)"', start_html)[0])
		for i in range(1, depth + 1):
			try:
				print('=================================正在爬取第{}页数据================================='.format(i))
				url = 'https://search.jd.com/Search?keyword={0}&page={1}&scrolling=y'.format(
					goods, i)
				html = self.getHTMLText(url)
				# print(html)
				html = etree.HTML(html)
				self.parsePage(html)
			except:
				continue


if __name__ == '__main__':
	tb = taobao()
	taobao_name = '8424西瓜'
	rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
	tb.create_excel(taobao_name, rowTitle)
	tb.search(taobao_name)
	
	
	
	jds = jd()
	name = '8424西瓜'
	rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
	jds.create_excel(name, rowTitle)
	jds.search(name)
