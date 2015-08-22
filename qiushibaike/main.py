#!/usr/bin/ python
# encoding: utf-8

import urllib2
import requests
import re

#糗事百科爬虫类
class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        pageCode = requests.get(url, headers = self.headers).text
        return pageCode

    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败..."
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?class' +
            '="content".*?>(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                #item[0]是一个段子的发布者，item[1]是内容（加时间），item[3]是点赞数
                pageStories.append([item[0].strip(), item[1].strip().replace('<br/>', '\n'), item[3].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        #遍历一页的段子
        for story in pageStories:
            input = raw_input("('q' to exit) > ")
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input in ['Q', 'q']:
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞：%s\n\n%s\n" % (page, story[0], story[2], story[1])

    def start(self):
        print "正在读取糗事百科，按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #线加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
