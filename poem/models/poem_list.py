#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.poem import Poem
from models.author import Author
import requests
import json
import math
import time
import random
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import threading
import collections
import os

import sys
sys.path.append('..')
from config import HOST, THREAD_NUM, THREAD_POOL_SIZE, OUTPUT_DIR

thread_pool = ThreadPoolExecutor(THREAD_POOL_SIZE)


class PoemList:
    def __init__(self, search_key):
        self.search_key = search_key
        self.poem_list = []
        self.author = None  # TODO: 以后再考虑author字段
        self.output_file = os.path.join(OUTPUT_DIR, search_key + '.json')
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

    def __str__(self):
        res = 'key: {}\n'.format(self.search_key)
        counter = 0
        for poem in self.poem_list:
            counter += 1
            res += '({}) {}\n'.format(counter, poem)
        return res

    def download_and_save(self):
        self._fetch_author_and_poems()

    def to_map(self):
        poems = []
        for poem in self.poem_list:
            poems.append(poem.__dict__)

        res = collections.OrderedDict()
        res['search_key'] = self.search_key
        if self.author is not None:
            res['author'] = self.author.__dict__
        res['poem'] = poems

        return res

    def _fetch_author_and_poems(self):
        start_url = '{}/hanyu/ajax/search_list?wd={}'.format(
            HOST, self.search_key)
        print('view page:', 0)
        res = requests.get(start_url)
        if res.status_code == 200:
            r = json.loads(res.text)
            self._before_collect_poems()
            self._collect_poems(r)
            total_page = self._get_total_page(r)
            for i in range(1, total_page):
                print('view page:', i)
                page_url = '{}&pn={}'.format(start_url, i+1)
                res = requests.get(page_url)
                if res.status_code == 200:
                    r = json.loads(res.text)
                    self._collect_poems(r, i == total_page-1)
            self._after_collect_poems()

    def _get_total_page(self, r):
        if r['ret_type'] == 'author':
            return int(r['ret_array'][0]['poems']['extra']['total-page'])
        return int(r['extra']['total-page'])

    def _init_author(self, r):
        if self.author is not None:
            return

        author_info = r['ret_array'][0]['author']
        author = Author(
            author_info['name'][0],
            author_info['basic_piclink'][0],
            author_info['basic_description'][0],
            author_info['basic_source_url'][0],
        )

        self.author = author

    def _before_collect_poems(self):
        with open(self.output_file, 'w') as f:
            f.write('[')

    def _after_collect_poems(self):
        with open(self.output_file, 'a') as f:
            f.write('\n]')

    def _collect_poems(self, r, last_page=False):
        """
        r = json.loads(res)
        """
        if r['ret_type'] == 'author':
            self._init_author(r)
            poems = r['ret_array'][0]['poems']['ret_array']
        else:
            poems = r['ret_array']

        # json_poems = r['ret_array'][0]['poems']
        for poem in poems:
            title = poem['display_name'][0]
            author_name = poem['literature_author'][0]
            dynasty = poem['dynasty'][0]
            sid = poem['sid'][0]
            self._add_poem(title, author_name, dynasty, sid)

        self._fetch_poem_bodys()
        self._flush_to_file(last_page)

    def _flush_to_file(self, last_page):
        with open(self.output_file, 'a') as f:
            while len(self.poem_list) > 0:
                poem = self.poem_list.pop()
                f.write(json.dumps(poem.__dict__, indent=2))
                if (not last_page) or len(self.poem_list) > 0:
                    f.write(',')

    def _add_poem(self, title, author_name, dynasty, poem_sid):
        poem_url = '{}/shici/detail?pid={}'.format(HOST, poem_sid)
        poem = Poem(title, author_name, dynasty, poem_url)
        self.poem_list.append(poem)

    def _fetch_poem_bodys(self):
        total = len(self.poem_list)
        print('total:', total)
        step = math.ceil(total / THREAD_NUM)
        all_task = []
        for start in range(0, total, step):
            all_task.append(thread_pool.submit(
                self._fetch_poem_bodys_by_range, start, start+step))
            # self._fetch_poem_bodys_by_range(start, start+step)
        wait(all_task, return_when=ALL_COMPLETED)

    def _fetch_poem_bodys_by_range(self, start_index, end_index):
        for poem in self.poem_list[start_index: end_index]:
            # time.sleep(random.choice([0.5, 1, 1.5]))
            print(threading.current_thread().name,
                  '> fetching', poem.get_title())
            poem.fetch()
