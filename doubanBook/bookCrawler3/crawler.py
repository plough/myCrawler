#encoding: utf-8
# 使用requests和BeautifulSoup模块，爬取豆瓣的图书信息。先爬标签，再爬每个标签下的书籍信息。
# 用子线程来爬取图片信息和书籍详情

# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup
import MySQLdb
import time
import os

class BookCrawler:
    def __init__(self):
        self.tag = '编程'
        self.f_books = 'books.txt'
        self.f_content = ''
        # 伪装成浏览器，防止403错误
        self.headers = [
                {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
                {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
                {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
                {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
                {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
                ]
        self.sessions = []
        for header in self.headers:
            s = requests.Session()
            s.headers.update(header)
            self.sessions.append(s)

        # 标签下的图书列表。用于一次性插入数据库。
        self.book_list = []

        # 连接数据库
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='345881709', charset='utf8')
        self.cur = self.conn.cursor()
        self.conn.select_db('douban_book')

    def doCrawling(self):
        try:
            self.getInfoWithTag(self.tag,14)
        except Exception as e:
            print "出错：%s" % (e)
            exit(-1)
        finally:
            # 书籍处理完后提交一次
            self.conn.commit()
            # 收尾工作，关闭数据库连接
            self.cur.close()
            self.conn.close()

    '''获取某个标签下的书籍信息。参数tag为标签名，参数max_num为爬取的书籍数量。'''
    def getInfoWithTag(self,tag,max_num = 5000):
        index = 0
        step = 15 # 每一跳的尺度（因为每页显示15本书）
        while index <= max_num:
            time.sleep(5)
            url = 'http://www.douban.com/tag/%s/book?start=%d' % (tag, index)
            try:
                source_code = self.sessions[0].get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, 'lxml')
                # 得到soup对象
                books_group = soup.find('div', {'class': 'mod book-list'})
                index += step
                #print tag, index

                # 如果已经没有书籍，爬取结束
                book_info_list = books_group.findAll('dl')
                if len(book_info_list) == 0:
                    break

                print 'len(book_info_list) =', len(book_info_list)
                # 提取数据
                for book_info in book_info_list:
                    print 'book_info=%s' % book_info
                    book_table = {}

                    # 处理图片
                    image_url = book_info.dt.a.img.get('src').strip()
                    image_name = image_url.split('/')[-1]
                    book_table['image_name'] = image_name
                    #book_table['image_url'] = image_url
                    self.saveImage(image_url, image_name)

                    desc_raw = book_info.find('div', {'class': 'desc'})
                    if desc_raw != None:
                        desc = desc_raw.string.strip()
                        book_table['description'] = desc

                    title_raw = book_info.find('a', {'class': 'title'})
                    title = title_raw.string.strip()
                    book_table['title'] = title
                    book_url = title_raw.get('href')

                    # 在书籍详情页面爬取图书剩余信息，并整合
                    book_table_expand = self.crawlDetailInfo(book_url)
                    book_table.update(book_table_expand.items())

                    # 将一本书的信息暂存到book_list中
                    self.book_list.append(book_table)
                    print 'processed %s' % book_table['title']
            except requests.exceptions.ConnectionError:
                time.sleep(30)
            except Exception as e:
                #time.sleep(30)
                print type(e),e
                time.sleep(1)
#           # 15本书籍处理完之后，执行一次批量插入操作
#           sql = "INSERT INTO Books (BookID, Tag, Title, Author, Publisher, Rating, Date)\
#                   VALUES (%s, %s, %s, %s, %s, %s, %s)"

#           self.cur.executemany(sql, self.book_list)
            # 清空book_list
            #print self.book_list
            print 'start writing...'
            theindex = 1
            for book_info in self.book_list:
                self.f_content += '%s -------------------\n' % theindex
                for key in book_info:
                    self.f_content += '%s : %s\n' % (key, book_info[key])
                self.f_content += '\n'
                theindex += 1
            with open('books.txt', 'w') as f:
                f.write(self.f_content)
            self.book_list = []

    # 保存网络图片
    def saveImage(self, image_url, image_name ="default.jpg"):
        response = self.sessions[1].get(image_url, stream=True)
        image = response.content
        dist_dir = 'pics'
        try:
            with open(os.path.join(dist_dir, image_name),'wb') as jpg:
                jpg.write(image)
        except IOError as e:
            print("IO Error: %s" % e)

    def crawlDetailInfo(self, book_url):
        book_table = {}
        plain_text = self.sessions[1].get(book_url, timeout=10).content
        soup = BeautifulSoup(plain_text, 'lxml')

        # 评分和评价人数
        rating_soup = soup.find('div', {'class': 'rating_wrap'})
        rating_raw = rating_soup.find('strong')
        votes_raw = rating_soup.find('span', {'property': 'v:votes'})
        if rating_raw != None:
            book_table['rating'] = float(rating_raw.string.strip())
        if votes_raw != None:
            book_table['votes'] = int(votes_raw.string.strip())

        # 内容简介
        intro_soups = soup.findAll('div', {'class': 'intro'})
        if len(intro_soups) > 0:
            intro = '\t'
            intro_index = 0
            while intro == '\t' or intro.endswith('(展开全部)'):
                intro = '\t'
                paragraphs = []
                intro_soup = intro_soups[intro_index]
                for p in intro_soup.findAll('p'):
                    if p.string != None:
                        paragraphs.append(p.string.strip())
                intro += '\n\t'.join(paragraphs)
                intro_index += 1
            book_table['introduction'] = intro

        # 书籍其他信息
        info_soup = soup.find('div', {'id': 'info'})
        info_list = info_soup.findAll('span', {'class': 'pl'})
        for info in info_list:
            info_s = info.string.strip()
            if info_s.startswith('作者'):
                author_list = []
                authors_raw = info.parent.findAll('a')
                for author_raw in authors_raw:
                    author_list.append(author_raw.string.strip())
                book_table['author'] = ','.join(author_list)
                continue
            if info_s.startswith('译者'):
                trans_list = []
                trans_raw = info.parent.findAll('a')
                for trans in trans_raw:
                    trans_list.append(trans.string.strip())
                book_table['translator'] = ','.join(trans_list)
                continue
            if info_s.startswith('出版社'):
                book_table['publisher'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('副标题'):
                book_table['subtitle'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('原作名'):
                book_table['origin'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('出版年'):
                date_l = info.next_sibling.string.strip().split('-')
                # 保证日期由“年-月-日”组成，不够用0补足
                while len(date_l) < 3:
                    date_l.append('0')
                book_table['publish_date'] = '-'.join(date_l)
                continue
            if info_s.startswith('页数'):
                book_table['page_number'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('定价'):
                book_table['price'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('装帧'):
                book_table['binding_type'] = info.next_sibling.string.strip()
                continue
            if info_s.startswith('丛书'):
                book_table['series'] = info.parent.findAll('a')[-1].string.strip()
                continue
            if info_s.startswith('ISBN'):
                book_table['ISBN'] = info.next_sibling.string.strip()
        return book_table


if __name__ == '__main__':

    crawler = BookCrawler()
    crawler.doCrawling()
    #crawler.saveImage('http://img3.douban.com/lpic/s11314802.jpg', 's11314802.jpg')
    #url = 'http://book.douban.com/subject/11541213/?from=tag_all'
    #url = 'http://book.douban.com/subject/10546125/?from=tag_all'
#   url = 'http://book.douban.com/subject/1230413/?from=tag_all'
#   book_table = crawler.crawlDetailInfo(url)
#   print book_table['introduction']
#   for key in book_table:
#       print "%s: %s" % (key, book_table[key])
