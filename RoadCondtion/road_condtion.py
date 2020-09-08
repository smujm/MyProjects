#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: road_condtion.py
@time: 2020/9/1 10:58
@desc:
"""

import requests
import json
import time
import pprint
import dmPython
import math


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


left_bottom = [121.12034, 30.927838]
right_top = [121.692956, 31.326482]

part_n = math.ceil(max((right_top[0] - left_bottom[0]) / 0.05, (right_top[1]-left_bottom[1]) / 0.05))

# part_n = 5  # 设置区域网格2*2
base_url = 'http://api.map.baidu.com/place/v2/search?'
x_item = (right_top[0] - left_bottom[0]) / part_n
y_item = (right_top[1] - left_bottom[1]) / part_n
quary = '道路'  # 搜索关键字
ak = '7DAlBDu0LsE8ohFybgKDkD7P9lKlszGQ'
n = 0  # 切片计数器
db = DataBase()

for i in range(part_n):
    for j in range(part_n):
        # 切片的左下角
        left_bottom_part = [left_bottom[0] + i * x_item, left_bottom[1] + j * y_item]
        # 切片的右上角
        right_top_part = [right_top[0] - (part_n - i - 1) * x_item, right_top[1] - (part_n - j - 1) * y_item]
        seq_params = []  # 插入到数据库的数组
        for k in range(20):
            url = base_url + 'query={}&page_size=20&page_num={}&scope=1'.format(quary, str(k)) + '&bounds=' + str(
                left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ',' + str(right_top_part[1]) + ',' + str(
                right_top_part[0]) + '&output=json&ak=' + ak
            time.sleep(1.51)
            data = requests.get(url)
            # pprint.pprint(data.json())
            print(data.text)
            hjson = json.loads(data.text)
            if hjson['message'] == 'ok':
                results = hjson['results']
                if len(results) <= 0:
                    break
                else:
                    for m in range(len(results)):  # 提取返回的结果
                        # print(results[m]['name'])
                        name = results[m]['name']
                        address = results[m]['address']
                        province = results[m]['province']
                        city = results[m]['city']
                        area = results[m]['area']
                        detail = results[m]['detail']
                        lat = results[m]['location']['lat']
                        lng = results[m]['location']['lng']
                        uid = results[m]['uid']
                        values = (name, address, province, city, area, detail, lat, lng, uid)
                        seq_params.append(values)
        # 调用sql将数据插入数据库
        sql_zl = """
                    insert into "ROAD_CONDITION"."ROADS"("NAME", "ADDRESS", "PROVINCE",
                    "CITY", "AREA", "DETAIL", "LAT", "LNG", "ID") VALUES(?,?,?,?,?,?,?,?,?);
                    """
        if len(seq_params) > 0:
            db.insert_tb(sql_zl, seq_params)

        n += 1
        print('第{}个切片成功'.format(n))
