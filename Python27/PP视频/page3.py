# coding=utf-8

import requests
import time
import xlwt
import xlrd
from lxml import etree




import json
import os
import pandas as pd


# s=etree.HTML(源码) #将源码转化为能被XPath匹配的格式
# s.xpath(xpath表达式) #返回为一列表,

# 获取页面地址
class ppData(object):
    def __init__(self):
        self.f = xlwt.Workbook()  # 创建工作薄
        self.sheet1 = self.f.add_sheet(u'视频', cell_overwrite_ok=True)
        self.rowsTitle = [u'编号', u'标题', u'链接', u'时间', u'导演或上传者', u'简介', u'宣传照片', u'时长(分:秒)']
        for i in range(0, len(self.rowsTitle)):
            self.sheet1.write(0, i, self.rowsTitle[i], self.set_style('Times new Roman', 220, True))

        self.f.save('pp.xlsx')

    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.colour_index = 2
        font.height = height
        style.font = font
        return style

    def getUrl(self):
        for i in range(1, 51):
            url = 'https://sou.pptv.com/s_video?kw=%E5%8A%A0%E8%8F%B2%E7%8C%AB&pn={}'.format(i)
            if i == 1:
                self.first(url)
            elif i == 2:
                self.second(url)
            else:
                self.scrapyPage(url)

    def first(self, url):
        if url is None:
            return None
        try:
            data = xlrd.open_workbook(('pp.xlsx'))
            table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件至少有一个table
            rowCount = table.nrows  # 获取行数，下次从这一行开始

            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

            html = requests.get(url, headers=header).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
            s = etree.HTML(html)
            m = 0
            for i in range(2, 7):
                data = []
                try:
                    href = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/a/@href')[0]
                except Exception as e:
                    href = ''
                try:
                    title = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/a/@title')[0]
                except Exception as e:
                    title = ''
                try:
                    time = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/span[1]/i/text()')[0]
                except Exception as e:
                    time = ''
                try:
                    country = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[1]/a/text()')[0]
                except Exception as e:
                    country = ''
                try:
                    director = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[2]/a[2]/text()')[0]
                except Exception as e:
                    director = ''
                try:
                    if (i >= 4):
                        intro = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[5]/div/p/text()')[0]
                    else:
                        intro = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[4]/div/p/text()')[0]
                except Exception as e:
                    intro = ''
                # try:
                #     pop = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[4]')
                #     pop = pop[0].xpath('string(.)') if len(pop) > 0 else ''
                # except Exception as e:
                #     pop = ''
                try:
                    img = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/a/img/@src')[0]
                except Exception as e:
                    img = ''
                # try:
                #
                # except Exception as e:
                #     = ''
                # 拼装成一个集合
                data.append(rowCount + m)  # 加序号
                data.append(title)
                data.append(href)
                data.append(time)
                # data.append(country)
                data.append(director)
                data.append(intro)
                # data.append(pop)
                data.append(img)

                for i in range(len(data)):
                    self.sheet1.write(rowCount + m, i, data[i])  # 写入数据

                m += 1  # 记录行数增量

                print title, href, time, country, director, intro, img

            for i in range(1, 12):
                data = []
                if i != 4:
                    try:
                        href = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/h5/a/@href')[0]
                    except Exception as e:
                        href = ''
                    try:
                        title = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/h5/@title')[0]
                    except Exception as e:
                        title = ''
                    try:
                        if i == 6 or i == 7 or i == 8:
                            time = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/p[1]/text()')[
                                0]
                        else:
                            time =  s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/p[1]/span[2]/text()')[
                                0]
                    except Exception as e:
                        time = ''
                    try:
                        author = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/p[1]/a/text()')[
                            0]
                    except Exception as e:
                        author = ''
                    try:
                        pop = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/div/p[2]/text()')[0]
                    except Exception as e:
                        pop = ''
                    try:
                        dur = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/a/i/text()')[0]
                    except Exception as e:
                        dur = ''

                    try:
                        img = s.xpath('/html/body/div[3]/div[1]/div[8]/ul/li[{}'.format(i) + ']/a/img/@src')[0]
                    except Exception as e:
                        img = ''
                    # try:
                    #
                    # except Exception as e:
                    #     = ''
                    # 拼装成一个集合
                    data.append(rowCount + m)  # 加序号
                    data.append(title)
                    data.append(href)
                    data.append(time)
                    data.append(author)
                    data.append(pop)
                    data.append(img)
                    data.append(dur)
                    for i in range(len(data)):
                        self.sheet1.write(rowCount + m, i, data[i])  # 写入数据

                    m += 1  # 记录行数增量
                    print title, href, time, author, pop, dur, img
        except Exception, e:
            print '出错', e.message
        finally:
            self.f.save('pp.xlsx')

    def second(self, url):
        if url is None:
            return None
        try:
            data = xlrd.open_workbook(('pp.xlsx'))
            table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件至少有一个table
            rowCount = table.nrows  # 获取行数，下次从这一行开始
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

            html = requests.get(url, headers=header).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
            s = etree.HTML(html)
            m = 0
            for i in range(2, 5):
                data = []
                try:
                    href = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/a/@href')[0]
                except Exception as e:
                    href = ''
                try:
                    title = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/a/@title')[0]
                except Exception as e:
                    title = ''
                try:
                    time = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dt/span[1]/i/text()')[0]
                except Exception as e:
                    time = ''
                try:
                    country = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[1]/a/text()')[0]
                except Exception as e:
                    country = ''
                try:
                    director = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[2]/a[2]/text()')[0]
                except Exception as e:
                    director = ''
                try:
                    intro = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/div/dl/dd[5]/div/p/text()')[0]
                except Exception as e:
                    intro = ''
                try:
                    img = s.xpath('/html/body/div[3]/div[1]/div[{}'.format(i) + ']/a/img/@src')[0]
                except Exception as e:
                    img = ''
                # try:
                #
                # except Exception as e:
                #     = ''
                # 拼装成一个集合
                data.append(rowCount + m)  # 加序号
                data.append(title)
                data.append(href)
                data.append(time)
                data.append(director)
                data.append(intro)
                data.append(img)

                for i in range(len(data)):
                    self.sheet1.write(rowCount + m, i, data[i])  # 写入数据

                m += 1  # 记录行数增量

                print title, href, time, country, director, intro, img

            for i in range(1, 12):
                data = []
                if i != 4:
                    try:
                        href = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/h5/a/@href')[0]
                    except Exception as e:
                        href = ''
                    try:
                        title = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/h5/@title')[0]
                    except Exception as e:
                        title = ''
                    try:
                        time = \
                        s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[1]/span[2]/text()')[0]
                    except Exception as e:
                        time = ''
                    try:
                        author = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[1]/a/text()')[
                            0]
                    except Exception as e:
                        author = ''
                    try:
                        pop = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[2]/text()')[0]
                    except Exception as e:
                        pop = ''
                    try:
                        img = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/a/img/@src')[0]
                    except Exception as e:
                        img = ''
                    try:
                        dur = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/a/i/text()')[0]
                    except Exception as e:
                        dur = ''
                    # try:
                    #
                    # except Exception as e:
                    #     = ''
                    # 拼装成一个集合
                    data.append(rowCount + m)  # 加序号
                    data.append(title)
                    data.append(href)
                    data.append(time)
                    data.append(author)
                    data.append(pop)
                    data.append(img)
                    data.append(dur)

                    for i in range(len(data)):
                        self.sheet1.write(rowCount + m, i, data[i])  # 写入数据

                    m += 1  # 记录行数增量
                    print title, href, time, author, pop, img
        except Exception, e:
            print '出错', e.message
        finally:
            self.f.save('pp.xlsx')

    def scrapyPage(self, url):
        if url is None:
            return None
        try:
            data = xlrd.open_workbook(('pp.xlsx'))
            table = data.sheets()[0]  # 通过索引顺序获取table，一个excel文件至少有一个table
            rowCount = table.nrows  # 获取行数，下次从这一行开始
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

            html = requests.get(url, headers=header).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
            s = etree.HTML(html)
            m = 0
            for i in range(1, 12):
                data = []
                if i != 4:
                    try:
                        href = s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/div/h5/a/@href')[0]
                    except Exception as e:
                        href = ''
                    try:
                        title = s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/div/h5/@title')[0]
                    except Exception as e:
                        title = ''
                    try:
                        time = \
                        s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/div/p[1]/span[2]/text()')[0]
                    except Exception as e:
                        time = ''
                    try:
                        author = s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/div/p[1]/a/text()')[
                            0]
                    except Exception as e:
                        author = ''
                    try:
                        pop = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[2]/text()')
                    except Exception as e:
                        pop = ''
                    try:
                        img = s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/a/img/@src')[0]
                    except Exception as e:
                        img = ''
                    try:
                        dur = s.xpath('/html/body/div[3]/div[1]/div[3]/ul/li[{}'.format(i) + ']/a/i/text()')[0]
                    except Exception as e:
                        dur = ''
                    # try:
                    #
                    # except Exception as e:
                    #     = ''
                    print title, href, time, author, pop, img
                    # 拼装成一个集合
                    data.append(rowCount + m)  # 加序号
                    data.append(title)
                    data.append(href)
                    data.append(time)
                    data.append(author)
                    data.append(pop)
                    data.append(img)
                    data.append(dur)

                    for i in range(len(data)):
                        self.sheet1.write(rowCount + m, i, data[i])  # 写入数据

                    m += 1  # 记录行数增量

        except Exception, e:
            print '出错', e.message
        finally:
            self.f.save('pp.xlsx')


if '__main__':
    pp = ppData()
    pp.getUrl()
