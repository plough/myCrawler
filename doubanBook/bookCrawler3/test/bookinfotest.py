#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup

def main():
    #url = 'http://book.douban.com/subject/11541213/'
    text = """
<div id="info" class="">
    <span>
      <span class="pl"> 作者</span>:
        <a class="" href="/search/%E5%AE%89%E5%BE%B7%E9%B2%81%C2%B7%E9%9C%8D%E5%A5%87%E6%96%AF">（英）安德鲁·霍奇斯</a>
    </span><br/>
    <span class="pl">出版社:</span> 湖南科学技术出版社<br/>
    <span class="pl">副标题:</span> 如谜的解谜者<br/>
    <span class="pl">原作名:</span> Alan Turing: The Enigma<br/>
    <span>
      <span class="pl"> 译者</span>:
        <a class="" href="/search/%E5%AD%99%E5%A4%A9%E9%BD%90">孙天齐</a>
    </span><br/>
    <span class="pl">出版年:</span> 2012-8-1<br/>
    <span class="pl">页数:</span> 534<br/>
    <span class="pl">定价:</span> 68.00元<br/>
    <span class="pl">装帧:</span> 平装<br/>
      <span class="pl">ISBN:</span> 9787535773067<br/>
</div>
    """
    #plain_text = requests.get(url).text
    soup = BeautifulSoup(text, 'lxml')
    info_soup = soup.find('div', {'id': 'info'})
    print info_soup

main()
