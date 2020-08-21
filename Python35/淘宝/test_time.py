import datetime
import requests
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}
response = requests.get('https://www.ximalaya.com/youshengshu/16411402/p1/',headers=headers)
print(response.text)
curr_time = datetime.datetime.now()		# 获取当前时间
time_str = curr_time.strftime('%Y-%m-%d %H:%M:%S')
print((time_str))
