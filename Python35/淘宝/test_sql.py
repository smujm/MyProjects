import dmPython

user = 'SYSDBA'
password = 'citygis1613'
server = '106.14.243.179'
port = 5236


class database:
	def __init__(self):
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
			print("查询全部结果：", result1)
			# print(result1[1][0])
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
			
db = database()

sql = """
select PROGRAMNAME from "TENCENTAPI"."SPIDERINDEX" where WEBNAME = '淘宝' and FLAG = 0
"""
sql4 = """
insert into "TENCENTAPI"."taobao_jd"("平台", "店铺名称", "店铺URL", "商品名称", "商品URL", "价格", "重量", "单价(元/500g)", "获取日期") VALUES(?,?,?,?,?,?,?,?,?);
"""
data = [('jd','tainamo', 'www', '464', '56w', 50, '55kg', '345', '2020-1-1')]

# db.insert_tb(sql4, data)
db.select_tb(sql)

sql2 = """
update "TENCENTAPI"."SPIDERINDEX" set FLAG = 1 where WEBNAME = '淘宝' and PROGRAMNAME = '{}'
""".format('香蕉')

print(sql2)
db.update(sql2)

