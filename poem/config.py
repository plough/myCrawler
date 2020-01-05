#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户配置
"""
# 配置要爬取的关键词，可以配置为诗人名字，或诗集名称。爬取内容与百度汉语网页上搜出来的结果一致。
KEYS = ['戴望舒']
# KEYS = ['现代诗']
OUTPUT_DIR = './output'

"""
程序配置，一般不用改
"""
HOST = 'https://hanyu.baidu.com'
THREAD_POOL_SIZE = 8
THREAD_NUM = 8
# 生成的结果文件中，只包含一条条的json对象，最外层不用中括号包裹，数据之间也没有逗号。
ONLY_ROWS = False
