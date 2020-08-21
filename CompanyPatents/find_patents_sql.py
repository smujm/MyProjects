import requests
import re
import dmPython
from jpype import *
import jpype
import os
from aip import AipOcr
import asyncio
from pyppeteer import launch
import datetime


class DataBase:
	def __init__(self):
		user = 'SYSDBA'
		password = 'citygis1613'
		server = '106.14.243.179'
		port = 5236
		
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


async def get_all_content(url):
	browser = await launch(headless=True)
	page = await browser.newPage()
	await page.setUserAgent(
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
	# 设置页面视图大小
	await page.setViewport(viewport={'width': 1920, 'height': 1080})
	# 是否启用JS, enable设为False, 则无渲染效果
	await page.setJavaScriptEnabled(enabled=True)
	# 请求网页
	await page.goto(url, {
		'timeout': 1000 * 60  # 这里超时是60s
	})
	html = await page.content()
	await browser.close()
	return html


def ocr_text(url):
	'''
	通用文字识别
	'''
	# 百度识字账号
	APP_ID = '21577308'
	API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
	SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
	}
	company = name
	url_last = url.split('/')[-1]
	
	requests.packages.urllib3.disable_warnings()
	response = requests.get(url, headers=headers, verify=False)
	path = 'picture\\{}'.format(company)
	if not os.path.exists(path):
		os.makedirs(path)
	flag1 = os.path.exists(path + '/' + url_last)
	if not flag1:
		with open(path + '/' + url_last, mode='wb') as f:
			f.write(response.content)
	with open(path + '/' + url_last, 'rb') as fp:
		image = fp.read()
	client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
	# 调用通用文字识别接口
	response = client.basicGeneral(image)
	
	'''
	request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
	# 二进制方式打开图片文件
	# f = open('[本地文件]', 'rb')
	# img = base64.b64encode(f.read())
	params = {"url": url}
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GIZsgTXmtdxLAbzNUucUzUQb&client_secret=0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'
	try:
		response = requests.get(host)
		if response:
			# print(response.json())
			access_token = response.json()['access_token']
	except Exception as e:
		print('请求百度账号失败', e)
	try:
		request_url = request_url + "?access_token=" + access_token
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		response = requests.post(request_url, data=params, headers=headers)
	except Exception as e:
		print('请求百度通用文字识别失败', e)
	'''
	
	if response:
		# print(response.json())
		try:
			code = response['words_result']
		except:
			return ''
		string = ''
		for c in range(len(code)):
			string += code[c]['words'] + '--'
		string += '//'
		return string
	# print(string)
	# print(code)
	else:
		return ''


def get_all_url(url):
	# 使用jar获取传入的url的所有地址，并返回所有地址的list
	jar_path = os.path.join(os.path.abspath('.'), r'D:\UseJar\webAllUrl(5).jar')  # jar路径
	jvm_path = getDefaultJVMPath()
	try:
		jpype.startJVM(jvm_path, '-Djava.class.path=%s' % jar_path, convertStrings=True)
	except:
		pass
	JClass = jpype.JClass('util.WebCrawlerDemo')
	instance = JClass()  # 建立对象
	link_list = instance.myPrint(url)
	# url_list = []
	# for i in range(len(link_list)):
	# 	url_list.append(link_list[i])
	# jpype.shutdownJVM()
	return link_list


def search_url(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
	}
	if url != '-':
		try:
			link_list = get_all_url(url)
		# print(link_list)
		except Exception as e:
			print("访问公司网页失败", e)
		# print("进入公司主页成功！")
		# response.encoding = response.apparent_encoding  # 自动获取编码
		# html = response.text
		# # print(html)
		# start_hrefs = re.findall('a href="(.*?)"', html)
		# start_hrefs = set(start_hrefs)  # 去除重复网址
		else:
			for i in range(len(link_list)):
				if link_list[i].find('http' or 'https') == -1:
					link_list[i] = url + '/' + link_list[i]
				# print(href)
				try:
					try:
						loop = asyncio.get_event_loop()
						content_html = loop.run_until_complete(get_all_content(link_list[i]))
					except Exception as e:
						content_response = requests.get(url=link_list[i], headers=headers, timeout=45, verify=False)
						content_html = content_response.text
					
					# 去除css修饰
					content_html = re.sub('<span.*?>', '', content_html)
					content_html = re.sub('</span.*?>', '', content_html)
					# patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]', content_html)
					patent_detail = re.findall('[\w]*[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]',
											   content_html)
					print(link_list[i])
					if len(patent_detail) > 0:
						print(patent_detail)
						img_src = re.findall('<img .*?src="(.*?)"', content_html)
						img_flag = True  # 记录网页中是否含有‘专利’的图片,true-->不含有
						seq_params = []  # 暂存获取的数据
						for j in range(len(img_src)):
							if img_src[j].find('http' or 'https') == -1:
								img_src[j] = url + '/' + img_src[j]
								# print(img_src[j])
								text = ocr_text(img_src[j])  # 调用百度通用识字获取图片中文本
								if '专利' in text:
									img_flag = False
									curr_time = datetime.datetime.now()  # 获取当前时间
									time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
									values = (
										# 公司名，公司url，二级网址，含专利关键字，图片地址，图片文字，获取时间
										str(name), str(url), str(link_list[i]), str(patent_detail), str(img_src[j]),
										str(text), str(time_str))
									seq_params.append(values)
						if img_flag:
							curr_time = datetime.datetime.now()  # 获取当前时间
							time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
							values = (
								# 公司名，公司url，二级网址，含专利关键字，图片地址，图片文字，获取时间
								str(name), str(url), str(link_list[i]), str(patent_detail), str('此页无相关专利照片'),
								str('无照片无内容'), str(time_str))
							seq_params.append(values)
						
						# 调用sql将数据插入数据库
						sql_zl = """
									insert into "PUDONG_COMPANY"."PATENT_DETAIL"("NAME", "NAME_URL", "SECOND_URL",
									"KEYWORDS", "IMG_SRC", "IMG_TEXT", "GET_TIME") VALUES(?,?,?,?,?,?,?);
									"""
						db.insert_tb(sql_zl, seq_params)
						
				except Exception as e:
					print("访问失败", e)
	else:
		print("此公司无官方网站！")


if __name__ == '__main__':
	db = DataBase()
	sql = """
	select NAME,URL from "PUDONG_COMPANY"."COMPANY_URL"
	"""
	result = db.select_tb(sql)
	# print(result, len(result))
	for i in range(len(result)):
		print("\n=============================正在访问第{}家公司，其名称为：{}=============================".format(i + 1,
																									  result[i][0]))
		name = result[i][0]
		search_url(result[i][1])

# search_url('https://www.3s-guojian.com')
