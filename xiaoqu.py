# !/usr/bin/env python
# coding=utf-8

from lib.request.web_xiaoqu import *

if __name__ == "__main__" :
    spider = web_xiaoqu()
    spider.get_price_info("gz", "tianhe")
    spider.store_price_info()
