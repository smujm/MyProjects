import requests
import re
import os


class DealFile:
    def write_txt_file(self, path, url):
        try:
            with open(path, mode='w', encoding='utf-8') as f:
                f.write(url)
                f.close()
        except Exception as e:
            print("写入文件失败", e)

    def read_txt_file(self, path):
        result = ''  # 读取结果
        this_line = ''  # 每次读取的行
        try:
            with open(path, mode='r') as f:
                this_line = f.readline()
                while this_line != '':
                    result += this_line + "\n"
                f.close()
        except Exception as e:
            print("读取文件失败", e)
        return result

    def get_file_line(self, path, num):
        this_line = ''
        this_num = 0
        try:
            f = open(path)
            this_line = f.readline()
            while this_line != '':
                if num == this_num:
                    return this_num
                this_num += 1
        except Exception as e:
            print("读取指定行数失败", e)
        return ''

    def get_file_count(self, file):
        count = 0
        try:
            f = open(file)
            while f.readline() is not None:
                count += 1
        except Exception as e:
            print("读取文件总行数失败", e)
        return count


a_link_file = r'LinkFile/ALinks.txt'
img_link_file = r'LinkFile/ImgLinks.txt'
doc_link_file = r'LinkFile/DocLinks.txt'
error_link_file = r'LinkFile/ErrorLinks.txt'
files = [a_link_file, img_link_file, doc_link_file, error_link_file]
try:
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        os.mknod(file, mode=0, device=0)
except Exception as e:
    print('创建文件失败', e)

numbers = -1
sums = 0

def get_all_url(url):
    headers = {
        "Referer": url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    if url != '-':
        global numbers
        try:
            start_url = url
            response = requests.get(start_url, headers=headers)
        except Exception as e:
            df.write_txt_file(error_link_file, url + '\r\n')
            numbers += 1
            if sums > numbers:
                get_all_url(df.get_file_line(a_link_file, numbers))
            return
        else:
            print("开始链接：", url)
            response.encoding = response.apparent_encoding  # 自动获取编码
            html = response.text
            # print(html)
            start_hrefs = re.findall('a href="(.*?)"', html)
            start_hrefs = set(start_hrefs)  # 去除重复网址
            for href in start_hrefs:
                if href.find('http' or 'https') == -1:
                    href = start_url + '/' + href
                # print(href)
                if not df.read_txt_file(a_link_file).find(href):
                    if href.find(url):
                        # 判断该a标签的内容是文件还是子链接
                        if not (href.find(".doc") or href.find(".exl")
                                or href.find(".exe") or href.find(".apk")
                                or href.find(".mp3") or href.find(".mp4")):
                            df.write_txt_file(a_link_file, href + "\r\n")
                            global sums
                            sums += 1
                try:
                    content_response = requests.get(url=href, headers=headers, timeout=25)
                    content_html = content_response.text
                    # 去除css修饰
                    content_html = re.sub('<span.*?>', '', content_html)
                    content_html = re.sub('</span.*?>', '', content_html)
                    # patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]', content_html)
                    patent_detail = re.findall('[\u4e00-\u9fa5][^，。<>_\n\t]*专利[^，。<>_\n\t]*[\u4e00-\u9fa5\d]',
                                               content_html)
                    print(href)
                    if len(patent_detail) > 0:
                        print(patent_detail)

                except Exception as e:
                    print("访问失败", e)

                if sums > numbers:
                    get_all_url(df.get_file_line(a_link_file, numbers))

    else:
        print("此公司无官方网站！")


if __name__ == '__main__':

    df = DealFile()
    get_all_url('https://www.3s-guojian.com')
