#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: find_patents_sql_thread.py
@time: 2020/8/24 11:20
@desc:
"""
import requests
import re
import dmPython
from jpype import *
import jpype
import os
from aip import AipOcr
import asyncio
from pyppeteer import launch
import time
import datetime
import random
from PIL import Image
import concurrent.futures
import sys
sys.setrecursionlimit(10000)


class DataBase:
    def __init__(self):
        user = 'SYSDBA'
        password = 'citygis1613'
        server = '106.14.243.179'
        port = 5236

        try:
            conn = dmPython.connect(
                user=user,
                password=password,
                server=server,
                port=port,
                autoCommit=True
            )
            print("数据库连接成功！")
            self.conn = conn
        except dmPython.Error as e:
            print("连接失败", str(e))

    def create_tb(self, sql):
        try:
            cursor = self.conn.cursor()  # 获取光标
            cursor.execute(sql)  # 执行sql
            print("创建成功")
        except dmPython.Error as e:
            print("创建失败", str(e))
        finally:
            cursor.close()  # 关闭游标

    def insert_tb(self, sql, data):
        try:
            cursor = self.conn.cursor()
            # cursor.execute('set identity_insert "TENCENTAPI"."taobao_jd" on;')
            cursor.executemany(sql, data)
            self.conn.commit()
            print("数据插入成功")
        except dmPython.Error as e:
            self.conn.rollback()
            print("插入失败", str(e))
        finally:
            cursor.close()

    def select_tb(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result1 = cursor.fetchall()
            # print("查询全部结果：", result1)
            return result1
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def select_tb_one(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result2 = cursor.fetchone()
            print("查询一条结果：", result2)
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def select_tb_many(self, sql, count):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result3 = cursor.fetchmany(count)
            print("查询结果：", result3)
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()

    def update(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            print("修改成功")
        except dmPython.Error as e:
            print("查询失败", str(e))
        finally:
            cursor.close()


async def get_all_content(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
    # 设置页面视图大小
    await page.setViewport(viewport={'width': 1920, 'height': 1080})
    # 是否启用JS, enable设为False, 则无渲染效果
    await page.setJavaScriptEnabled(enabled=True)
    # 请求网页
    await page.goto(url, {
        'timeout': 1000 * 60  # 这里超时是60s
    })
    html = await page.content()
    await browser.close()
    return html


def ocr_text(name, url, id):
    '''
    通用文字识别
    '''
    # 百度识字账号
    APP_ID = '21577308'
    API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
    SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    company = name
    url_last = url.split('/')[-1]

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = response.apparent_encoding
    path = 'picture\\{}'.format(company)
    if not os.path.exists(path):
        os.makedirs(path)
    flag1 = os.path.exists(path + '/' + url_last)
    if not flag1:
        with open(path + '/' + url_last, mode='wb') as f:
            f.write(response.content)
    with open(path + '/' + url_last, 'rb') as fp:
        image = fp.read()
        image_size = len(image)
        image_data = Image.open(fp)
        x, y = image_data.size
        if image_size > 4194304 or x > 4096 or y > 4096:
            return 'Image size error'
            print('Image size error:', url)
        radio = x / y
        if radio > 1.25 or radio < 0.6:
            # print("isn't patent")
            return "isn't patent"
    client = AipOcr(id['APP_ID'], id['API_KEY'], id['SECRET_KEY'])
    # 设置等待，减少QPS
    # random_wait = random.uniform(1, 2)
    # time.sleep(random_wait)
    time.sleep(0.51)
    # 调用通用文字识别接口
    response = client.basicGeneral(image)

    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    # f = open('[本地文件]', 'rb')
    # img = base64.b64encode(f.read())
    params = {"url": url}
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GIZsgTXmtdxLAbzNUucUzUQb&client_secret=0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'
    try:
        response = requests.get(host)
        if response:
            # print(response.json())
            access_token = response.json()['access_token']
    except Exception as e:
        print('请求百度账号失败', e)
    try:
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
    except Exception as e:
        print('请求百度通用文字识别失败', e)
    '''

    if response:
        # print(response.json())
        try:
            code = response['words_result']
        except:
            code = response['error_code']
            print('百度api接口错误码:', code, '图片地址:'+url)
            return 'none'
        string = ''
        for c in range(len(code)):
            string += code[c]['words'] + '--'
        string += '//'
        return string
    # print(string)
    # print(code)
    else:
        return 'null'


def get_all_url_jar(url):
    # 使用jar获取传入的url的所有地址，并返回所有地址的list
    jar_path = os.path.join(os.path.abspath('.'), r'D:\UseJar\webAllUrl(7).jar')  # jar路径
    jvm_path = getDefaultJVMPath()
    try:
        jpype.startJVM(jvm_path, '-Djava.class.path=%s' % jar_path, convertStrings=True)
    except:
        pass
    JClass = jpype.JClass('util.WebCrawlerDemo')
    instance = JClass()  # 建立对象
    link_list = instance.myPrint(url)
    # url_list = []
    # for i in range(len(link_list)):
    # 	url_list.append(link_list[i])
    # jpype.shutdownJVM()
    return link_list


def get_all_url(base_url, url, sums, number, url_list):
    headers = {
        "Referer": base_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    if base_url != '-':
        try:
            start_url = url
            response = requests.get(start_url, headers=headers)
        except Exception as e:
            number += 1
            if sums > number:
                get_all_url(base_url, url_list[number], sums, number, url_list)
            return
        else:
            # print("开始链接：", url)
            response.encoding = response.apparent_encoding  # 自动获取编码
            html = response.text
            # print(html)
            start_hrefs = re.findall('a href="(.*?)"', html)
            start_hrefs = set(start_hrefs)  # 去除重复网址
            for href in start_hrefs:
                if href.find('http' or 'https') == -1:
                    if href.startswith('/'):
                        href = base_url + href
                    else:
                        href = base_url + '/' + href
                # print(href)
                if href not in url_list:
                    if href.find(base_url) != -1:
                        # 判断该a标签的内容是文件还是子链接
                        if href.find(".doc") == -1 and href.find(".exl") == -1 and href.find(".dbf") == -1 \
                                and href.find(".exe") == -1 and href.find(".apk") == -1 \
                                and href.find(".mp3") == -1 and href.find(".mp4") == -1 \
                                and href.find("javascript") == -1 and href.find('.pdf') == -1:
                            url_list.append(href)
                            sums += 1
            # try:
            #                 #     content_response = requests.get(url=href, headers=headers, timeout=25)
            #                 #     content_html = content_response.text
            #                 #     # 去除css修饰
            #                 #     content_html = re.sub('<span.*?>', '', content_html)
            #                 #     content_html = re.sub('</span.*?>', '', content_html)
            #                 #     # patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]', content_html)
            #                 #     patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]',
            #                 #                                content_html)
            #                 #     print(href)
            #                 #     if len(patent_detail) > 0:
            #                 #         print(patent_detail)
            #                 #
            #                 # except Exception as e:
            #                 #     print("访问失败", e)
            number += 1
            if sums > number:
                get_all_url(base_url, url_list[number], sums, number, url_list)

    else:
        print("此公司无官方网站！")


def search_url(name, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    if url != '-':
        try:
            sums = 0
            number = -1
            base_url = url
            link_list = []
            get_all_url(base_url, url, sums, number, link_list)
            print(name, '官网网址总数：', len(link_list))
        # print(link_list)
        except Exception as e:
            print("访问公司网页失败", e)
        # print("进入公司主页成功！")
        # response.encoding = response.apparent_encoding  # 自动获取编码
        # html = response.text
        # # print(html)
        # start_hrefs = re.findall('a href="(.*?)"', html)
        # start_hrefs = set(start_hrefs)  # 去除重复网址
        else:
            seq_params = []  # 暂存获取的数据
            state = '/'
            remark = '/'
            state1, state2, state3, state4, state5 = [], [], [], [], []
            state1_flag = True  # 检测状态1的存在
            for i in range(len(link_list)):
                # if link_list[i].find('http' or 'https') == -1:
                #     link_list[i] = url + '/' + link_list[i]
                # print(href)
                try:
                    try:
                        loop = asyncio.get_event_loop()
                        content_html = loop.run_until_complete(get_all_content(link_list[i]))
                    except Exception as e:
                        content_response = requests.get(url=link_list[i], headers=headers, timeout=45, verify=False)
                        content_response.encoding = 'utf-8'
                        content_html = content_response.text

                    # 去除css修饰
                    content_html = re.sub('<span.*?>', '', content_html)
                    content_html = re.sub('</span.*?>', '', content_html)
                    content_html = content_html.replace('™', '').replace('®', '')
                    # patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]', content_html)
                    patent_detail = re.findall('[\w]*[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t\/]*[\u4e00-\u9fa5\d]',
                                               content_html)
                    print(link_list[i])

                    if len(patent_detail) > 0:
                        # patent_detail = str(patent_detail).encode('unicode-escape')
                        print(patent_detail)
                        img_src = re.findall('<img .*?src="(.*?)"', content_html)
                        img_flag = True  # 记录网页中是否含有‘专利’的图片,true-->不含有


                        # 多线程账号
                        record = 0
                        for rec in range(len(account_list)):
                            if account_list[rec]['flag']:
                                record = rec
                                account_list[rec]['flag'] = False
                                break
                        for j in range(len(img_src)):
                            if img_src[j].find('http' or 'https') == -1:
                                img_src[j] = url + '/' + img_src[j]
                            text = ocr_text(name, img_src[j], account_list[record])

                            if '专利证书' in text:
                                img_flag = False
                                state1_flag = False
                                # curr_time = datetime.datetime.now()  # 获取当前时间
                                time_str = time.strftime('%Y-%m-%d %H:%M:%S')
                                print('专利证书信息:', text)
                                patent_num = re.findall('--(专利号.*?)--', text)
                                if len(patent_num) <= 0:
                                    state = "专利号模糊"
                                    values = (
                                        # 公司名，公司url，二级网址，含专利关键字，图片地址，图片文字，预测，获取时间
                                        # 公司名，公司url，二级网址，含专利关键字，预测，备注，获取时间
                                        str(name), str(url), str(link_list[i]), str(patent_detail), str(state),
                                        str(remark), str(time_str))
                                    state2.append(values)
                                if '发明专利证书' or '实用新型专利证书' or '外观设计专利证书' in text:
                                    today = datetime.date.today()
                                    patent_date = re.findall('([0-9]+)年([0-9]+)月([0-9]+)日', text)

                                    try:
                                        if '发明专利证书' in text:
                                            year = int(patent_date[0][0]) + 20
                                        else:
                                            year = int(patent_date[0][0]) + 10
                                        month = int(patent_date[0][1])
                                        day = int(patent_date[0][2])
                                        patent_day = datetime.date(year, month, day)
                                        if today.__gt__(patent_day):
                                            state = "专利号异常"
                                            remark = "专利过期"
                                            print(patent_date, '-' * 100)
                                            values = (
                                                # 公司名，公司url，二级网址，含专利关键字，图片地址，图片文字，预测，获取时间
                                                # 公司名，公司url，二级网址，含专利关键字，预测，备注，获取时间
                                                str(name), str(url), str(link_list[i]), str(patent_detail), str(state),
                                                str(remark), str(time_str))
                                            state3.append(values)
                                    except Exception as e:
                                        pass

                        # 将多线程账号释放
                        account_list[record]['flag'] = True
                        if img_flag:
                            # curr_time = datetime.datetime.now()  # 获取当前时间
                            state = "声称有专利而无专利号或专利证书展示"
                            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
                            values = (
                                # 公司名，公司url，二级网址，含专利关键字，图片地址，图片文字，获取时间
                                str(name), str(url), str(link_list[i]), str(patent_detail), str(state),
                                str(remark), str(time_str))
                            state1.append(values)

                except Exception as e:
                    print("访问失败", e)

            if state1_flag:
                seq_params.extend(state1)
            if len(state2) > 0:
                seq_params.extend(state2)
            if len(state3) > 0:
                seq_params.extend(state3)
            # 调用sql将数据插入数据库
            sql_zl = """
                        insert into "PUDONG_COMPANY"."PATENT_DETAIL8"("NAME", "NAME_URL", "SECOND_URL",
                        "KEYWORDS", "PREDICT", "REMARK", "GET_TIME") VALUES(?,?,?,?,?,?,?);
                        """
            if len(seq_params) > 0:
                db.insert_tb(sql_zl, seq_params)


    else:
        print("此公司无官方网站！")


if __name__ == '__main__':
    db = DataBase()
    sql = """
	select NAME,URL from "PUDONG_COMPANY"."COMPANY_URL"
	"""
    result = db.select_tb(sql)

    account1 = {
        'APP_ID': '21577308',
        'API_KEY': 'GIZsgTXmtdxLAbzNUucUzUQb',
        'SECRET_KEY': '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs',
        'flag': True,
    }
    account2 = {
        'APP_ID': '22423512',
        'API_KEY': 'tSPQWteLhiXV6br3ObBI49hh',
        'SECRET_KEY': 'EoHMbfdjNKGlkWOLGQzUx9pVwsksmygN',
        'flag': True,
    }
    account_list = [account1, account2]
    # print(result, len(result))
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    for i in range(len(result)):
        print("\n=============================正在访问第{}家公司，其名称为：{}=============================".format(i + 1,
                                                                                                      result[i][0]))
        # name = result[i][0]
        # search_url(result[i][0], result[i][1])

        thread_pool.submit(search_url, result[i][0], result[i][1])
    thread_pool.shutdown()
# search_url('https://www.3s-guojian.com')
