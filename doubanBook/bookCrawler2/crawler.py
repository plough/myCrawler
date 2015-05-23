#encoding: utf-8
# 使用BeautifulSoup模块，爬取豆瓣的图书信息。先爬标签，再爬每个标签下的书籍信息。

# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup

class BookCrawler:
    def __init__(self):
        self.f_tag_list = 'tagList.txt'
        self.f_books = 'books.txt'
        self.f_content = ''
        self.tag_list = []

    def doCrawling(self):
        self.initTags() # 将所有的标签名存储到tag_list列表中
        self.getInfoWithTag('小说',100)

    def initTags(self):
        url = 'http://book.douban.com/tag/?view=cloud'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        i = 0
        tags_soup = soup.find('div', {'class' : 'indent tag_cloud'})
        for tag in tags_soup.findAll('a'):
            i += 1
            tag_name = tag.string.strip()
            self.tag_list.append(tag_name)

    '''获取某个标签下的书籍信息。参数tag为标签名，参数max_num为爬取的书籍数量。'''
    def getInfoWithTag(self,tag,max_num = 5000):
        index = 0
        step = 15 # 每一跳的尺度（因为每页显示15本书）
        i = 1
        while index <= max_num:
            url = 'http://www.douban.com/tag/%s/book?start=%d' % (tag, index)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
            # 得到soup对象
            books_group = soup.find('div', {'class': 'mod book-list'})
            index += step
            print index

            # 提取数据
            for book_info in books_group.findAll('dd'):
                # desc和rating可能为空，此时应该忽略
                desc_raw = book_info.find('div', {'class': 'desc'})
                rating_raw = book_info.find('span', {'class': 'rating_nums'})
                if desc_raw == None or rating_raw == None:
                    continue
                title_raw = book_info.find('a')
                title = title_raw.string.strip()
                book_id = title_raw['href'].strip().split('/')[-2] # 豆瓣上的书籍ID编号
                print book_id
                desc = desc_raw.string.split('/')
                author = desc[0].strip()
                publisher = desc[-3].strip()
                date = desc[-2].strip()
                rating = float(rating_raw.string.strip())
                self.f_content += "%d-- rating: %.1f--《%s》，%s，%s，%s\n" % (i, rating, title, author,\
                        publisher, date)
                i += 1

        f = open(self.f_books, 'w')
        f.write(self.f_content)
        f.close()


crawler = BookCrawler()
crawler.doCrawling()
