import requests
import re
import execjs
from urllib.request import quote


def getHTMLText(url):
	f_headers1 = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
		'AccessToken': '2H7VNDV5SMZEE7THVERQEZN6GV5QVL2A5TR7TO44U3VLCTXCMSDQ1114596',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Cookie': 'api_uid=CiWW2l8ZKUZHJABXxXWRAg==; ua=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F84.0.4147.89%20Safari%2F537.36; _nano_fp=XpdbnpTJn0TJn5TaX9_UgZWWSkOGx9zF5qDHLLNT; PDDAccessToken=2H7VNDV5SMZEE7THVERQEZN6GV5QVL2A5TR7TO44U3VLCTXCMSDQ1114596; pdd_user_id=9965051753797; pdd_user_uin=SPJEITWABOMXO52OK5GXTFAMMM_GEXDA; webp=1; JSESSIONID=2ED1CB36CF151A4F7C4E65F5FB92E596; vds=gaZKvXhWdZxrDhhHZvxJTFZzvvTKeHDZCZlFrJxJuvfHcKrHCXZWYquhZrcH',
		'DNT': '1',
		'Host': 'yangkeduo.com',
		'Referer': 'http://yangkeduo.com/',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
		'VerifyAuthToken': 'S_3665luAT0anflo8bPRLgdabf5be4e4de5254d',
	}
	
	try:
		r = requests.get(url=url, headers=f_headers1, timeout=20)
		r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
		# print(r.raise_for_status())
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""


with open('anticontent.js', 'r', encoding='utf-8') as f:
	js = f.read()

key_name = quote('8424西瓜')

url = 'http://yangkeduo.com/search_result.html?search_key=' + key_name
response = getHTMLText(url)
print(response)
list_id = re.search('"listID":"([^"]+)"', response).group(1)
flip = re.search('"flip":"([^"]+)"', response).group(1)

ctx = execjs.compile(js)
anti_content = ctx.call('get_anti', url)

next_url = 'http://apiv3.yangkeduo.com/search?page={0}&size=50&sort=default&requert=0&list_id={1}&q={2}&flip={3}&anti_content={4}&pdduid=0'
r = getHTMLText(next_url.format(2, list_id, key_name, flip, anti_content))
print(r)