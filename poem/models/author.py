#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Author:

    def __init__(self, name, pic_url, desc, more_url):
        self.name = name
        self.pic_url = pic_url
        self.desc = desc
        self.more_url = more_url

    def get_name(self):
        return self.name

    def __str__(self):
        return self.get_name()
