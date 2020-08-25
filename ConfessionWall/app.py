#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jmz
@file: app.py.py
@time: 2020/8/25 15:48
@desc:
"""
from tornado import web, ioloop, httpserver


# 视图
class MainPageHandler(web.RequestHandler):
	def get(self, *args, **kwargs):
		self.write('hello xy')

# 表白
class ConfessionHandler(web.RequestHandler):
	def get(self, *args, **kwargs):
		self.render('')
	def post(self, *args, **kwargs):

# 模板

# 路由系统
app = web.Application(
	[
		(r'/', MainPageHandler),
	]
)

if __name__ == '__main__':
	# 前台 socket
	http_server = httpserver.HTTPServer(app)
	http_server.listen(8000)
	ioloop.IOLoop.current().start()
