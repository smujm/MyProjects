# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random


class taobao:
    def __init__(self):
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options = webdriver.ChromeOptions()
        #代理ip地址
        # ip = 'http://127.0.0.1'
        # options.add_argument(('--proxy-server=' + ip))
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # ，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
        self.driver = webdriver.Chrome(chrome_options=options)
        # 窗口最大化
        self.driver.maximize_window()
        # 打开登录页面
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get('https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.201864-2.d1.5af911d9WKLvsv&f=top&redirectURL=http%3A%2F%2Fwww.taobao.com%2F')
        time.sleep(2.8)

    def login(self):
        #淘宝的用户名和密码
        username = "17621374324"
        password = "Ly19980626"
        #给输入框赋值
        self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').clear()
        self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').clear()
        for i in range(len(username)):
            self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username[i])
            time.sleep(0.1)
        for j in range(len(password)):
            self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password[j])
            time.sleep(0.12)

        time.sleep(2.7)
        #模拟滑块滑动
        action = ActionChains(self.driver)
        source = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        action.click_and_hold(source).perform() # 鼠标左键按下不放
        time.sleep(1.2)
        matrix = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        random.shuffle(matrix)
        for i in range(24):
            action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
            time.sleep(0.02)
        action.release().perform()  # 释放鼠标
        #once again，有时候让你重新滑动
        bool = True;
        while(bool):
            try:
                time.sleep(2.5)
                random.shuffle(matrix)
                self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/span/a').click()#刷新
                bool = True;
                time.sleep(2.6)
                action = ActionChains(self.driver)
                source = self.driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
                action.click_and_hold(source).perform() # 鼠标左键按下不放
                time.sleep(1.1)
                for i in range(24):
                    action.move_by_offset(matrix[i], 0)  # 需要滑动的坐标
                    # time.sleep(0.001)
                action.release().perform()  # 释放鼠标
            except Exception, e:
                bool = False
                print '重复',e.message
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

        #模拟点击事件
        #/html/body/div[1]/div/main/div/div/div/div[1]/div/form/button
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button').click()
        time.sleep(2.8)
        taobao_name = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul[1]/li[2]/div[1]/div[2]/a').text
        print taobao_name

    def searchgood(self,good_name):
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(good_name.decode("utf-8"))
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div[3]/div/input').send_keys(Keys.ENTER)
    # 模拟向下滑动
    def swipe_down(self,second):
        for i in range(int(second/0.1)):
            js = "var q = document.documentElement.scrollTop=" + str(300+200*i)
            self.driver.execute_script(js)
            time.sleep(0.1)
        time.sleep(0.2)
    #模拟翻页操作
    def next_page(self,page_number):
        #获取下一页按钮，
        next_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/ul/li[8]/a')
        # 获取页码输入框
        next_input = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[2]/input')
        #将当前输入框中的内容清空，并重置为page_number
        next_input.clear()
        next_input.send_keys(page_number)

        time.sleep(2)
        next_button.click()

    #得到所有的页数
    def get_total_page(self):
        time.sleep(5.4)
        #先等待所有的商品都加载完/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]
        page_total = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[1]').text
        print page_total
        result = page_total.strip("共 ").replace(' 页，','')
        print result



if '__main__':
    tb = taobao()
    tb.login()
    tb.searchgood("8424西瓜")
    tb.get_total_page()