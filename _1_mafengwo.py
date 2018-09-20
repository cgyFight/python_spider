# -*- coding: utf-8 -*-
# @Time     : 9/20/18 3:42 PM
# @Author   : cgy
# @Email    : at_cgy@qq.com
# @File     : _1_mafengwo.py

"""
下载马蜂窝所有游记
"""

import os
import requests
import re


dir_name = 'notes/'


def start():
    return


def find_all_city_pages():
    req = requests.get('http://www.mafengwo.cn/mdd/')
    city_pages = re.findall('/travel-scenic-spot/mafengwo/\d{5}.html', req.text)
    for city in city_pages:
        print(city)
    print(req.text)


if __name__ == '__main__':
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    find_all_city_pages()
