# !/usr/bin/env python
# coding=utf-8

from lib.request.web_xiaoqu import *

if __name__ == "__main__" :
    spider = web_xiaoqu("gz", "tianhe")
    spider.get_price_info()
    spider.store_into_db()
