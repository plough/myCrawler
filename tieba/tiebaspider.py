#!/usr/bin/env python
# encoding: utf-8
"""
爬取百度贴吧帖子，20页。
涉及技术：
    1. xpath解析网页数据
    2. json库的基本使用
    3. 使用map函数实现并行化
"""

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def toWrite(content_dict):
    f.writelines('回帖时间：' + str(content_dict['topic_reply_time']) + '\n')
    f.writelines('回帖内容：' + str(content_dict['topic_reply_content']) + '\n')
    f.writelines('回帖时间：' + str(content_dict['user_name']) + '\n\n')


def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.content)
    content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    item = {}
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot', ''))
        author = reply_info['author']['user_name']
        content = each.xpath('.//cc/div/text()')[0].strip()
        reply_time = reply_info['content']['date']
        print author
        print content
        print reply_time
        item['user_name'] = author
        item['topic_reply_content'] = content
        item['topic_reply_time'] = reply_time
        toWrite(item)


if __name__ == "__main__":
    pool = ThreadPool(4)
    f = open('content.txt', 'w')
    page = []
    for i in range(1, 21):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)

    results = pool.map(spider, page)
    pool.close()
    pool.join()
    f.close()
