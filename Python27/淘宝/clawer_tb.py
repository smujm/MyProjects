# coding=utf-8

import base64
import os
import random
import sys
import time

from aip import AipOcr
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # 等待浏览器加载数据

reload(sys)
sys.setdefaultencoding('utf8')
import re
import requests
import xlwt
import xlrd
from lxml import etree
from PIL import Image


# 百度识字账号
APP_ID = '21577308'
API_KEY = 'GIZsgTXmtdxLAbzNUucUzUQb'
SECRET_KEY = '0taT9GYtOOqvHpTWT1GGX0ncSdqNuZrs'


class taobao:
    def __init__(self):

        # excel创建
        self.f = xlwt.Workbook()  # 创建工作薄
        self.sheet1 = self.f.add_sheet(u'淘宝', cell_overwrite_ok=True)
        self.rowsTitle = [u'编号', u'掌柜', u'名称', u'价格', u'重量/g', u'价格/重量', u'链接', u'产地', u'交易情况',u'注册地址']
        for i in range(0, len(self.rowsTitle)):
            self.sheet1.write(0, i, self.rowsTitle[i], self.set_style('Times new Roman', 220, True))
        self.f.save('taobao.xlsx')

        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options = webdriver.ChromeOptions()
        # 代理ip地址
        # ip = 'http://127.0.0.1'
        # options.add_argument(('--proxy-server=' + ip))
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
        self.driver = webdriver.Chrome(chrome_options=options)

        # 窗口最大化
        self.driver.maximize_window()
        # 打开登录页面
        self.wait = WebDriverWait(self.driver, 20)  # 超时时长为20s
        self.driver.get(
            'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.201864-2.d1.5af911d9WKLvsv&f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F')
        time.sleep(2.8)

    def set_style(self, name, height, bold=False):  # 设置excel表格样式
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.colour_index = 2
        font.height = height
        style.font = font
        return style

    def get_file(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 百度识字
    def baidu(self, filePath):
        image = self.get_file(filePath)
        options = {
            'detect_direction': 'true',
            'language_type': 'ENG',
        }
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # 调用通用文字识别接口
        result = client.basicGeneral(image, options)
        # for word in result['words_result']:
        #     print word['words']
        try:
            code = result['words_result'][0]['words']
        except Exception, e:
            code = '4004'
        return code

    # 判断元素是否存在
    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except Exception, e:
            print '识别失败'
            flag = False
            return flag

    def login2(self):  # 手动扫码登录
        # 淘宝的用户名和密码
        username = "17621374324"
        password = "Ly19980626"
        # 给输入框赋值
        # self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').clear()
        # self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').clear()
        # for i in range(len(username)):
        #     self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username[i])
        #     time.sleep(0.1)
        # for j in range(len(password)):
        #     self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password[j])
        #     time.sleep(0.12)
        #
        # time.sleep(2.7)
        # #模拟滑块滑动
        # action = ActionChains(self.driver)
        # source = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        # action.click_and_hold(source).perform() # 鼠标左键按下不放
        # time.sleep(1.2)
        # matrix = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        # random.shuffle(matrix)
        # for i in range(24):
        #     action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
        #     time.sleep(0.02)
        # action.release().perform()  # 释放鼠标
        self.driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
        time.sleep(10)
        # #once again，有时候让你重新滑动
        # bool = True;
        # while(bool):
        #     try:
        #         time.sleep(2.5)
        #         random.shuffle(matrix)
        #         self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/span/a').click()#刷新
        #         bool = True;
        #         time.sleep(2.6)
        #         action = ActionChains(self.driver)
        #         source = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        #         action.click_and_hold(source).perform() # 鼠标左键按下不放
        #         time.sleep(1.1)
        #         for i in range(24):
        #             action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
        #             # time.sleep(0.001)
        #         action.release().perform()  # 释放鼠标
        #     except Exception, e:
        #         bool = False
        #         print '重复',e.message
        # self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button').click()
        time.sleep(2.8)
        taobao_name = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul[1]/li[2]/div[1]/div[2]/a').text
        print taobao_name  #

    def login(self):  # 自动输入密码并滑动登录
        # 淘宝的用户名和密码
        username = "17621374324"
        password = "Ly19980626"
        # 给输入框赋值
        self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').clear()
        self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').clear()
        for i in range(len(username)):
            self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username[i])
            time.sleep(0.1)
        for j in range(len(password)):
            self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password[j])
            time.sleep(0.12)

        time.sleep(2.7)
        # 模拟滑块滑动
        action = ActionChains(self.driver)
        source = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        action.click_and_hold(source).perform()  # 鼠标左键按下不放
        time.sleep(1.2)
        matrix = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        random.shuffle(matrix)  # 生成随机滑动值
        for i in range(24):
            action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
            time.sleep(0.02)
        action.release().perform()  # 释放鼠标
        # once again，有时候让你重新滑动
        bool = True;
        while (bool):
            try:
                time.sleep(2.5)
                random.shuffle(matrix)
                self.driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/span/a').click()  # 刷新
                bool = True;
                time.sleep(2.6)
                action = ActionChains(self.driver)
                source = self.driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
                action.click_and_hold(source).perform()  # 鼠标左键按下不放
                time.sleep(1.1)
                for i in range(24):
                    action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
                    # time.sleep(0.001)
                action.release().perform()  # 释放鼠标
            except Exception, e:
                bool = False
                print '重复', e.message
        # try:
        #     random.shuffle(matrix)
        #     self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/span/a').click()#刷新
        #     action = ActionChains(self.driver)
        #     source = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        #     action.click_and_hold(source).perform() # 鼠标左键按下不放
        #     time.sleep(1.5)
        #     for i in range(24):
        #         action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
        #         time.sleep(0.03)
        #     action.release().perform()  # 释放鼠标
        # except Exception, e:
        #     print '重复',e.message

        # 模拟点击事件
        # /html/body/div[1]/div/main/div/div/div/div[1]/div/form/button
        self.driver.find_element_by_xpath(
            '/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button').click()  # 找到登录按钮
        time.sleep(2.8)
        taobao_name = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul[1]/li[2]/div[1]/div[2]/a').text
        print taobao_name

    def searchgood(self, good_name):
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(
            good_name.decode("utf-8"))  # 找出搜索框并输入搜索名称
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(Keys.ENTER)

    # 模拟向下滑动
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q = document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.driver.execute_script(js)  # 使用js代码模拟滑动
            time.sleep(0.1)
        time.sleep(0.2)

    # 模拟翻页操作
    def next_page(self, page_number):
        print '-----------------------------------=========================', page_number
        time.sleep(0.5)
        if page_number <= 4:  # 1-4页
            # '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a'
            next_button = self.driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a')
        elif 5 <= page_number <= 6:  # 5-6页
            next_button = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[{}]/a'.format(4 + page_number))
        elif int(self.total_page) - 1 <= page_number <= int(self.total_page):  # 最后倒数两页
            next_button = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[10]/a')
        else:  # 剩余页数
            next_button = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[11]/a')
        # 获取页码输入框
        next_input = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[2]/input')
        # 将当前输入框中的内容清空，并重置为page_number
        next_input.clear()
        next_input.send_keys(page_number)

        time.sleep(1.8)
        next_button.click()

    # 得到所有的页数
    def get_total_page(self):
        time.sleep(5.4)
        # 先等待所有的商品都加载完/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]
        page_total = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]').text
        print page_total
        result = page_total.strip("共 ").replace(' 页，', '')
        return result

    # 得到商品集
    def get_infos(self):
        self.total_page = self.get_total_page()

        for i in range(1, int(self.total_page) + 1):
            # 等待页面商品数据加载完成
            time.sleep(2.6)
            # 模拟向下滑动
            self.swipe_down(2)
            try:
                # 获取本页面源代码
                html = self.driver.page_source
                # print html
                s = etree.HTML(html)
                tds = s.xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[21]/div/div/div[1]/div/div[2]')
                # 打开excel文件
                data = xlrd.open_workbook('taobao.xlsx')
                table = data.sheets()[0]  # 通过索引顺序获取table, 一个execl文件一般都至少有一个table
                rowCount = table.nrows  # 获取行数   ，下次从这一行开始
                m = 0  # 计数
                for td in tds:
                    data = []

                    manager = td.xpath('./div[3]/div[1]/a/span[2]/text()')  # 掌柜名
                    name = td.xpath('./div[2]/a')  # 商品名
                    # name_info = name.xpath('string(.)').extract()
                    price = td.xpath('./div[1]/div[1]/strong/text()')  # 价格
                    href = td.xpath('./div[2]/a/@href')  # 链接
                    source = td.xpath('./div[3]/div[2]/text()')  # 产地
                    num_payers = td.xpath('./div[1]/div[2]/text()')  # 购买人数
                    icon = td.xpath('./div[4]/div[1]/ul/li/a/span/@class')  # 天猫标志

                    manager = manager[0] if len(manager) > 0 else ''
                    name = name[0].xpath('string(.)') if len(name) > 0 else ''
                    name = name.replace(' ', '').replace("\n", "").replace("\r", "")
                    # name_info = name_info if len(name_info) > 0 else ''
                    price = price[0] if len(price) > 0 else ''
                    href = href[0] if len(href) > 0 else ''
                    source = source[0] if len(source) > 0 else ''
                    num_payers = num_payers[0] if len(num_payers) > 0 else ''
                    icon = icon[0] if len(icon) > 0 else ''

                    weight = ''
                    Tcode_data = ''

                    if icon == "icon-service-tianmao":  # 如果是天猫店铺
                        self.driver.get('https:' + href)
                        html = self.driver.page_source  # 进入天猫店铺
                        s = etree.HTML(html)
                        time.sleep(2)

                        try:
                            logo = s.xpath('//*[@id="mallLogo"]/span/a/@href')  # 判断天猫类型
                            logo = logo[0] if len(logo) > 0 else '0'
                            # 处理天猫超市
                            if logo == "//chaoshi.tmall.com?notjump=true&_ig=logo":
                                # 重量
                                weight = s.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[3]/dl[2]/dd/em/text()')
                                weight = weight[0] if len(weight) > 0 else ''
                                weight = (float(weight) * 1000)
                                price_item = ''

                            # 处理除天猫超市的天猫店铺
                            else:
                                weight = s.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[3]/dl[2]/dd/text()')
                                weight = weight[0] if len(weight) > 0 else ''
                                weight = weight.replace('g', '')

                                price_item = s.xpath('//*[@id="J_StrPriceModBox"]/dd/span[2]/text()')  # 价格/重量
                                price_item = price_item[0] if len(price_item) > 0 else ''

                                img_name = manager + '.png'  # 图片取名字
                                flag1 = os.path.exists('CoLicense' + '/' + img_name)
                                print flag1
                                if flag1:
                                    print "已经存在"
                                else:
                                    co_href = re.findall(r'href="(.*?)" class="tm-gsLink"', html, re.I)  # 公司资质链接
                                    co_href = co_href[0] if len(co_href) > 0 else ''
                                    co_href = co_href.replace("u'", '').replace("'", '')
                                    self.driver.get('https:' + co_href)  # 进入公司资质链接
                                    html = self.driver.page_source
                                    s = etree.HTML(html)
                                    time.sleep(1)
                                    flag = True
                                    while flag:  # 若flag为真，验证码匹配失败，则验证码重新输入
                                        try:
                                            img_href = s.xpath('//*[@id="J_CheckCode"]/@data-url')  # 验证码链接
                                            img_href = img_href[0] if len(img_href) > 0 else ''
                                            headers = {
                                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

                                            response = requests.get(url='http:' + img_href, headers=headers)  # 请求验证码链接
                                            img_data = response.content  # 读取验证码数据
                                            with open('yzm.jpg', mode='wb') as f:  # 写入验证码
                                                f.write(img_data)
                                            code = self.baidu('yzm.jpg')  # 调用接口识别验证码
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').clear()  # 清除输入框
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').send_keys(code)  # 输入验证码
                                            self.driver.find_element_by_xpath(
                                                '/html/body/div/div/div/div[1]/form/input[2]').send_keys(Keys.ENTER)
                                            time.sleep(2)
                                            html_flag = self.driver.page_source  # 获取网页源码
                                            s_flag = etree.HTML(html_flag)
                                            # 判断是否存在“确定”按钮
                                            button = s_flag.xpath(
                                                '//*[@id="J_LicenceCheckPop"]/div/div/div[1]/form/div[1]/button/text()')
                                            if len(button) > 0:
                                                flag = True
                                                self.driver.back()  # 每错误一次回退到页面
                                            else:
                                                flag = False

                                        except Exception, e:
                                            print '验证码出错', e.message
                                    img_src = s_flag.xpath('/html/body/div/div[2]/div/img/@src')  # 返回企业加密信息
                                    img_src = img_src[0] if len(img_src) > 0 else ''
                                    img_src = img_src.replace('data:image/png;base64,', '')  # 去除头部不需要信息
                                    img_src_data = base64.b64decode(img_src)  # 对企业信息进行解密

                                    with open('CoLicense' + '/' + img_name, 'wb') as f:  # 写入图片
                                        f.write(img_src_data)
                                    self.driver.back()  # 回到验证码

                                    self.driver.back()  # 回到店铺

                        except Exception, e:
                            print 'weight出错1', e.message

                        self.driver.back()  # 回到搜索店铺
                    else:  # 淘宝店铺  ‘//scportal.taobao.com/quali_show.htm?uid=2207759828325&qualitype=1’
                        href = href.replace("https:", '')
                        self.driver.get('https:' + href)  # 进入店铺详情
                        html = self.driver.page_source
                        s = etree.HTML(html)
                        time.sleep(2)
                        try:
                            weight = s.xpath('//*[@id="detail"]/div[1]/div[1]/div/div[2]/div/div/ul/li[2]/text()')
                            weight = weight[1] if len(weight) > 0 else ''
                            weight = weight.replace(' ', '').replace('g', '').replace("\n", "")
                            # print weight
                            price_item = s.xpath('//*[@id="J_StrPriceModBox"]/div/span/text()')
                            price_item = price_item[0] if len(price_item) > 0 else ''
                        except Exception, e:
                            print "weight出错2", e.message

                        shopInfo = s.xpath('//*[@id="J_ShopInfo"]/div[2]/div[1]/div[5]/dl/dd/a[1]/@class')
                        shopInfo = shopInfo[0] if len(shopInfo) > 0 else ''  # 判断是否支付宝个人认证

                        if (shopInfo == 'tb-icon tb-icon-alipay-persion-auth'):  # 若是个人店铺
                            # '//scportal.taobao.com/quali_show.htm?spm=a1z10.1-c-s.0.0.6db96af9smeyNG&uid=47915300&qualitype=1'
                            shipIcon = s.xpath('//*[@class="tb-icon tb-icon-qualification"]/@href')
                            shipIcon = shipIcon[0] if len(shipIcon) > 0 else ''
                            if(shipIcon != ''):
                                shipIcon = shipIcon.replace('all', '1')
                                self.driver.get(shipIcon)  # 进入店铺验证码环节
                                html = self.driver.page_source
                                ss = etree.HTML(html)
                                time.sleep(1)

                                action = ActionChains(self.driver)
                                source = self.driver.find_element_by_xpath(
                                    "/html/body/div/form/div/div/div[1]/span")  # 需要滑动的元素
                                action.click_and_hold(source).perform()  # 鼠标左键按下不放
                                time.sleep(0.5)
                                # matrix = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                #           24]
                                # random.shuffle(matrix)  # 生成随机滑动值
                                # for i in range(24):
                                action.move_by_offset(470, 0)  # 需要滑动的坐标
                                time.sleep(0.02)
                                action.release().perform()  # 释放鼠标
                                time.sleep(1)
                                flag = True
                                while flag:  # 若flag为真，验证码匹配失败，则验证码重新输入
                                    try:
                                        # 获取截图
                                        self.driver.get_screenshot_as_file('VfCode/screenshot.png')
                                        # 获取指定元素位置
                                        # element = self.driver.find_element_by_id('checkcode')
                                        left = 783 + 128
                                        top = 150
                                        right = left + 205
                                        bottom = top + 60

                                        # 通过image处理图像
                                        im = Image.open('VfCode/screenshot.png')
                                        im = im.crop((left, top, right, bottom))
                                        im.save('VfCode/yzm.png')

                                        # code_href = s.xpath('//*[@id="nc_1__imgCaptcha_img"]/img/@src')  # 验证码链接
                                        # code_href = code_href[0] if len(code_href) > 0 else ''
                                        # decode_href = code_href.replace('data:image/jpg;base64,', '')  # 去除头部不需要信息
                                        # decode_data = base64.b64decode(decode_href)  # 对验证码信息进行解密
                                        #
                                        # with open('VfCode' + '/' + 'yzm.jpg', 'wb') as f:  # 写入图片
                                        #     f.write(decode_data)

                                        Tcode = self.baidu('VfCode' + '/' + 'yzm.png')  # 调用接口识别验证码
                                        self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').clear()  # 清除输入框
                                        self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').send_keys(Tcode)  # 输入验证码
                                        self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').send_keys(Keys.ENTER)
                                        self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                        checkcode_html = self.driver.page_source  # 获取网页源码
                                        checkcode_s = etree.HTML(checkcode_html)
                                        self.wait = WebDriverWait(self.driver, 10)  # 超时时长为20s
                                        # 判断是否存在checkcode
                                        checkcode = checkcode_s.xpath('//*[@id="formId"]/@class')
                                        if len(checkcode) > 0:
                                            flag = True
                                            print '需要重新验证'
                                        else:
                                            flag = False
                                            print '验证成功'
                                    except Exception, e:
                                        print 'taobao验证码出错', e.message
                                Tcode_html = self.driver.page_source  # 获取网页源码
                                Tcode_res = etree.HTML(Tcode_html)
                                Tcode_data = Tcode_res.xpath('//*[@id="index"]/div[3]/div[2]/text()')
                                Tcode_data = Tcode_data[0] if len(Tcode_data) > 0 else ''
                                self.driver.back()  # 回到滑块验证
                                self.driver.back()  # 回到店铺
                        self.driver.back()  # 回到搜索店铺

                    # 拼装成一个集合
                    data.append(rowCount + m)
                    data.append(manager)
                    data.append(name)
                    data.append(price)
                    data.append(weight)
                    data.append(price_item)
                    data.append(href)
                    data.append(source)
                    data.append(num_payers)
                    data.append(Tcode_data)

                    for j in range(len(data)):  # 写入数据
                        self.sheet1.write(rowCount + m, j, data[j])
                    m += 1

                    print manager, name, price, weight, href, source, num_payers



            except Exception, e:
                print '出错', e.message
            finally:
                self.f.save('taobao.xlsx')

            time.sleep(2)
            # 下一页
            if i < int(self.total_page):
                self.next_page(i + 1)


if '__main__':
    tb = taobao()
    tb.login2()
    tb.searchgood("8424西瓜")
    # tb.get_total_page()
    tb.get_infos()
