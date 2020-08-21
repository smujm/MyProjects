import re
import requests
import xlwt
import xlrd
import parsel
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据
import time
from lxml import etree
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
			cursor.execute('set identity_insert "TENCENTAPI"."COMPANY_URL" on;')
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


class aiqycha:
	def __init__(self):
		# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
		options = webdriver.ChromeOptions()
		# 代理ip地址
		ip = 'http://211.144.213.145:80'
		options.add_argument(('--proxy-server=' + ip))
		options.add_experimental_option('excludeSwitches', ['enable-automation'])
		# 不加载图片,加快访问速度
		options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
		# ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
		self.driver = webdriver.Chrome(chrome_options=options)
		
		# 窗口最大化
		self.driver.maximize_window()
		# 打开登录页面
		self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
		self.driver.get(
			'https://aiqicha.baidu.com/')
	
	def getTables(self):
		excel = xlrd.open_workbook(r'company.xlsx')
		sheetNames = excel.sheet_names()
		print('sheetNames:', sheetNames)
		# 循环从sheetNames中读取sheet表，返回的是sheet的内存地址
		for sheet in sheetNames:
			table = excel.sheet_by_name(sheet)
		print('table:', table)
		return table
	
	def getData(self, sheets):
		self.data = []
		for i in range(0, sheets.nrows):
			row_content = sheets.row_values(i)
			self.data.append(row_content)
		# data.append(dict(zip(sheets.row_values(i))))
		
		print('读取的data:', self.data)
	
	def write_sheet(self, new_table, datas):
		for i in range(len(datas)):
			row_content = datas[i]
			print(row_content)
			for j in range(len(row_content)):
				new_table.write(i, j, row_content[j])
	
	def input(self):
		CoUrls = []
		for name in self.data:
			href = ''
			try:
				# 找出输入框位置
				self.driver.find_element_by_xpath('//*[@id="aqc-search-input"]').send_keys(name)
				self.driver.find_element_by_xpath('//*[@id="aqc-search-input"]').send_keys(Keys.ENTER)
				html = self.driver.page_source		# 获取网页
				# print(html)
				selector = parsel.Selector(html)
				lis = selector.css('div.items')
				href = lis[0].css('div > h3 > a::attr(href)').get()		# 选择第一个
			except Exception as e:
				print('访问错误', e)
			if href == '':
				CoUrls.append((name[0], '-'))
			else:
				href = 'https://aiqicha.baidu.com/' + href		# 生成链接
				time.sleep(0.3)
				self.driver.get(href)
				html = self.driver.page_source
				selector = etree.HTML(html)
				co_url = selector.xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div[3]/div[2]/p[1]/a/@href')
				co_url = co_url[0] if len(co_url) > 0 else '-'
				values = (name[0], co_url)
				CoUrls.append(values)
				time.sleep(0.1)
				self.driver.back()		# 返回上一页
				time.sleep(0.2)
			self.driver.back()
			
			# print(href)
			# print(lis)
		# 调用sql将数据插入数据库
		sql_jd = """
							insert into "TENCENTAPI"."COMPANY_URL"("name", "url") VALUES(?,?);
									"""
		db.insert_tb(sql_jd, CoUrls)


if __name__ == '__main__':
	aqc = aiqycha()
	db = database()
	aqc.getData(aqc.getTables())
	aqc.input()
