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
import dmPython

user = 'SYSDBA'
password = 'citygis1613'
server = '106.14.243.179'
port = 5236


class database:
	def __init__(self):
		try:
			conn = dmPython.connect(
				user=user,
				password=password,
				server=server,
				port=port,
				autoCommit=True
			)
			print("数据库连接成功！")
			self.conn = conn
		except dmPython.Error as e:
			print("连接失败", str(e))
	
	def create_tb(self, sql):
		try:
			cursor = self.conn.cursor()  # 获取光标
			cursor.execute(sql)  # 执行sql
			print("创建成功")
		except dmPython.Error as e:
			print("创建失败", str(e))
		finally:
			cursor.close()  # 关闭游标
	
	def insert_tb(self, sql, data):
		try:
			cursor = self.conn.cursor()
			cursor.execute('set identity_insert "TENCENTAPI"."taobao_jd" on;')
			cursor.executemany(sql, data)
			self.conn.commit()
			print("数据插入成功")
		except dmPython.Error as e:
			self.conn.rollback()
			print("插入失败", str(e))
		finally:
			cursor.close()
	
	def select_tb(self, sql):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			result1 = cursor.fetchall()
			# print("查询全部结果：", result1)
			return result1
		except dmPython.Error as e:
			print("查询失败", str(e))
		finally:
			cursor.close()
	
	def select_tb_one(self, sql):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			result2 = cursor.fetchone()
			print("查询一条结果：", result2)
		except dmPython.Error as e:
			print("查询失败", str(e))
		finally:
			cursor.close()
	
	def select_tb_many(self, sql, count):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			result3 = cursor.fetchmany(count)
			print("查询结果：", result3)
		except dmPython.Error as e:
			print("查询失败", str(e))
		finally:
			cursor.close()
	
	def update(self, sql):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			print("修改成功")
		except dmPython.Error as e:
			print("查询失败", str(e))
		finally:
			cursor.close()


class taobao:
	def __init__(self):
		print('淘宝爬虫准备就绪!')
	
	def create_excel(self, sheet_name, row_title):
		self.f = xlwt.Workbook()
		self.sheet_info = self.f.add_sheet(sheet_name, cell_overwrite_ok=True)
		for i in range(0, len(row_title)):
			self.sheet_info.write(0, i, row_title[i])
		self.f.save('taobao.xls')
	
	def getHTMLText(self, url):
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
			# data = xlrd.open_workbook('taobao.xls')
			# table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件一般都至少有一个table
			# rowCount = table.nrows  # 获取行数，下次从这一行开始
			# m = 0  # 计数
			Seq_params = []
			shops = re.findall(r'"nick":"(.*?)"', html)
			# 'http://store.taobao.com/shop/view_shop.htm?id=3012860579%22'
			# 'https://store.taobao.com/shop/view_shop.htm?user_number_id=3012860579'
			shops_href = re.findall(r'"user_id":"([0-9]+)"', html)
			titles = re.findall(r'"raw_title":".*?"', html)
			# goods_href = re.findall(r'"detail_url":"//[^/:]+\/item.htm\?id\\u003d[0-9]*', html)
			goods_href = re.findall(r'"nid":"([0-9]+)"', html)
			prices = re.findall(r'"view_price":"[\d.]*"', html)
			
			for i in range(len(titles)):
				# data = []
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
				
				values = ('淘宝', shop, shop_href, title, good_href, price, weight, unit_price, time_str)
				Seq_params.append(values)
				# data.append(rowCount + m)
				# data.append('淘宝')
				# data.append(shop)
				# data.append(shop_href)
				# data.append(title)
				# data.append(good_href)
				# data.append(price)
				# data.append(weight)
				# data.append(unit_price)
				# data.append(time_str)
				# # 写入数据
				# for j in range(len(data)):
				# 	self.sheet_info.write(rowCount + m, j, data[j])
				# m += 1
				
				print(shop, shop_href, title, good_href, price, weight, unit_price)
			# 调用sql将数据插入数据库
			sql_jd = """
					insert into "TENCENTAPI"."taobao_jd"("平台", "店铺名称", "店铺URL", "商品名称", "商品URL", "价格", "重量", "单价(元/500g)", "获取日期") VALUES(?,?,?,?,?,?,?,?,?);
					"""
			db.insert_tb(sql_jd, Seq_params)
		except:
			print("error")
	
	# finally:
	# 	self.f.save('taobao.xls')
	
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
				print(
					'=================================正在爬取淘宝{0}---第{1}页数据================================='.format(goods,
																												 i + 1))
				self.parsePage(html)
			except:
				continue


