# coding=utf-8

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

class taobao:
    def __init__(self):
        #淘宝的用户名和密码
        username = "17621374324"
        password = "Ly19980626"
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        #，获取浏览器的驱动，这里需要提前给chrome指定环境变量，如果没有指定则需要指定路径
        driver = webdriver.Chrome(chrome_options=options)
        #窗口最大化
        driver.maximize_window()
        #打开登录页面
        driver.get('https://login.taobao.com/member/login.jhtml')

        time.sleep(2.8)

        #给输入框赋值
        driver.find_element_by_xpath('//*[@id="fm-login-id"]').clear()
        driver.find_element_by_xpath('//*[@id="fm-login-password"]').clear()
        driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)

        time.sleep(5.7)
        #模拟滑块滑动
        action = ActionChains(driver)
        source = driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        action.click_and_hold(source).perform() # 鼠标左键按下不放
        time.sleep(1.2)
        action.move_by_offset(298, 0)  # 需要滑动的坐标
        action.release().perform()  # 释放鼠标
        #once again，有时候让你重新滑动
        time.sleep(2.5)
        driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/span/a').click()#刷新
        action = ActionChains(driver)
        source = driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[3]/div[2]/div/div[1]/span")  # 需要滑动的元素
        action.click_and_hold(source).perform() # 鼠标左键按下不放
        time.sleep(2.5)
        action.move_by_offset(298, 0)  # 需要滑动的坐标
        action.release().perform()  # 释放鼠标

        #模拟点击事件
        #/html/body/div[1]/div/main/div/div/div/div[1]/div/form/button
        driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button').click()

        time.sleep(2.8)
        #点击输入
        driver.find_element_by_xpath('/html/body/header/article/nav/div/div/form/div[2]/div/div/div/div/input').send_keys("8424西瓜".decode("utf-8"))
        driver.find_element_by_xpath('/html/body/header/article/nav/div/div/form/div[2]/div/div/div/div/input').send_keys(Keys.ENTER)

if '__main__':
    tb = taobao()


os.system("pause")