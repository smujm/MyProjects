import scrapy  # 导入scrapy


# 创建爬虫类，并继承自scrapy.Spider -->最基础的类
class KuaidailiSpider(scrapy.Spider):
	name = 'kuaidaili'  # 爬虫名字--->必须唯一
	allowed_domains = ['https://www.kuaidaili.com/free']  # 允许采集的域名
	# start_urls = ['https://www.kuaidaili.com/free/']  # 开始采集的网站
	start_urls = [f'https://www.kuaidaili.com/free/inha/{page}/' for page in range(1, 3593)]  # 开始采集的网站
	
	# 解析响应数据，提取数据，或者网址等。response 就是网页源码
	def parse(self, response):
		# 提取数据
		# 提取IP PORT
		selectors = response.xpath('//*[@id="list"]/table/tbody/tr')  # 选择所有的tr标签
		for selector in selectors:
			ip = selector.xpath('./td[1]/text()').get()
			port = selector.xpath('./td[2]/text()').get()
			
			items = {
				'ip': ip,
				'port': port,
			}
			yield items
			# print(ip + ":" + port)