class jd:
	def __init__(self):
		
		print('京东爬虫准备就绪!')
	
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
			# data = xlrd.open_workbook('taobao_jd.xls')
			# table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件一般都至少有一个table
			# rowCount = table.nrows  # 获取行数，下次从这一行开始
			# m = 0  # 计数
			Seq_params = []
			for td in tds:
				# data = []
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
				
				values = (
					'京东', str(shop_name), str(shop_href), str(good_name), str(good_href), float(price), str(weight),
					float(unit_price), str(time_str))
				Seq_params.append(values)
				
				# data.append(rowCount + m)
				# data.append('京东')
				# data.append(shop_name)
				# data.append(shop_href)
				# data.append(good_name)
				# data.append(good_href)
				# data.append(price)
				# data.append(weight)
				# data.append(unit_price)
				# data.append(time_str)
				#
				# # 写入数据
				# for j in range(len(data)):
				# 	self.sheet_info.write(rowCount + m, j, data[j])
				# m += 1
				
				print(shop_name, shop_href, good_name, good_href, price, weight, unit_price)
				# print(type(shop_name), type(shop_href), type(good_name), type(good_href), type(price), type(weight),
				# 	  type(unit_price))
				
			# 调用sql将数据插入数据库
			print(len(Seq_params))
			sql_jd = """
						insert into "TENCENTAPI"."taobao_jd"("平台", "店铺名称", "店铺URL", "商品名称", "商品URL", "价格", "重量", "单价(元/500g)", "获取日期") VALUES(?,?,?,?,?,?,?,?,?);
						"""
			db.insert_tb(sql_jd, Seq_params)
		except:
			print("error---警告")
	
	# finally:
	# 	self.f.save('taobao_jd.xls')
	
	def search(self, good_name):
		goods = good_name  # 商品名称
		start_url = 'https://search.jd.com/Search?keyword={}'.format(goods)
		start_html = self.getHTMLText(start_url)
		depth = int(re.findall('page_count:"([0-9]*)"', start_html)[0])
		for i in range(1, depth + 1):
			try:
				print('=================================正在爬取京东{0}---第{1}页数据================================='.format(
					goods, i))
				url = 'https://search.jd.com/Search?keyword={0}&page={1}&scrolling=y'.format(
					goods, i)
				html = self.getHTMLText(url)
				# print(html)
				html = etree.HTML(html)
				self.parsePage(html)
			except:
				continue


if __name__ == '__main__':
	db = database()
	tb = taobao()
	jd = jd()
	sql = """
	select WEBNAME,PROGRAMNAME from "TENCENTAPI"."SPIDERINDEX" where (WEBNAME = '京东' or WEBNAME = '淘宝')and FLAG = 0
	"""
	result = db.select_tb(sql)
	print(result, len(result))
	for i in range(len(result)):
		if result[i][0] == '淘宝':  # 淘宝
			tb.search(result[i][1])
			sql_update = """
			update "TENCENTAPI"."SPIDERINDEX" set FLAG = 1 where WEBNAME = '淘宝' and PROGRAMNAME = '{}'
			""".format(result[i][1])
			db.update(sql_update)
		else:  # 京东
			jd.search(result[i][1])
			sql_update = """
			update "TENCENTAPI"."SPIDERINDEX" set FLAG = 1 where WEBNAME = '京东' and PROGRAMNAME = '{}'
			""".format(result[i][1])
			db.update(sql_update)

# tb = taobao()
# taobao_name = '8424西瓜'
# rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
# tb.create_excel(taobao_name, rowTitle)
# tb.search(taobao_name)
#
# jds = jd()
# name = '8424西瓜'
# rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
# jds.create_excel(name, rowTitle)
# jds.search(name)
