# !/usr/bin/env python
# coding=utf-8

from lib.request.web_house import *

if __name__ == "__main__":
    spider = web_house("gz", "富力天禧花园", "富力天禧花园")
    spider.get_price_info()
    spider.store_into_db()
