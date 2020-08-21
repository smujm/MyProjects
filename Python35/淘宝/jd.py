# coding=utf-8
# coding=utf-8
import base64
import os
import random
import sys
import time

import parsel
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据

import re
import requests
from urllib.request import urlopen
from urllib.parse import quote
import xlwt
import xlrd
from lxml import etree
from PIL import Image


class jd:
    def __init__(self):

        print('启动京东爬虫!')

    def create_excel(self, sheet_name, row_title):
        self.f = xlwt.Workbook()
        self.sheet_info = self.f.add_sheet(sheet_name, cell_overwrite_ok=True)
        for i in range(0, len(row_title)):
            self.sheet_info.write(0, i, row_title[i])
        self.f.save('taobao_jd.xls')

    def getHTMLText(self, url):
        f_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        }

        try:
            r = requests.get(url=url, headers=f_headers)
            r.raise_for_status()  # 判断返回的Response类型状态是不是200。如果是200，返回的内容是正确的，不是200，他就会产生一个HttpError的异常
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""

    def parsePage(self, html):
        try:
            tds = html.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div/li/div')
            # 打开excel文件
            data = xlrd.open_workbook('taobao_jd.xls')
            table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件一般都至少有一个table
            rowCount = table.nrows  # 获取行数，下次从这一行开始
            m = 0  # 计数
            for td in tds:
                data = []
                shop_name = td.xpath('./div[5]/span/a/@title')
                shop_name = shop_name[0] if len(shop_name) > 0 else ''
                shop_href = td.xpath('./div[5]/span/a/@href')
                shop_href = 'https:' + shop_href[0] if len(shop_href) > 0 else ''
                good_name = td.xpath('./div[3]/a/em')
                good_name = good_name[0].xpath('string(.)') if len(good_name) > 0 else ''
                good_name = good_name.replace(' ', '').replace("\n", "").replace("\r", "")
                good_href = td.xpath('./div[3]/a/@href')
                good_href = 'https:' + good_href[0] if len(good_href) > 0 else ''
                price = td.xpath('./div[2]/strong/i/text()')
                price = price[0] if len(price) > 0 else ''
                good_html = self.getHTMLText(good_href)
                # s_good_html = etree.HTML(good_html)
                weight = re.findall('商品毛重：(.*?)</li>', good_html)  # <dt>净含量</dt><dd>(.*?)</dd>
                # print(good_href, weight)
                if len(weight) > 0:
                    weight = weight[0]
                else:
                    weight = re.findall('<dt>净含量</dt><dd>(.*?)</dd>', good_html)
                    weight = weight[0] if len(weight) > 0 else 1

                if weight.find('kg') == -1:     # 没找到
                    unit = float(weight.replace('kg', '').replace('g', ''))
                else:
                    unit = float(weight.replace('kg', '').replace('g', '')) * 1000  # kg-->g
                unit_price = float(price) / (unit / 500)
                unit_price = round(unit_price, 2)  # 保留两位小数
                data.append(rowCount + m)
                data.append('京东')
                data.append(shop_name)
                data.append(shop_href)
                data.append(good_name)
                data.append(good_href)
                data.append(price)
                data.append(weight)
                data.append(unit_price)
                # 写入数据
                for j in range(len(data)):
                    self.sheet_info.write(rowCount + m, j, data[j])
                m += 1

                print(shop_name, shop_href, good_name, good_href, price, weight, unit_price)

            # slt = re.findall(r'href=".*?" title="(.*?)"', html)
            # slt_href = re.findall(r'href="(.*?)" title=".*?"',html)
            # plt = re.findall(r'"view_price":"[\d.]*"', html)
            # tlt = re.findall(r'"raw_title":".*?"', html)
            # for i in range(len(slt)):
            #     shop = slt[i]
            #     price = eval(plt[i].split(':')[1])  # eval去除两端的单引号
            #     title = eval(tlt[i].split(':')[1])
            #     ilt.append([shop, price, title])
        except:
            print("error---警告")
        finally:
            self.f.save('taobao_jd.xls')

    def search(self, good_name, page_num):
        goods = good_name  # 商品名称
        depth = page_num  # 商品页数
        start_url = 'https://search.jd.com/Search?keyword={}'.format(goods)
        for i in range(1, depth + 1):
            try:
                print('=================================正在爬取第{}页数据================================='.format(i))
                url = 'https://search.jd.com/Search?keyword={0}&page={1}&scrolling=y'.format(
                    goods, i)
                html = self.getHTMLText(url)
                # print(html)
                html = etree.HTML(html)
                self.parsePage(html)
            except:
                continue


if __name__ == '__main__':
    jds = jd()
    name = '8424西瓜'
    rowTitle = ['uid', '平台', '店铺名称', '店铺URL', '商品名称', '商品URL', '价格', '重量', '单价(元/500g)']
    jds.create_excel(name, rowTitle)
    jds.search(name, 100)
