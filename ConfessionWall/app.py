#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: app.py.py
@time: 2020/8/25 15:48
@desc:
"""
from tornado import web, ioloop, httpserver

# 留言

MESSAGES = [
	{'id': 1, 'name': 'xm', 'time': '2020-8-24 21:16:00', 'content': '爱你', 'num': 1}
]


# 视图
class MainPageHandler(web.RequestHandler):
	def get(self, *args, **kwargs):
		self.write('hello xy')


# 表白
class ConfessionHandler(web.RequestHandler):
	def get(self, *args, **kwargs):
		self.render('index.html')
	
	def post(self, *args, **kwargs):
		pass


# 设置
settings = {
	'template_path': '前端文件\\templates',  # 模板文件路径
	'static_path': '前端文件\\statics',  # 静态文件路径
}

# 模板

# 路由系统
app = web.Application(
	[
		(r'/', ConfessionHandler),
	], **settings
)

if __name__ == '__main__':
	# 前台 socket
	http_server = httpserver.HTTPServer(app)
	http_server.listen(8000)
	ioloop.IOLoop.current().start()
