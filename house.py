# !/usr/bin/env python
# coding=utf-8

from lib.request.web_house import *

def test(name, fetch, ptype):
    print(name)
    spider = web_house("gz", name, name)
    if fetch:
        spider.get_price_info()
        spider.store_into_db()
    spider.price_by_month(2020, ptype)

if __name__ == "__main__":
    test("中海康城", False, 0)
    # test("富力天禧花园", False, 0)
    # test("骏景花园", False, 3)
    # test("阳光假日园", False, 0)
    # test("美林湖畔花园", False, 3)
    # test("富力天朗明居", False, 2)

