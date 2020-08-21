import requests
import re

num = -1
sums = 0


def write_txt_file(path, url):
	try:
		with open(path, mode='w', encoding='utf-8') as f:
			f.write(url)
			f.close()
	except Exception as e:
		print("写入文件失败", e)
	
		
def read_txt_file(path):
	result = '' 	# 读取结果
	this_line = ''	 # 每次读取的行
	try:
		with open(path, mode='r') as f:
			this_line = f.readline()
			while this_line != '':
				result += this_line + "\n"
			f.close()
	except Exception as e:
		print("读取文件失败", e)
	return result


def get_file_line(path, num):
	this_line = ''
	this_num = 0
	try:
		f = open(path)
		this_line = f.readline()
		while this_line != '':
			if num == this_num:
				return this_num
			this_num += 1
	except Exception as e:
		print("读取指定行数失败", e)
	return ''
	

def get_file_count(file):
	count = 0
	try:
		f = open(file)
		while f.readline() is not None:
			count += 1
	except Exception as e:
		print("读取文件总行数失败", e)
	return count
	
	
def get_all_url(url):
	headers = {
		"Referer": url,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
	}
	if url != '-':
		try:
			start_url = url
			response = requests.get(start_url, headers=headers)
		except Exception as e:
			print("进入公司主页失败！", e)
			
		else:
			print("进入公司主页成功！")
			response.encoding = response.apparent_encoding  # 自动获取编码
			html = response.text
			# print(html)
			start_hrefs = re.findall('a href="(.*?)"', html)
			start_hrefs = set(start_hrefs)  # 去除重复网址
			for href in start_hrefs:
				if href.find('http' or 'https') == -1:
					href = start_url + '/' + href
				# print(href)
				try:
					content_response = requests.get(url=href, headers=headers, timeout=25)
					content_html = content_response.text
					# 去除css修饰
					content_html = re.sub('<span.*?>', '', content_html)
					content_html = re.sub('</span.*?>', '', content_html)
					# patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]', content_html)
					patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]',
											   content_html)
					print(href)
					if len(patent_detail) > 0:
						print(patent_detail)
				except Exception as e:
					print("访问失败", e)

	else:
		print("此公司无官方网站！")
		
		
get_all_url('https://www.3s-guojian.com')