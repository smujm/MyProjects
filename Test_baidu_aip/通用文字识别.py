import requests
import pprint
from aip import AipOcr
import re
import os
import base64

import asyncio
from pyppeteer import launch
from pyppeteer import chromium_downloader

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}


async def pyppeteer(url):
	browser = await launch(headless=True, ignoreHEEPSErrors=True)
	page = await browser.newPage()
	
	await page.setUserAgent(
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
	# 设置页面视图大小
	await page.setViewport(viewport={'width': 1920, 'height': 1080})
	# 是否启用JS, enable设为False, 则无渲染效果
	await page.setJavaScriptEnabled(enabled=True)
	# 请求网页
	await page.goto(url, timeout=60000,)
	html = await page.content()
	await browser.close()
	return html


def ocr_text(url):		# 通用文字识别, url: 图片地址
	# 百度识字账号
	APP_ID = '21577308'
	API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
	SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
	}
	last = url.split('/')[-1]
	
	response = requests.get(url, headers=headers)
	flag1 = os.path.exists('picture\\{}'.format(last))
	if not flag1:
		with open('picture\\{}'.format(last), mode='wb') as f:
			f.write(response.content)
	with open('picture\\{}'.format(last), 'rb') as fp:
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
	response = requests.get(host)
	if response:
		print(response.json())
		access_token = response.json()['access_token']

	request_url = request_url + "?access_token=" + access_token
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.post(request_url, data=params, headers=headers)
	'''
	if response:
		# pprint.pprint(response.json())
		try:
			code = response['words_result']
		except:
			return ''
		string = ''
		for i in range(len(code)):
			string += code[i]['words'] + '--'
		string += '//'
		print(string)
		# print(code)
		return string


url1 = 'https://www.epmedtec.com/#'
url = 'https://www.epmedtec.com/recruit_11.html'

try:
	loop = asyncio.get_event_loop()
	content_html = loop.run_until_complete(pyppeteer(url))
except Exception as e:
	content_response = requests.get(url=url, headers=headers, timeout=45, verify=False)
	content_html = content_response.text
	
# text = ocr_text(url)
# content_response = requests.get(url=url, headers=headers, timeout=25)
# content_html = content_response.text
img_src = re.findall('<img .*?src="(.*?)"', content_html)
for j in range(len(img_src)):
	if img_src[j].find('http' or 'https') == -1:
		img_src[j] = url1 + '/' + img_src[j]
	# print(img_src[j])
	text = ocr_text(img_src[j])
	if '专利' in text:
		print(text, end=' ')
