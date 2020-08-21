#coding=utf-8
import requests
import re

def getHTMLText(url):
    f_headers = {
        'authority': 's.taobao.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'referer': 'https://www.taobao.com/?spm=a230r.1.1581860521.1.44436fbeX7fwH0',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'cna=88pKFuAt2QMCAWVY2F3T01h1; cookie2=17b6ac1692df0c736e28c4efcb5ee79a; t=447830b48ce5b736833b764b92809ff2; _tb_token_=715e9a3b15e9; v=0; thw=cn; unb=2082742785; uc3=id2=UUjZcE2LH1EDaQ%3D%3D&vt3=F8dBxdgrdaJJ5KSVCHo%3D&nk2=3RdKdRwto8z8PA%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D; csg=4e1f7957; lgc=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; cookie17=UUjZcE2LH1EDaQ%3D%3D; dnk=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; skt=ec673df4ff6e43ac; existShop=MTU3Nzk1NTE4OQ%3D%3D; uc4=nk4=0%4035zQA7TpoK2iybOgdcGoulv7b5aB&id4=0%40U2o7m3X6u2tj46bVVY%2FxUsnfO1hN; tracknick=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; _cc_=UtASsssmfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E5%A4%8F5b; _nk_=%5Cu65E7%5Cu91D1%5Cu5C71%5Cu7684%5Cu590F; cookie1=VvaIEm24hLue5D5qhr2avxolnb%2FaZNMx4VbmE815fEA%3D; enc=PrShuTMeEH7c84JZDvhxe%2BofqKPYVhiahZMb778yWEXwjAX4aS4mDthKut6ysn9Le5wPLAhqNs6w80YwVrDGZw%3D%3D; mt=ci=46_1; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie14=UoTbmhmo%2BDP65Q%3D%3D; JSESSIONID=17E0512B44E7C08C2078A64DE1792A91; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; l=dBrD7EMqqZ0JhEKsBOCwnurza77tsIRAguPzaNbMi_5aZ6LsLT7OoX_6cFp6cjWfTLTB4cPM8Rp9-etkmEy06Pt-g3fPixDc.; isg=BMjIpqdQAuYKqW2s7p0pvmNimTbacSx7WbTdyIJ5EsM2XWjHKobICwRf0XWI7eRT',
    }

    try:
        r = requests.get(url, headers=f_headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html):
    try:
        plt = re.findall(r'"view_price":"[\d.]*"', html)
        tlt = re.findall(r'"raw_title":".*?"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])  # eval去除两端的单引号
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = '手机'
    depth = 1  # 只爬取两页信息
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            print(html)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)


main()