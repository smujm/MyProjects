# Scrapy框架

### scrapy框架简介

- Scrapy是用纯Python实现一个为了爬取网站数据、提取结构性数据而编写的应用框架，用途非常广泛
- 框架的力量，用户只需要定制开发几个模块就可以轻松的实现一个爬虫，用来抓取网页内容以及各种图片，非常之方便
- scrapy架构图

## scrapy架构图

![图片描述](https://segmentfault.com/img/bVco7P)

#### 新建scrapy项目

1、创建爬虫项目，命令：scrapy startproject 项目名称
2、创建爬虫文件，命令：scrapy genspider 文件名称 域名

**文件的功能：**

- scrapy.cfg：配置文件
- spiders：存放你Spider文件，也就是你爬取的py文件
- items.py：相当于一个容器，和字典较像
- middlewares.py：定义Downloader Middlewares(下载器中间件)和Spider Middlewares(蜘蛛中间件)的实现
- pipelines.py:定义Item Pipeline的实现，实现数据的清洗，储存，验证。
- settings.py：全局配置

### 实战：斗鱼图片获取

### 运行

命令行：

```python
scrapy crawl xxx(项目的名字)
```

### requests和scrapy框架比较

#### 相同点：

- 两者都可以用进行页面请求和爬取，Python爬虫的两个重要技术路线。
- 两者可用性都好，文档丰富，入门简单。
- 两者都没有处理js,提交表单，应对验证码等功能。

#### 对比：

![1597748358838](Scrapy框架.assets/1597748358838.png)

