import requests
import re
from aip import AipSpeech

# 百度语音合成
APP_ID = '22061361'
API_KEY = 'Tp8cSYMO67oKDc8EcBQ1UH1u'
SECRET_KEY = 'nsQdgoI8VrGHWf6sD39bKuQQEQIzGAxM'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


def txt_to_voice():
	with open('a.txt', mode='r', encoding='utf-8') as f:
		flag = 0
		while True:
			flag += 1
			text = f.read(1023)		# 设置1023字节长度
			if not text:		# 判断text里是否还有数据
				break
			# print(text)
			# print('+' * 100)
			result = client.synthesis(text, 'zh', 1, {
				'vol': 9,
				'pit': 9,
				'per': 4,
			})
		
			# 识别正确返回语音二进制，错误则返回dict
			if not isinstance(result, dict):
				with open('video\\{}.mp3'.format(str(flag)), mode='wb') as file:
					file.write(result)
					print('正在生成第{}段语音。。。'.format(flag))

	
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
	txt_to_voice()
