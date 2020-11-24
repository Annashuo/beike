# !/usr/bin/env python
# coding=utf-8

import re
import os
import requests
import math
import random
import time
from bs4 import BeautifulSoup
from config import *
from lib.request.web_request_header import *


def fetch_raw(target, file):
    target = target.encode("utf-8")
    print('request target web:', target)

    # 获得请求头部
    headers = create_request_headers()

    # 发起网页请求（获取总页数）
    response = requests.get(target, timeout=10, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    with open(file, "wb") as fd:
        fd.write(soup.encode("utf-8"))


begin = [[u"https://gz.ke.com/chengjiao/rs骏景花园/", "./test2.txt"]]

# ["https://gz.ke.com/xiaoqu/tianhe/y4/", "./test1.txt"],
# [u"https://gz.ke.com/chengjiao/rs骏景花园/", "./test2.txt"],
# [u"https://gz.ke.com/xiaoqu/tianhe/", "./test3.txt"]
# ["https://gz.ke.com/chengjiao/108400942598.html", "./test4.txt"]
for a in begin:
    fetch_raw(a[0], a[1])
