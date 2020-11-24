# !/usr/bin/env python
# coding=utf-8

from lib.request.web_house import *

if __name__ == "__main__":
    spider = web_house()
    spider.get_price_info("gz", "富力天禧花园")
    spider.store_price_info("fulitianxi")
