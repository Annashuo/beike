# !/usr/bin/env python
# coding=utf-8

from lib.request.web_house import *

def test(name, fetch):
    print(name)
    spider = web_house("gz", name, name)
    if fetch:
        spider.get_price_info()
        spider.store_into_db()
    spider.price_by_month(2020)

if __name__ == "__main__":
    test("中海康城", False)
    test("富力天禧花园", False)
    test("骏景花园", False)

