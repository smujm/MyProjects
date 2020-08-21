import requests
import re
import aip

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


def get_novel(num):
	url = 'http://www.xbiquge.la/10/10489/'
	response = requests.get(url=url)
	response.encoding = response.apparent_encoding
	html_data = response.text
	# print(html)
	result_list = re.findall("<dd><a href='(.*?)' >.*</a></dd>", html_data)
	# print(result_list)
	
	count = result_list[num]
	all_url = 'http://www.xbiquge.la' + count
	# print(all_url)
	response2 = requests.get(url=all_url)
	response2.encoding = response2.apparent_encoding
	html_data2 = response2.text
	# print(html_data2)
	
	result = re.findall('<div id="content">(.*?)<p>.*</p></div>', html_data2, re.S)
	print(result)
	
	with open('a.txt', mode='w', encoding='utf-8') as f:
		f.write(result[0].replace('&nbsp;', '').replace('<br/>', '/n', ).replace('<br />', ''))

		
if __name__ == '__main__':
	num = int(input("请输入章节序号(数字)："))
	get_novel(num)
