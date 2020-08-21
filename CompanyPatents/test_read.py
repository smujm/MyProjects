import requests
import re


def search_url(url='http://www.jenomed.com/we1.asp'):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
	}
	if url != '-':
		try:
			start_url = url
			response = requests.get(start_url, headers=headers)
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
					content_response = requests.get(url='http://www.jenomed.com/we1.asp', headers=headers, timeout=25)
					content_html = content_response.text

					
					patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]',
											   content_html)
					print(href)
					if len(patent_detail) > 0:
						print(patent_detail)
				except Exception as e:
					print("访问失败", e)
		except Exception as e:
			print("进入公司主页失败！", e)
	
	else:
		print("此公司无官方网站！")


search_url()
