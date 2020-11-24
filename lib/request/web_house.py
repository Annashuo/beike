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


class web_house():
    def __init__(self):
        pass

    def format_price_info(self, house_number, house_type, house_layer, house_area, house_direction,
        house_elevator, house_time, deal_date, duration, begin_price, end_price, by_price):
        return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}\n".\
            format(house_number, house_type, house_layer, house_area, house_direction,
            house_elevator, house_time, deal_date, duration, begin_price, end_price, by_price)

    def get_raw_price_info(self, houseid, deal_date, city, headers):
        if houseid in self.numbers:
            return
        if True == RANDOM_DELAY:
            # 随机延时（0-15）秒
            random_delay = random.randint(0, DELAY_MAX + 1)
            print('random delay: %s S...' % (random_delay))
            time.sleep(random_delay)

        target_web = 'http://{0}.ke.com/chengjiao/{1}.html'.format(city, houseid)
        print('request target web:', target_web)
        response = requests.get(target_web, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')

        # with open("test4.txt", "r") as f:
        #     contents = f.read()
        # soup = BeautifulSoup(contents, 'lxml')

        house_price = soup.find("div", class_="info fr")
        house_base = soup.find("div", class_="base").find("div", class_="content")
        house_transaction = soup.find("div", class_="transaction").find("div", class_="content")

        try:
            end_price = house_price.find("span", class_="dealTotalPrice").text.encode("utf-8").decode("utf-8")
            end_price = re.findall(r'\d+', end_price)[0].encode("utf-8").decode("utf-8")
            by_price = re.findall(r'\d+', house_price.find("b").text)[0].encode("utf-8").decode("utf-8")
            price_msg = house_price.find("div", class_="msg")
            spans = price_msg.find_all("span")
            begin_price = re.findall(r'\d+', spans[0].text)[0].encode("utf-8").decode("utf-8")
            duration = re.findall(r'\d+', spans[1].text)[0].encode("utf-8").decode("utf-8")
        except Exception as e:
            print(e)
            begin_price = "0"
            duration = "0"
            end_price = "0"
            by_price = "0"

        try:
            lis = house_base.find_all("li")
            for li in lis:
                li.span.decompose()
            house_type = lis[0].text.strip().encode("utf-8").decode("utf-8")
            house_layer = lis[1].text.strip().encode("utf-8").decode("utf-8")
            house_area = re.findall(r'\d+', lis[2].text.strip())[0].encode("utf-8").decode("utf-8")
            house_direction = lis[6].text.strip().encode("utf-8").decode("utf-8")
            house_elevator = lis[12].text.strip().encode("utf-8").decode("utf-8")
        except Exception as e:
            house_type = ""
            house_layer = ""
            house_area = ""
            house_direction = ""
            house_elevator = "无"

        try:
            lis = house_transaction.find_all("li")
            for li in lis:
                li.span.decompose()
            house_number = lis[0].text.strip().encode("utf-8").decode("utf-8")
            house_time = lis[2].text.strip().encode("utf-8").decode("utf-8")
        except Exception as e:
            house_number = ""
            house_time = ""

        # 打印单条房价信息
        print("\t===> 房号: %s, 户型: %s, 楼层: %s, 面积: %s 平米, 朝向: %s, "
              "电梯: %s, 放盘时间: %s, 成交时间: %s, 周期: %s, 挂牌价: %s, 成交价: %s, 单价: %s" % (
            house_number, house_type, house_layer, house_area, house_direction,
        house_elevator, house_time, deal_date, duration, begin_price, end_price, by_price))

        # 格式化单条房价信息，并添加到list中
        if int(house_number) not in self.numbers:
            self.numbers.add(int(house_number))
            price_fmt_str = self.format_price_info(house_number, house_type, house_layer, house_area, house_direction,
            house_elevator, house_time, deal_date, duration, begin_price, end_price, by_price)
            self.price_info_list.append(price_fmt_str)

    def get_page_price_info(self, target_sub_web, city, headers):
        if True == RANDOM_DELAY:
            # 随机延时（0-15）秒
            random_delay = random.randint(0, DELAY_MAX + 1)
            print('random delay: %s S...' % (random_delay))
            time.sleep(random_delay)

        print('request target web:', target_sub_web)
        response = requests.get(target_sub_web, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')

        # with open("test2.txt", "r") as f:
        #     contents = f.read()
        # soup = BeautifulSoup(contents, 'lxml')

        # 获取房价相关内容
        house_contents = soup.find("ul", class_="listContent").find_all("li", class_="VIEWDATA")
        for house_content in house_contents:
            item = str(house_content.find("a", class_="CLICKDATA maidian-detail"))
            num = int(re.findall(r'\d+', item[item.find("fb_item_id"):])[0])
            deal_date = house_content.find("div", "dealDate").text.strip().encode("utf-8").decode("utf-8")
            self.get_raw_price_info(num, deal_date, city, headers)


    def get_price_info(self, city, xiaoqu):
        # xiaoqu = xiaoqu.encode("utf-8").decode("utf-8")
        self.city = city
        self.xiaoqu = xiaoqu
        self.numbers = set()
        self.price_info_list = list()

        target_web = 'http://{0}.ke.com/chengjiao/rs{1}/'.format(city, xiaoqu)
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
            print("warning: only find one page for {0}".format(xiaoqu))
            print(e)
            total_page = 2

        print('total pages:', total_page)
        headers = create_request_headers()
        # 遍历房价网页
        for i in range(1, total_page + 1):
        # for i in range(1, total_page):
            target_sub_web = target_web + "pg{0}".format(i)
            print('request target web:', target_sub_web)

            # 发起网页请求
            self.get_page_price_info(target_sub_web, city, headers)



    def store_price_info(self, xiaoqu):
        # 创建数据存储目录
        root_path = get_root_path()
        store_dir_path = root_path + "/data/original_data/{0}".format(self.city)
        is_dir_exit = os.path.exists(store_dir_path)
        if not is_dir_exit:
            os.makedirs(store_dir_path)

        # 存储格式化的房价数据到相应日期的文件中
        store_path = store_dir_path + "/{0}.csv".format(xiaoqu)
        with open(store_path, "w") as fd:
            fd.write("房号, 户型, 楼层, 面积, 朝向, 电梯, 放盘时间, 成交时间, 周期, 挂牌价, 成交价, 单价\n")
            for price in self.price_info_list:
                fd.write(price)


if __name__ == "__main__":
    pass