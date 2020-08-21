import scrapy
import json
from douyu.items import DouyuItem


class SpiderSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['https://www.douyu.com']
    base_url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        # 提取数据
        data_list = json.loads(response.body)['data']
        if len(data_list) == 0:
            return
        for data in data_list:
            item = DouyuItem()
            item['nickname'] = data['nickname'].encode('utf-8')
            item['vertical_src'] = data['vertical_src']
            
            yield item
            
        self.offset += 20
        url = self.base_url + str(self.offset)
        # callback 回调函数，将得到请求的相应交给自己处理
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)
