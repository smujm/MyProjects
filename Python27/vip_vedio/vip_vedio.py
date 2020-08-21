# coding=utf-8
import requests
import re
import tkinter as tk

import webbrowser
try:
    url = 'http://www.qmaile.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    response_text = response.text
    # print(response_text)
    
    res = re.compile('<option value="(.*?)" selected="">')
    res_data = re.findall(res, response_text)
    # print(res_data)
except Exception as e:
    print("换个网站")
    url = 'https://www.bavei.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    response_text = response.text
    # print(response_text)
    
    res = re.compile('<option value="(.*?)">')
    res_data = re.findall(res, response_text)
    # print(res_data)
    
    
one = res_data[0]
two = res_data[1]
three = res_data[2]
four = res_data[3]
five = res_data[4]

root = tk.Tk()
root.title('vip播放by-xm')
root.geometry('600x250')
root.resizable(0, 0)  # 设置窗口大小不可变

var = tk.StringVar()
l1 = tk.Label(root, text='播放接口', font=8)
l1.grid()

r1 = tk.Radiobutton(root, text='播放接口1', variable=var, value=one)
r1.grid(row=0, column=1)
r2 = tk.Radiobutton(root, text='播放接口2', variable=var, value=two)
r2.grid(row=1, column=1)
r3 = tk.Radiobutton(root, text='播放接口3', variable=var, value=three)
r3.grid(row=2, column=1)


r4 = tk.Radiobutton(root, text='播放接口4', variable=var, value=four)
r4.grid(row=3, column=1)
r5 = tk.Radiobutton(root, text='播放接口5', variable=var, value=five)
r5.grid(row=4, column=1)
l2 = tk.Label(root, text='播放链接:', font=12)
l2.grid(row=5, column=0)
e = tk.StringVar()
e1 = tk.Entry(root, textvariable=e, width=50)
e1.grid(row=5, column=1)


def button_add():
    webbrowser.open(var.get() + e.get())
button1 = tk.Button(root, text="播放", font=12, width=8, command=button_add)
button1.grid(row=6, column=1)


def button_del():
    e1.delete(0, 'end')
button2 = tk.Button(root, text="清除", font=12, width=8, command=button_del)
button2.grid(row=7, column=1)

menubar = tk.Menu(root)
helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='帮助(H)', menu=helpmenu)
helpmenu.add_command(label='输入完链接请点击播放接口')
helpmenu.add_command(label='接口不行请更换接口')
root.config(menu=menubar)

root.mainloop()
