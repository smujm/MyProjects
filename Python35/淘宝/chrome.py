import pyppeteer.chromium_downloader

# 这里的 mac 替换成你系统的版本，win32，win64，linux，mac 因为我是 mac 所以这里写mac
# 这个是返回在当前系统下chromium的路径
print(pyppeteer.chromium_downloader.chromiumExecutable.get("win64"))
# 这个是返回当前系统默认的下载地址
print(pyppeteer.chromium_downloader.downloadURLs.get("win64"))

"""
在这里使用的是淘宝镜像中的chromium
进入这个网址 https://npm.taobao.org/mirrors/chromium-browser-snapshots
选择对应系统和对应的版本（我这里是mac系统，选择了我系统默认的588429）
"""