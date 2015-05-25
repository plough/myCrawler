#encoding: utf-8
# 使用BeautifulSoup模块，爬取豆瓣的图书信息。先爬标签，再爬每个标签下的书籍信息。

# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup
import MySQLdb
import time

class BookCrawler:
    def __init__(self):
        self.f_tag_list = 'tagList.txt'
        self.f_books = 'books.txt'
        self.f_content = ''
        # 伪装成浏览器，防止403错误
        '''self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
                'Host': 'book.douban.com', 'Connection': 'keep-alive',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'}
        '''
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
                'Connection': 'keep-alive',
                'Referer': 'http://book.douban.com/tag/?view=cloud',
                'Cookie': '	bid="kxpJWb9tjVo"; __utma=30149280.603118853.1413707596.1432436432.1432464641.30; __utmz=30149280.1432436432.29.22.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=mysql%20%E6%8F%92%E5%85%A5%E4%B8%AD%E6%96%87; viewed="25913058_5921328_1281964_1054685_4770297_19952400_1473329_1103015_1041482_4242172"; __utmv=30149280.6944; ll="118159"; ap=1; ue="345881709@qq.com"; push_noty_num=0; push_doumail_num=2; pgv_pvi=5017648128; __utmb=30149280.5.10.1432464641; __utmc=30149280'}

        self.tag_list = []
        # 每个标签下的所有图书的列表。用于一次性插入数据库。处理完每个标签后，置空。
        self.book_list = []

        # 连接数据库
        self.conn = MySQLdb.connect(host='localhost', user='plough', passwd='345881709', charset='utf8')
        self.cur = self.conn.cursor()
        self.conn.select_db('douban_book')

    def doCrawling(self):
        self.initTags() # 将所有的标签名存储到tag_list列表中
        for tag in self.tag_list:
            try:
                self.getInfoWithTag(tag,1000)
            except Exception as e:
                print "出错：%s" % (e)
                exit(-1)
            finally:
                # 每个标签下的书籍处理完后提交一次
                self.conn.commit()

        # 收尾工作，关闭数据库连接
        self.cur.close()
        self.conn.close()

    def initTags(self):
        url = 'http://book.douban.com/tag/?view=cloud'
        self.session = requests.Session()
        source_code = self.session.get(url, headers = self.headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        print soup

        #i = 0
        tags_soup = soup.find('div', {'class' : 'indent tag_cloud'})
        for tag in tags_soup.findAll('a'):
            #i += 1
            tag_name = tag.string.strip()
            self.tag_list.append(tag_name)

    '''获取某个标签下的书籍信息。参数tag为标签名，参数max_num为爬取的书籍数量。'''
    def getInfoWithTag(self,tag,max_num = 5000):
        index = 0
        step = 15 # 每一跳的尺度（因为每页显示15本书）
        while index <= max_num:
            time.sleep(5)
            url = 'http://www.douban.com/tag/%s/book?start=%d' % (tag, index)
            try:
                source_code = self.session.get(url, headers = self.headers)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text)
                # 得到soup对象
                books_group = soup.find('div', {'class': 'mod book-list'})
                index += step
                print tag, index

                # 提取数据
                for book_info in books_group.findAll('dd'):
                    # desc和rating可能为空，此时应该忽略
                    desc_raw = book_info.find('div', {'class': 'desc'})
                    rating_raw = book_info.find('span', {'class': 'rating_nums'})
                    desc = [ s.strip() for s in desc_raw.string.split('/') ]
                    if desc_raw == None or rating_raw == None or len(desc) < 4 or desc[-2].isdigit():
                        continue

                    title_raw = book_info.find('a')
                    title = title_raw.string.strip()
                    book_id = title_raw['href'].strip().split('/')[-2] # 豆瓣上的书籍ID编号
                    author = desc[0]
                    publisher = desc[-3]
                    #rating = float(rating_raw.string.strip())
                    rating = rating_raw.string.strip()
                    # 对于出版日期中，只有年、月的情况，令日的值与月份相同
                    date_raw = [l for l in desc[-2].strip().split('-')]
                    # 用于插入数据库的date（字符串，格式‘2008-8-8’）
                    date = '-'.join([date_raw[0], date_raw[1], date_raw[-1]])
                    self.book_list.append((book_id, tag, title, author, publisher, rating, date))
            # 少数数据不规则，可能导致异常，此时直接忽略
            except IndexError:
                pass
            except Exception as e:
                #time.sleep(30)
                print type(e),e
                time.sleep(120)
            # 15本书籍处理完之后，执行一次批量插入操作
            sql = "INSERT INTO Books (BookID, Tag, Title, Author, Publisher, Rating, Date)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"

            self.cur.executemany(sql, self.book_list)
            # 清空book_list，便于下一个标签使用
            self.book_list = []


crawler = BookCrawler()
crawler.doCrawling()
