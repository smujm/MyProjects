#coding=utf-8
from PIL import Image
left = 783 + 128
top = 150
right = left + 205
bottom = top+ 60

# 通过image处理图像
im = Image.open('VfCode/screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('VfCode/yzm.png')