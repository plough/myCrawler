#!/usr/bin/env python
# encoding: utf-8
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getSrtpInfo():
    htmlTpl = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>%s</body></html>'
    url = 'http://jwc.seu.edu.cn/10097/list.htm'

    html = requests.get(url).content
    tree = etree.HTML(html.decode('utf-8'))
    links = [a for a in tree.xpath("//a") if a.text and a.text.startswith("课外研学讲座")]
    for link in links:
        print link.text
        print link.get('href')
        date = link.getparent().getnext().xpath("div")[0].text
        print date


if __name__ == "__main__":
    getSrtpInfo()
