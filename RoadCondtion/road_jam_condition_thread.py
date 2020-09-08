#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: road_jam_condition.py
@time: 2020/9/1 15:39
@desc:
"""

import time

import dmPython
import requests


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


db = DataBase()
sql = """
	select NAME, CITY from "ROAD_CONDITION"."ROADS" 
	"""
results = db.select_tb(sql)
base_url = 'http://api.map.baidu.com/traffic/v1/road?'
ak = '7DAlBDu0LsE8ohFybgKDkD7P9lKlszGQ'
estimate = ['畅通', '较为畅通', '缓行', '轻微拥堵', '拥堵', '严重拥堵']
ak_list = ['HCW0Wb8MVw3YvOVyAyTjtScbjGkV8rfw',
           'eN7QThzwM7pe9vE5Xb73LIxma0LQYahU',
           'Inhhi1GKHGm5wauG7D9y3ba0wnMiYBGF',
           'xB3n6CxAVVUYijVwW4O3UcamGCsidBBe',
           'NUHvhki5aQzzDUxEtEY4wU8HcmgEOS6R']
li = 0


def get_detail(json):
    # 路况语义化描述
    description = rjson['description']
    # 路况整体评估
    status = estimate[rjson['evaluation']['status']]
    status_desc = rjson['evaluation']['status_desc']
    # 路况详细信息
    road_traffic = rjson['road_traffic'][0]
    road_name = road_traffic['road_name']
    # 若有拥堵路段
    status_est = ['未知路况', '畅通', '缓行', '拥堵', '严重拥堵']
    params = []
    if 'congestion_sections' in road_traffic:
        for con in road_traffic['congestion_sections']:
            congestion_distance = con['congestion_distance']
            speed = con['speed']
            status2 = status_est[con['status']]
            congestion_trend = con['congestion_trend']
            section_desc = con['section_desc']

            # 建立values
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            values = (road_name, description, status, status_desc, congestion_distance,
                      speed, status2, congestion_trend, section_desc, time_str)
            params.append(values)
    else:
        # 建立values
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        values = (road_name, description, status, status_desc, '/',
                  0, '/', '/', '/', time_str)
        params.append(values)

    return params


for result in range(len(results)):
    name = results[result][0]
    address = results[result][1]
    url = base_url + 'road_name={}&city={}&ak={}'.format(name, address, ak)
    response = requests.get(url)
    rjson = response.json()
    seq_params = []  # 存入数据库中的数组
    if rjson['status'] == 0:  # 本次API访问状态，如果成功返回0，如果失败返回其他数字
        print(name, '{}请求:'.format('-' * 100), rjson['message'])
        seq_params = get_detail(rjson)

    elif rjson['status'] == 302:
        print(name, '{}请求:失败,'.format('-' * 96), rjson['message'])
        ak = ak_list[li]
        if li < len(ak_list) - 1:
            li += 1
        url = base_url + 'road_name={}&city={}&ak={}'.format(name, address, ak)
        response = requests.get(url)
        rjson = response.json()
        if rjson['status'] == 0:  # 本次API访问状态，如果成功返回0，如果失败返回其他数字
            print(name, '{}请求:'.format('-' * 100), rjson['message'])
            seq_params = get_detail(rjson)

            # record += 1
    # if record >= 49:
    # 调用sql将数据插入数据库,每次插入50条
    sql_zl = """
               insert into "ROAD_CONDITION"."BAIDU_ROADS2"("NAME", "DESCRIPTION", "STATUS",
               "STATUS_DESC", "CONGESTION_DISTANCE", "SPEED", "STATUS2", "CONGESTION_TREND", "SECTION_DESC","GET_TIME") VALUES(?,?,?,?,?,?,?,?,?,?);
               """
    if len(seq_params) > 0:
        db.insert_tb(sql_zl, seq_params)
