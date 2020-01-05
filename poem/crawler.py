#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models import PoemList
import time
from config import KEYS


def crawl(keys):
    time_start = time.time()

    for key in keys:
        poem_list = PoemList(key)
        poem_list.download_and_save()

    time_end = time.time()
    print('totally cost {:.2f}s'.format(time_end - time_start))


if __name__ == "__main__":
    crawl(KEYS)
