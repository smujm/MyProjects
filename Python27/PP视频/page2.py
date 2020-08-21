#coding=utf-8
import urllib2
import urllib
import requests
from lxml import etree
#s=etree.HTML(源码) #将源码转化为能被XPath匹配的格式
#s.xpath(xpath表达式) #返回为一列表,


url = 'https://sou.pptv.com/s_video?kw=%E5%8A%A0%E8%8F%B2%E7%8C%AB&pn=2'
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

html = requests.get(url, headers = header).text    #这里一般先打印一下html内容，看看是否有内容再继续。
s = etree.HTML(html)

for i in range(2, 5):
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
        print title, href, time,country,director, intro, img

for i in range(1, 12):
    if i != 4:
        try:
            href = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/h5/a/@href')[0]
        except Exception as e:
            href = ''
        try:
            title = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/h5/@title')[0]
        except Exception as e:
             title= ''
        try:
            time = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[1]/span[2]/text()')[0]
        except Exception as e:
            time = ''
        try:
            author = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[1]/a/text()')[0]
        except Exception as e:
            author = ''
        try:
            pop = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/div/p[2]/text()')[0]
        except Exception as e:
            pop = ''
        try:
            img = s.xpath('/html/body/div[3]/div[1]/div[6]/ul/li[{}'.format(i) + ']/a/img/@src')[0]
        except Exception as e:
            img= ''
        # try:
        #
        # except Exception as e:
        #     = ''
        print title,href,time,author,pop,img


