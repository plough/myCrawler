#!/usr/bin/env python
# encoding: utf-8
import time
import requests
from lxml import etree
# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
    html = requests.get(url).content
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
