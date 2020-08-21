#coding=utf-8
from PIL import Image
import pytesseract

img = Image.open(r'/id_code/get_img (3).jfif')

#二值化图像传入图像和阈值
def erzhihua(image, threshold):
    '''type image:Image.Image'''
    image = image.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')

# img = erzhihua(img, 127)
img.show()

res = pytesseract.image_to_string(img, lang="eng")
print res