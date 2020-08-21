import time
import datetime
import requests
import json

base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
offset = 0
start_urls = base_url + str(offset)

response = requests.get(start_urls)
response.encoding = response.apparent_encoding
# 提取数据
print(response.text)
data_list = json.loads(response.text)['data']
if len(data_list) == 0:
	print('.')
	
	