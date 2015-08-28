#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup

def getInfo(url):
    proxy_info = []
    page_code = requests.get(url).text
    soup = BeautifulSoup(page_code)
    table_soup = soup.find('table')
    proxy_list = table_soup.findAll('tr')[1:]
    for tr in proxy_list:
        td_list = tr.findAll('td')
        ip = td_list[2].string
        port = td_list[3].string
        location = td_list[4].string
        anonymity = td_list[5].string
        proxy_type = td_list[6].string
        speed = td_list[7].find('div', {'class': 'bar'})['title']
        connect_time = td_list[8].find('div', {'class': 'bar'})['title']
        validate_time = td_list[9].string

        # strip
        l = [ip, port, location, anonymity, proxy_type, speed, connect_time, validate_time]
        for i in range( len(l) ):
            if l[i]:
                l[i] = l[i].strip()
        proxy_info.append(l)

    return proxy_info

if __name__ == '__main__':
    url = 'http://www.xici.net.co/nn/1'
    proxy_info = getInfo(url)
    for row in proxy_info:
        for s in row:
            print s,
        print
