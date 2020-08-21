# coding=utf-8
import urllib2
import urllib
import requests
from lxml import etree
# s=etree.HTML(源码) #将源码转化为能被XPath匹配的格式
# s.xpath(xpath表达式) #返回为一列表,
import sys

reload(sys)
sys.setdefaultencoding('utf8')

url = 'https://item.taobao.com/item.htm?spm=a230r.1.14.289.f6997e90O1ZduZ&id=618838787848&ns=1&abbucket=3#detail'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

cooikes = {'cookie': 'thw=cn; t=63c226a8929295a9d281329af575edaa; enc=WPgf8KkHGgsxoV3Ik9zZ9uyr5%2BaOhFf%2F701on1cFO%2FETJaeWm56klG8%2BX9v7vHWtRREKWt3JfrFqf%2BjTkpJj3TJMw50dOm9kl7RzFIa5AWU%3D; hng=CN%7Czh-CN%7CCNY%7C156; _tb_token_=7673d34bf378b; cookie2=1a822fbe529f66168a4a1e3a02781299; _samesite_flag_=true; _m_h5_tk=1e0fa156527b8905f5560c5464dcf225_1596014717687; _m_h5_tk_enc=6c3c0ae645b4e5db39bc288c9ff49ffb; sgcookie=EKbWGO%2BgFqVYtVdSv%2Bc8Y; tfstk=clSCBVZqzXcQ1IUrY9wwTVM5Hg-5akVXIrdddN7BFA6KCz696sVq0I9ZK1liXEp1.; mt=ci=0_0; tracknick=; cna=LBaDF7fMtlkCAWVQzVmZadAL; v=0; l=eBSNAONVOE6zAks8BOfCnurza779SIRYmuPzaNbMiOCP_yC65_fcWZoj9fLBCnGVhsNyR3oIr-vbBeYBqn4xIghne5DDwQHmn; isg=BGxsv-HVHx7vPAsdWuNmJDw6PUqeJRDPQtNkLcatfZe60Qzb7jbzX_dn8Znp3Ugn'}
html = requests.get(url=url, headers=header, cooikes=cooikes).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
print html
s = etree.HTML(html)

title = s.xpath('//*[@id="header-content"]/div[1]/div[1]/a/@href')
title = title[0] if len(title) > 0 else ''
print title
