#!/usr/bin/env python
# encoding: utf-8
# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import wx
import MySQLdb
import ConfigParser


class BookSearch:
    def __init__(self):
        config = self.getConfig()
        # 连接数据库
        self.conn = MySQLdb.connect(host=config['host'], user=config['user'],\
            passwd=config['passwd'], charset='utf8')
        self.cur = self.conn.cursor()
        self.conn.select_db(config['database'])
        
    def getConfig(self):
        result = {}
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        result['host'] = config.get('db_info', 'host')
        result['user'] = config.get('db_info', 'user')
        result['passwd'] = config.get('db_info', 'password')
        result['database'] = config.get('db_info', 'database')
        return result

    def startGUI(self):
        app = wx.App()
        self.win = wx.Frame(None, title='图书检索v1.0', size=(1050, 600))
        self.win.Bind(wx.EVT_CLOSE,self.OnClose)
        bkg = wx.Panel(self.win)

        search_btn = wx.Button(bkg, label='搜索')
        search_btn.Bind(wx.EVT_BUTTON, self.startSearch)

        title_lable = wx.StaticText(bkg, -1, '书名：')
        self.title_field = wx.TextCtrl(bkg)

        # 显示结果的区域
        self.results = wx.TextCtrl(bkg, style=wx.TE_MULTILINE)
        self.results.SetEditable(False)

        hbox = wx.BoxSizer()
        hbox.Add(title_lable, proportion=0, flag=wx.EXPAND)
        hbox.Add(self.title_field, proportion=1, flag=wx.EXPAND)
        hbox.Add(search_btn, proportion=0, flag=wx.LEFT, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(self.results, proportion=1,
                flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        bkg.SetSizer(vbox)
        self.win.Show()
        app.MainLoop()

    def startSearch(self, event):
        if not self.isValid():  # 保证输入框存在有效值
            return
        result_content = ''
        sql = "SELECT id, rating, title, description FROM program_book WHERE title LIKE '%"\
            + self.title + "%' ORDER BY rating DESC;"
        try:
            # Execute the SQL command
            self.cur.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cur.fetchall()
            index = 1
            for row in results:
                bookid = row[0]
                rating = row[1]
                title = row[2]
                description = row[3]
                # Now print fetched result
             #  print "bookid=%s,rating=%s,title=%s,desc=%s" % \
             #      (bookid, rating, title, description)
                result_content += "%d\t\t\t%s分    《%s》     %s\n" % \
                    (index, rating, title, description)
                index += 1
        except Exception as e:
            print e
            print "Error: unable to fecth data"

        self.showResult(result_content)

    # 输入框有效性验证
    def isValid(self):
        self.title = self.title_field.GetValue().strip()
        if self.title == '':
            # 报错
            return False
        return True

    # 将最终结果显示在界面上
    def showResult(self, result_content):
        content = '序号\t\t\t评分\t\t书名\t\t描述\n\n\n'
        content += result_content
        self.results.SetValue(content)

    def OnClose(self, evt):
        self.conn.close()
        print 'close ok!!!'
        evt.Skip()


rec = BookSearch()
rec.startGUI()
