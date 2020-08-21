#coding=utf-8

import urllib
import requests
from lxml import etree
#s=etree.HTML(源码) #将源码转化为能被XPath匹配的格式
#s.xpath(xpath表达式) #返回为一列表,
import sys
import dmPython
conn = dmPython.connect(user='SYSDBA', password="citygis1613", server='106.14.243.179', port=5236, autoCommit=True)


string = '7000g'
if string.find('g') == -1:
    str = float(string.replace(' ', '').replace('g', '').replace("\n", "").replace("\t", ""))
else:
    str = float(string.replace(' ', '').replace('g', '').replace("\n", "").replace("\t", ""))*1000
print(str)
