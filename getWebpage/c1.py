#!/usr/bin/env python
# encoding: utf-8
import urllib
import urllib.request

data = {}
data['word'] = 'Jecvay Notes'

url_values = urllib.parse.urlencode(data)
url = "http://www.baidu.com/s?"
full_url = url + url_values

data = urllib.request.urlopen(full_url).read()
data = data.decode('UTF-8')

with open("test.html", "w") as html_file:
    html_file.write(data)
print("保存页面成功！")
