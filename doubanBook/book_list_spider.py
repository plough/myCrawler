#!/usr/bin/env python
# encoding: utf-8

# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import requests
from bs4 import BeautifulSoup

file_name = 'book_list.txt'
file_content = '' # 最终要写到文件里的内容
file_content += '生成时间：' + time.asctime()

def book_spider(book_tag):
    global file_content

    url = "http://www.douban.com/tag/%s/book" % book_tag
    source_code = requests.get(url)
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text)

    title_divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    file_content += title_divide + '\t' * 4 + \
            book_tag + '：' + title_divide
    count = 1
    # 得到书籍列表的soup对象
    list_soup = soup.find('div', {'class': 'mod book-list'})
    for book_info in list_soup.findAll('dd'):
        title = book_info.find('a', {
            'class':'title'}).string.strip()

        desc = book_info.find('div', {'class':'desc'}).string.strip()
        desc_list = desc.split('/')
        author_info = '作者/译者： ' + '/'.join(desc_list[0:-3])
        pub_info = '出版信息： ' + '/'.join(desc_list[-3:])
        rating = book_info.find('span', {
            'class':'rating_nums'}).string.strip()
        file_content += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" % (
                count, title, rating, author_info, pub_info)
        count += 1


def do_spider(book_lists):
    for book_tag in book_lists:
        book_spider(book_tag)

book_lists = ['心理学','人物传记','中国历史','旅行','生活','科普']
do_spider(book_lists)

# 将最终结果写入文件
f = open(file_name, 'w')
f.write(file_content)
f.close()
