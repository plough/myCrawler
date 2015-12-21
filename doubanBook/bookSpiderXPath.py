#!/usr/bin/env python
# encoding: utf-8
import time
import requests
import random
from lxml import etree
# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]


def main():
    tags = ['哲学', '计算机', '心理学', '生活', '数学']

    fileContent = ''  # 最终要写到文件里的内容
    fileContent += '生成时间：' + time.asctime()

    for tag in tags:
        fileContent += bookSpider(tag)
        print "%s down!" % tag

    with open('book_list.txt', 'w') as f:
        f.write(fileContent)


def bookSpider(bookTag):
    result = ''
    divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    result += divide + '\t' * 4 + bookTag + '：' + divide

    url = "http://www.douban.com/tag/%s/book" % bookTag
    global headers
    html = requests.get(url, headers=random.choice(headers)).content
    #  print html
    tree = etree.HTML(html.decode('utf-8'))
    books = tree.xpath("//dl/dd")

    count = 1
    for book in books:
        # 得到书名
        title = book.xpath("a/text()")[0].strip()
        # 得到出版信息
        desc = book.xpath("div[@class='desc']/text()")[0].strip()
        descL = desc.split('/')
        authorInfo = '作者/译者： ' + '/'.join(descL[:-3])
        pubInfo = '出版信息： ' + '/'.join(descL[-3:])
        # 得到评分
        rating = book.xpath("div/span[@class='rating_nums']/text()")[0].strip()
        # 加入结果字符串
        result += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" \
            % (count, title, rating, authorInfo, pubInfo)

        count += 1

    return result


if __name__ == "__main__":
    main()
    #  bookSpider('哲学')
