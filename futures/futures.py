#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    future
    ~~~~~~~~~~~~~~~~~~~

    future study.

    :copyright: (c) 2017 by Blurt Heart.
    :license: BSD, see LICENSE for more details.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request


URLS = [
    'http://www.baidu.com',
    'http://www.sina.com',
    'http://nba.hupu.com'
]


def fetch_url(url, timeout=10):
    return urllib.request.urlopen(url, timeout=timeout).read()


def generator():
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_dict = dict((executor.submit(fetch_url, url), url) for url in URLS)
        # future_dict will be changed to a set in as_complete
        # and it will only remain keys when dict to set
        for future in as_completed(future_dict):
            print(future.result())


if __name__ == '__main__':
    generator()