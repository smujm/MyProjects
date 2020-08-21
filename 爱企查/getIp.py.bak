# coding=utf-8

# 爬取ip代理，构建ip代理池
# requests
# parsel
# 爬虫思路：
# 1.确定url地址（分析页面\网页性质）
# 2.发送请求-- requests（范数据）
# 3.解析数据-- 正则表达式\css选择器\xpath（路径选择器）
# 4.保存数据-- 数据库\本地文件

import requests
from lxml import etree
import parsel
import  time


def check_ip(proxies):
    '''检测代理的质量'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    can_use = []
    for proxy in proxies:
        try:
            response.get(url='https://www.taobao.com/', headers=headers, proxies=proxy, timeout=1)
            if response.status_code == 200:
                can_use.append(proxy)
        except Exception:
            print '当前代理ip:', proxy, '请求超时，检测不合格'
        else:
            print '当前代理ip:', proxy, '检测通过'
    return can_use

proxies_list = []
for page in range(1, 11):
    print '==========正在爬取第{}页数据==========='.format(page)
    # 1
    base_url = 'http://www.ip3366.net/?stype=1&page={}'.format(str(page))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    # 2
    response = requests.get(url=base_url, headers=headers)
    #response.encoding = response.apparent_encoding  # 自动识别响应体的编码
    html_data = response.text
    # print html_data

    # 3
    # 代理ip的结构 {'ip的协议(http/https)': 'ip:ip对应的端口'}
    parse_data = etree.HTML(html_data)  # 转换数据类型
    tr_list = parse_data.xpath('//*[@id="list"]/table/tbody/tr')
    for tr in tr_list:
        http_type = tr.xpath('./td[4]/text()')[0]  # 协议类型
        ip_num = tr.xpath('./td[1]/text()')[0]  # ip地址
        ip_port = tr.xpath('./td[2]/text()')[0]  # ip端口
        # print http_type, ip_num, ip_port

        proxies_dict = {}
        proxies_dict[http_type] = ip_num + ':' + ip_port
        print '正在获取ip:', proxies_dict
        proxies_list.append(proxies_dict)

    time.sleep(1)

print proxies_list
print '获取当前ip数量', len(proxies_list)

print '======================正在检测代理ip的质量======================'
can_use = check_ip(proxies_list)
print '能用的ip:', can_use
print '能用的数量:', len(can_use)
