# -*- coding: utf-8 -*-
# @Time     : 9/20/18 3:42 PM
# @Author   : cgy
# @Email    : at_cgy@qq.com
# @File     : _1_mafengwo.py

"""
下载马蜂窝热门地区游记
1. 找到目的地页http://www.mafengwo.cn/mdd/
2. 获取热门城市\地区 /travel-scenic-spot/mafengwo/10035.html"
3. 获取该城市游记 (社区-游记)

---
其它
1. 国内-省-目的地 可以获取该地区所有城市
2. 城市-景点 可以获取该城市所有景点
3. 城市-社区-游记 可以获取该城市所有游记

--
BloomFilter
"""

import os
import requests
import re
from pybloomfilter import BloomFilter


dir_name = 'notes/'
bf = BloomFilter(1024 * 1024 * 16, 0.01)


def find_all_city_pages_url():
    req = requests.get('http://www.mafengwo.cn/mdd/')
    city_pages = re.findall('/travel-scenic-spot/mafengwo/\d{5}.html', req.text)
    return city_pages


def get_city_number(url):
    return url[29:34]


def save_html(file_name, html):
    with open(file_name, 'wb+') as f:
        f.write(html.encode())
        f.close()


def download_city_notes(city_number):
    i = 0
    while True:
        i += 1
        url = 'http://www.mafengwo.cn/yj/%s/1-0-%d.html' % (city_number, i)
        if str.encode(url) in bf:
            continue

        if not bf.add(url.encode()):
            req = requests.get(url)
            city_notes = re.findall('href="/i/\d{7}.html"', req.text)

            # 当没有找到时退出
            if len(city_notes) == 0:
                return

            for city_note in city_notes:
                try:
                    city_url = 'http://www.mafengwo.cn%s' % (city_note[6:-1])
                    if str.encode(city_url) in bf:
                        continue
                    print("city_url = ", city_url)
                    if not bf.add(city_url.encode()):
                        req = requests.get(city_url)
                        save_html(dir_name + city_number + '_' + city_note[7:-1].replace('/', '_'), req.text)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    city_page_urls = find_all_city_pages_url()
    for city in city_page_urls:
        city_number = get_city_number(city)
        download_city_notes(city_number)

