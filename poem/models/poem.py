#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup


class Poem:
    SIMPLE_DESC_LENGTH = 20

    def __init__(self, title, author_name, dynasty, url, body=''):
        self.title = title
        self.author_name = author_name
        self.dynasty = dynasty
        self.url = url
        self.body = body

    def __str__(self):
        return '{}/({}) {}'.format(
            self.name,
            self.dynasty,
            self.url if len(self.body) == 0 else self.get_simple_desc_body())

    def get_title(self):
        return self.title

    def fetch(self):
        assert len(self.url) > 0
        res = requests.get(self.url)
        if res.status_code == 200:
            txt = re.sub(r'</*br/*>', '\n', res.text)
            txt = re.sub(r'<span.*?modern-line-span.*?>', '\n', txt)
            soup = BeautifulSoup(txt, 'lxml')
            try:
                target = soup.find('div', 'poem-detail-main-text')
                if target is None:
                    target = soup.find('div', 'poem-detail-item-content')
                self.body = target.text
            except Exception as e:
                print(e)
                print('soup:', soup)

    def get_simple_desc_body(self):
        if len(self.body) <= Poem.SIMPLE_DESC_LENGTH:
            return self.body
        return self.body[0: Poem.SIMPLE_DESC_LENGTH] + '...'
