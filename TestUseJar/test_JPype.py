from jpype import *
import jpype
import os

# 静态方法
# jar_path = os.path.join(os.path.abspath('.'), r'D:\UseJar\teatPython.jar')  # jar路径
# # jvm_path = getDefaultJVMPath()
# # jpype.startJVM(jvm_path, '-Djava.class.path=%s' % jar_path, convertStrings=True)
# # JPackage = jpype.JPackage('utils')
# # sum = JPackage.testPython.add(5, 10)
# # print(sum)
# # jpype.shutdownJVM()

# 非静态方法
jar_path = os.path.join(os.path.abspath('.'), r'D:\UseJar\webAllUrl(2).jar')  # jar路径
jvm_path = getDefaultJVMPath()
jpype.startJVM(jvm_path, '-Djava.class.path=%s' % jar_path, convertStrings=True)
JClass = jpype.JClass('util.WebCrawlerDemo')
instance = JClass()		# 建立对象
link_list = instance.myPrint('https://www.3s-guojian.com')
url_list = []
for i in range(len(link_list)):
	url_list.append(link_list[i])
jpype.shutdownJVM()
print(url_list)