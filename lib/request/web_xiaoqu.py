# !/usr/bin/env python
# coding=utf-8
# author: sunshinebooming@gmail.com

import re
import os
import requests
import math
import random
import time
from bs4 import BeautifulSoup
from config import *

from lib.utils.local_time import *
from lib.utils.file_storage import *
from lib.request.web_request_header import *


class web_xiaoqu():
    def __init__(self):
        pass

    def format_price_info(self, name, year, price, deal):
        return "{0}, {1}, {2}, {3}\n".format(name, year, price, deal)

    def get_page_price_info(self, target_sub_web, headers):
        if True == RANDOM_DELAY:
            # 随机延时（0-15）秒
            random_delay = random.randint(0, DELAY_MAX + 1)
            print('random delay: %s S...' % (random_delay))
            time.sleep(random_delay)

        response = requests.get(target_sub_web, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')

        # with open("test1.txt", "r") as f:
        #     contents = f.read()
        # soup = BeautifulSoup(contents, 'lxml')

        # 获取房价相关内容
        house_contents = soup.find_all("li", class_="clear xiaoquListItem CLICKDATA")
        for house_content in house_contents:
            # 获取小区名
            xiaoqu_name = house_content.find("div", class_="title")
            # 获取成交量
            xiaoqu_dealnum = house_content.find("div", class_="houseInfo")
            # 获取小区年份
            xiaoqu_year = house_content.find("div", class_="positionInfo")
            # 获取小区单价
            xiaoqu_price = house_content.find("div", class_="totalPrice")

            # 整理小区名称数据
            name = xiaoqu_name.text.strip().encode("utf-8")

            # 整理成交量数据
            try:
                deal = re.findall(r'\d+', xiaoqu_dealnum.find("a").text.encode("utf-8"))[1].encode("utf-8")
            except Exception as e:
                deal = "0"

            # 整理单价数据
            try:
                price = re.findall(r'\d+', xiaoqu_price.text)[0].encode("utf-8")
            except Exception as e:
                price = "0"

            # 整理年份
            try:
                year = re.findall(r'\d+', xiaoqu_year.text[xiaoqu_year.text.find("/"):])[0].encode("utf-8")
            except Exception as e:
                year = "0"

            # 打印单条房价信息
            print("\t===> name: %s, year: %s 年, price: %s 元/平米, deal: %s" % (
                name, year, price, deal))

            # 格式化单条房价信息，并添加到list中
            price_fmt_str = self.format_price_info(name, year, price, deal)
            self.price_info_list.append(price_fmt_str)


    def get_price_info(self, city_name, district):
        self.city_name = city_name
        self.district = district
        self.price_info_list = list()

        target_web = 'http://{0}.ke.com/xiaoqu/{1}/y4/'.format(city_name, district)
        print('request target web:', target_web)

        # 获得请求头部
        headers = create_request_headers()

        # 发起网页请求（获取总页数）
        response = requests.get(target_web, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')

        # 获得response总页数
        try:
            page_box = soup.find_all('div', class_='page-box house-lst-page-box')[0]
            tmp1 = str(page_box).find("totalPage")
            tmp2 = str(page_box).find("curPage")
            total_page = int(re.findall(r'\d+', str(page_box)[tmp1: tmp2])[0])
        except Exception as e:
            print("warning: only find one page for {0}".format(city_name))
            print(e)
            total_page

        print('total pages:', total_page)
        headers = create_request_headers()
        # 遍历房价网页
        for i in range(1, total_page + 1) :
        # for i in range(1, total_page):
            target_sub_web = target_web + "pg{0}".format(i)
            print('request target web:', target_sub_web)

            # 发起网页请求
            self.get_page_price_info(target_sub_web, headers)



    def store_price_info(self):
        # 创建数据存储目录
        root_path = get_root_path()
        store_dir_path = root_path + "/data/original_data/{0}".format(self.city_name)
        is_dir_exit = os.path.exists(store_dir_path)
        if not is_dir_exit:
            os.makedirs(store_dir_path)

        # 存储格式化的房价数据到相应日期的文件中
        store_path = store_dir_path + "/{0}_{1}.csv".format(self.city_name, self.district)
        with open(store_path, "w") as fd:
            fd.write("data, year, price, deal\n")
            for price in self.price_info_list:
                fd.write(price)


if __name__ == "__main__":
    pass
