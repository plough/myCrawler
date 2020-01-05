#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def get(url):
    i = 0
    while i < 3:
        try:
            r = requests.get(url, timeout=3)
            return r
        except requests.exceptions.RequestException:
            i += 1
