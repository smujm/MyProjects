import requests
import re
import random


def getHTMLText(url):
	cookies = ['thw=cn; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=EC4y8pYcHKNH3mt4PaC2B; mt=ci=0_0; tracknick=; cna=LBaDF7fMtlkCAWVQzVmZadAL; UM_distinctid=173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4; cookie2=176af44b1c952d401cab77fc6b60d5a6; t=21cf760cc2ec7d6c05b61ed1837879d3; _tb_token_=f535e3335edde; v=0; _m_h5_tk=11125db1bd0ff8d3316445edd47ac28b_1596439621213; _m_h5_tk_enc=fe1dc378da210800d2d793aa3d710bcf; tfstk=cuzCBv_24pvCB6jy8W1ZLmQY5T0PZbXjsiHLOlPy-8IB5YFCiK8qhfR3QdYtDf1..; l=eBSNAONVOE6zAYNyBOfaourza77TQIRYmuPzaNbMiOCP_0CW5Y1AWZolST8XCnGVh6leR3oIr-vXBeYBqn4wsWRKe5DDwCDmn; isg=BAAA90miS-SqRjfZBv8yKAge0Y7SieRT1nd46XqR0Zuu9aAfIps94zTHCV01wZwr',
			   'thw=cn; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=EC4y8pYcHKNH3mt4PaC2B; mt=ci=0_0; tracknick=; cna=LBaDF7fMtlkCAWVQzVmZadAL; UM_distinctid=173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4; cookie2=176af44b1c952d401cab77fc6b60d5a6; t=21cf760cc2ec7d6c05b61ed1837879d3; _tb_token_=f535e3335edde; v=0; _m_h5_tk=11125db1bd0ff8d3316445edd47ac28b_1596439621213; _m_h5_tk_enc=fe1dc378da210800d2d793aa3d710bcf; tfstk=cuzCBv_24pvCB6jy8W1ZLmQY5T0PZbXjsiHLOlPy-8IB5YFCiK8qhfR3QdYtDf1..; l=eBSNAONVOE6zAEF2BOfZourza77OsIRYmuPzaNbMiOCPOD5J5zCGWZolZWLvCnGVhsODR3oIr-vXBeYBqn4xIghne5DDwIMmn; isg=BIiIbqprQ4zeRK8x3lfK0PD2WfaaMew7no-AAUI52YP0HSiH60Ovy8QfkfVtKaQT',
			   'thw=cn; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=LBaDF7fMtlkCAWVQzVmZadAL; UM_distinctid=173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4; cookie2=176af44b1c952d401cab77fc6b60d5a6; t=21cf760cc2ec7d6c05b61ed1837879d3; _tb_token_=f535e3335edde; v=0; _m_h5_tk=11125db1bd0ff8d3316445edd47ac28b_1596439621213; _m_h5_tk_enc=fe1dc378da210800d2d793aa3d710bcf; _samesite_flag_=true; sgcookie=EujRwp9jWZ%2FgZnQfMLxw1; unb=2208588851436; uc3=nk2=qVXfcmfLpEg%3D&vt3=F8dBxG2g70XJIvK0kmU%3D&lg2=W5iHLLyFOGW7aA%3D%3D&id2=UUphwoIRWIH7kFPhBg%3D%3D; csg=69f7b506; lgc=%5Cu662F%5Cu5C0F%5Cu83B9%5Cu5440; cookie17=UUphwoIRWIH7kFPhBg%3D%3D; dnk=%5Cu662F%5Cu5C0F%5Cu83B9%5Cu5440; skt=5f766ec2cc179eef; existShop=MTU5NjQzMjYzMg%3D%3D; uc4=nk4=0%40qxB4VfeM%2BE77JDMlqzUVvvCy5g%3D%3D&id4=0%40U2grGRoA1RxezmkdeDFfKHJNXzz7fXTS; tracknick=%5Cu662F%5Cu5C0F%5Cu83B9%5Cu5440; _cc_=URm48syIZQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%91%8068; _nk_=%5Cu662F%5Cu5C0F%5Cu83B9%5Cu5440; cookie1=W8tw%2B6L5xH3PjMJMhAhEVEqr3xWguDa7CEpJFnAQqrg%3D; tfstk=cwWdB90DqP43vS-O06FMPIMaqOqcZxmJrmL-eumZDykqKLkRiH6cHsO0M3upBlC..; mt=ci=3_1; uc1=cookie14=UoTV6h9%2Ba%2Bz7Nw%3D%3D&existShop=false&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie21=UIHiLt3xTIkz&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D; l=eBSNAONVOE6zA9VjBOfanurza77tYIRYmuPzaNbMiOCPOJCJ5EMfWZolZrYvCnGVh6PvJ3oIr-vbBeYBqCmWfdWqe5DDwFDmn; isg=BGNjXwPHOG2B4vRgqY7h0X__8qcNWPeaYfZ7cJXA50I51IP2HCgd6mgKzqRa8E-S',
			   'thw=cn; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=EC4y8pYcHKNH3mt4PaC2B; mt=ci=0_0; tracknick=; cna=LBaDF7fMtlkCAWVQzVmZadAL; t=016e01511eed975d01ca996d95a5b0de; v=0; _m_h5_tk=c021e6e7411203add8dd2ee4dc8cc4a9_1596426267345; _m_h5_tk_enc=3cc04de7740cb561ea73f98413c1cae4; cookie2=1c383cec613c946bfdfbda77c2bb87aa; _samesite_flag_=true; UM_distinctid=173b1f1a6a418d-05bec1c05e6b95-b7a1334-149c48-173b1f1a6a5bc4; _tb_token_=eea13e13e6b3d; tfstk=cCxFBo29hDneUzSSkMszAOcvFP1dC75h1uXV-EEUYfw3Sfncgp50w7BiC7BlIsnG-; l=eBSNAONVOE6zAMIkBOfanurza77OSIRYmuPzaNbMiOCPOu5e5ONFWZou6jTwC3GVh6yMR3oIr-vbBeYBqI2wsWRKe5DDwQHmn; isg=BCUlE26JlgP8SvJmu8QfL40VNOFfYtn0cwz99icK4dxrPkWw77LpxLPcyKJIOvGs',
			   'cna=LBaDF7fMtlkCAWVQzVmZadAL; cmida=1401053355_20200731144605; sca=e203848a; aimx=5nKmF3ZelF0CAXToQgWmuZxW_1596432711; cnaui=2070505547; aui=2070505547; cdpid=UUjWDiI1lqneBg%253D%253D; tbsa=4c0e595ed6b0b29113895139_1596432739_38; atpsida=20a79211b6093245e275f1e6_1596432739_38',
			   'cna=LBaDF7fMtlkCAWVQzVmZadAL; csa=0_0_0_0_0_0_0_0_0_0_0; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=6e3b78cb7f73b182eea671843c8b89ab_1596424891510; _m_h5_tk_enc=cfb2d2ea41f06797ceb151ca251e55f3; sm4=310100; dnk=%5Cu5360jin%5Cu660E; uc1=cookie21=Vq8l%2BKCLjhS4UhJVbhgU&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=true&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoTV6h9%2Ba%2B1Jow%3D%3D&pas=0; uc3=nk2=tq1IqFaBgQ%3D%3D&vt3=F8dBxG2g70XI368xHIc%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&id2=UUjWDiI1lqneBg%3D%3D; tracknick=%5Cu5360jin%5Cu660E; lid=%E5%8D%A0jin%E6%98%8E; uc4=nk4=0%40tHu%2FdtQaEQTQc4%2Fzei1g18Vr&id4=0%40U2o0P%2FqsYj7uuwFuNV9u%2F38FZx%2By; _l_g_=Ug%3D%3D; unb=2070505547; lgc=%5Cu5360jin%5Cu660E; cookie1=WvBhS%2FBY5oVgFoKVdxGODEEXqSeN4g0dfd%2F%2F%2FIiLKbQ%3D; login=true; cookie17=UUjWDiI1lqneBg%3D%3D; cookie2=176af44b1c952d401cab77fc6b60d5a6; _nk_=%5Cu5360jin%5Cu660E; sgcookie=EKYvHYUd%2Fb3KpBjmeNz2i; t=21cf760cc2ec7d6c05b61ed1837879d3; sg=%E6%98%8E78; csg=c02e817c; enc=k5s3IXkP1FixtgD2HCz%2BRHteiFbymmhjAFtQNtZN%2BZKdgGcCRAuSiBVvrz4roQd2iypLHphltsXW%2FPU45zCZFQ%3D%3D; _tb_token_=f535e3335edde; pnm_cku822=098%23E1hvcvvUvbpvUpCkvvvvvjiPnLdpsjDRnLzUgjrCPmPUgjinPLd9tjEVPFdhljl8R2yCvvBvpvvv2QhvCvvvMMGCvpvVphhvvvvvmphvLhPOjpmF%2BFBCWDAvD46XjovDNKClHqyQcmDaIU9BDVQEVA3lYb8rwkYKjEcX%2BFysxe3C%2BE7rjC69EcqWaBwlb6OKCIkUDCODN5HHaNoivpvUphvhsx55aIJEvpvVpyUUCCQ4Kphv8hCvvvvvvhCvphvORvvvpirvpC96vvC286CvV2pvvhnGphvOnvvvpzA5vpvhphvhHv%3D%3D; tfstk=c5LdBd2cZADh44f9gHnGFia1gNTdZVNRESB8ybVaiO0Za9aRiWTDknsmD_ydWfC..; l=eBaKWmg4OgVMGMoDBOfahurza77ORIRYmuPzaNbMiOCPOh1e5gyFWZolaYTwCnGVh6eHR3oIr-vXBeYBqnX2_6Fca6Fy_BHmn; isg=BExMHuCqf7gDgWtor_aQh5XcHap-hfAvojNETaYNePeaMew7zpagv86D1TkJfSiH; cq=ccp%3D0'
			   ]
	temp = random.randint(0, 5)
	print(temp)
	f_headers1 = {
		'authority': 's.taobao.com',
		'cache-control': 'max-age=0',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
		'sec-fetch-user': '?1',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'navigate',
		'referer': 'https://www.taobao.com/?spm=a230r.1.1581860521.1.44436fbeX7fwH0',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'zh-CN,zh;q=0.9',
		'cookie': cookies[temp],
	}
	
	try:
		r = requests.get(url=url, headers=f_headers1)
		r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
		print(r.raise_for_status())
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""


good_href = 'https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-21202414081.10.1afc640akbapmW&id=618331355751'
good_html = getHTMLText(good_href)
# good_html = ''
if good_html.find('净重') != -1:
	weight = re.findall('净重<\/span>([0-9]*)g', good_html)
elif good_html.find('净含量') != -1:
	weight = re.findall('<dd>([0-9]*)g<\/dd>', good_html)
elif good_html.find('重量') != -1:
	weight = float(re.findall('<dd><em>(.*?)<\/em>kg<\/dd>', good_html)) * 1000
else:
	weight = ''
	
print(weight[0])