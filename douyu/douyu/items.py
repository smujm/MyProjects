# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 明确爬取数据内容
    # 主播名字
    nickname = scrapy.Field()
    # 封面图片
    vertical_src = scrapy.Field()
    
