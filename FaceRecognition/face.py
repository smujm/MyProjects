import PIL
import base64
import tkinter as tk
from aip import AipFace
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

# 百度 aip
APP_ID = '19895116'
API_KEY = 'aR6Oytn7ycDyhjBqPYCAGgqh'
SECRET_KEY = 'dXjz8QELSaj238GuEr0I3xnarEurWhit'
face = AipFace(APP_ID, API_KEY, SECRET_KEY)
image_type = 'BASE64'
options = {'face_field': 'age,gender,beauty'}


def get_file_base64(file_path):
    with open(file_path, 'rb') as fr:
        content = base64.b64encode(fr.read())
        return content.decode('utf8')


def get_score(file_path):
    # 脸部识别分数
    result = face.detect(get_file_base64(file_path), image_type, options)
    # print(result)
    age = result['result']['face_list'][0]['age']
    beauty = result['result']['face_list'][0]['beauty']
    gender = result['result']['face_list'][0]['gender']['type']
    return age, beauty, gender


class FaceScore():
    root = tk.Tk()
    # 设置窗口大小
    root.geometry('700x450')
    # 为窗口添加标题
    root.title('颜值测试工具')
    # 设置背景色
    canvas = tk.Canvas(root,
                       width=700,
                       height=450,
                       bg='#EEE8AA')
    canvas.pack()

    def start(self):
        # 照片选择按钮
        tk.Button(self.root, text='选择照片', font=('华文行楷', 16), command=self.show_img).place(x=40, y=180)
        # 颜值测试按钮
        tk.Button(self.root, text='查看颜值', font=('华文行楷', 16), command=self.set_score).place(x=40, y=280)
        # 标题
        tk.Label(self.root,
                 width=20,
                 height=1,
                 text='一张照片测颜值',
                 font=('华文行楷', 28),
                 bg='#EEE8AA',
                 fg='#0AB0D5').place(x=160, y=50)
        # 设置图片大小
        self.label_img_original = tk.Label(self.root)
        # 设置显示图框背景
        self.cv_orinial = tk.Canvas(self.root, bg='#EEE8AA', width=270, height=270)
        # 设置位置
        self.cv_orinial.place(x=195, y=130)
        # 设置显示图片位置
        self.label_img_original.place(x=195, y=130)
        tk.Label(self.root, text='性别', bg='#EEE8AA', fg='#0AB0D5', font=('华文行楷', 20)).place(x=500, y=150)
        self.text1 = tk.Text(self.root, width=10, height=2)
        tk.Label(self.root, text='年龄', bg='#EEE8AA', fg='#0AB0D5', font=('华文行楷', 20)).place(x=500, y=260)
        self.text2 = tk.Text(self.root, width=10, height=2)
        tk.Label(self.root, text='颜值', bg='#EEE8AA', fg='#0AB0D5', font=('华文行楷', 20)).place(x=500, y=360)
        self.text3 = tk.Text(self.root, width=10, height=2)
        # 填装文字
        self.text1.place(x=580, y=150)
        self.text2.place(x=580, y=260)
        self.text3.place(x=580, y=360)
        # 循环
        self.root.mainloop()

    def show_img(self):
        self.path_ = askopenfilename(title='选择照片')
        # 处理文件
        if self.path_.strip() != '':
            img = Image.open(self.path_)
            img = img.resize((270, 270), PIL.Image.ANTIALIAS)  # 调整图片大小至270*270
            # 生成 tkinter 图片对象
            img_png_original = ImageTk.PhotoImage(img)
            # 设置图片对象
            self.label_img_original.config(image=img_png_original)
            self.label_img_original.image = img_png_original
            self.cv_orinial.create_image(5, 5, anchor='nw', image=img_png_original)

    def set_score(self):
        if hasattr(self, 'path_') and self.path_.strip() != '':
            # 获取百度接口返回的年龄、分数、性别
            age, score, gender = get_score(self.path_)
            if gender == 'male':
                gender = '男'
            elif gender == 'female':
                gender = '女'
            # 清除文本框内容并进行插入
            self.text1.delete(1.0, tk.END)
            self.text1.tag_config('black', foreground='black')
            self.text1.insert(tk.END, gender, 'black')
            self.text2.delete(1.0, tk.END)
            self.text2.tag_config('black', foreground='black')
            self.text2.insert(tk.END, age, 'black')
            self.text3.delete(1.0, tk.END)
            self.text3.tag_config('black', foreground='black')
            self.text3.insert(tk.END, score, 'black')


fs = FaceScore()
fs.start()
