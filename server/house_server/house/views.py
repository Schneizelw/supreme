#coding=utf-8
from __future__ import unicode_literals

import re
import os
import sys
import json
import time
import pandas as pd
from pandas import DataFrame,Series
from pyecharts import Geo,Map
from house.models import RentHouse
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, HttpResponseRedirect

#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
#    reload(sys)
#    sys.setdefaultencoding(default_encoding)

EXPIRED = 86400
CITY_MAP = {
    "bj" : "北京",
    "sh" : "上海",
    "gz" : "广州",
    "sz" : "深圳",
    "cq" : "重庆",
    "cd" : "成都",
    "hz" : "杭州",
    "wh" : "武汉",
    "su" : "苏州",
    "xa" : "西安",
    "tj" : "天津",
    "nj" : "南京",
    "zz" : "郑州",
    "cs" : "长沙",
    "qd" : "青岛",
    "dg" : "东莞",
    "sy" : "沈阳",
    "km" : "昆明",
    "dl" : "大连",
    "xm" : "厦门",
    "hf" : "合肥",
    "fs" : "佛山",
    "fz" : "福州",
    "hrb" : "哈尔滨",
    "jn" : "济南", 
    "wz" : "温州",
    "cc" : "长春",
    "sjz": "石家庄",
    "changzhou" : "长春", 
    "nn" : "南宁",
    "gy" : "贵阳",
    "nc" : "南昌",
    "nt" : "南通", 
    "jh" : "金华", 
    "xz" : "徐州",
    "ty" : "太原", 
    "jx" : "嘉兴", 
    "yt" : "烟台", 
    "hui": "惠州", 
    "bd" : "保定", 
    "taizhou" : "台州", 
    "zs" : "中山", 
    "sx" : "绍兴", 
    "lz" : "兰州", 
    "gl" : "桂林",
    "liuzhou" : "柳州", 
    "bh" : "北海",
}


def check_cache(filename):
    """
        check cache filename 
        if cache file is valid return True else False
    """
    # cur path
    path = os.getcwd()
    # all file and dir in cur path
    listdir = os.listdir(path + "/cache")
    # check if have cache file
    if filename in listdir:
        update_time = os.path.getmtime(path + "/cache/" + filename)
        now = time.time()
        # if cache file last update time less than EXPIRED
        if now - update_time < EXPIRED:
            return True
    return False

def get_cache(filename):
    """
        open cache file ,load it
    """
    fd = open("./cache/" + filename, 'r')
    tmp = fd.read()
    data = json.loads(tmp)
    return data

def query_rent_count(filename):
    """
        query mongo to calculate the number of houses in each city
        return {"city" : num}
    """
    data = {}
    res = RentHouse.objects.only('city')
    for item in res:
        city = item.city
        if city in data.keys():
            data[city] += 1
        else:
            data[city] = 1
    fd = open('./cache/' + filename, "w")
    fd.write(json.dumps(data))
    return data

def clean_price(price):
    # 有些房价的加个是一个区间 例如 4500-5000 那么去中间值
    if isinstance(price, str):
        tmp = price.split("-")
        res = (int(tmp[0]) + int(tmp[1]))/2
    else:
        res = int(price)
    # 大于一百万的数据扔掉
    if res > 1000000:
        return -1
    return res
    
def query_rent_avgprice(filename):
    """
        query mongo calculate the avg price of each city
        return { city : price }
    """
    # { city : [price1,price2...]}
    rent_avgprice = {}
    res = RentHouse.objects.only('city', 'price')
    for item in res:
        city = item.city
        price = clean_price(item.price)
        if price == -1:
            continue
        if city in rent_avgprice.keys():
            rent_avgprice[city].append(price)
        else:
            rent_avgprice[city] = [price]
    for key, value in rent_avgprice.items():
        s = Series(value)
        rent_avgprice[key] = s.mean()
    for key, value in rent_avgprice.items():
        rent_avgprice[key] = int(value)
    # write the result to cache file
    fd = open('./cache/' + filename, "w", encoding="utf-8")
    fd.write(json.dumps(rent_avgprice))
    return rent_avgprice

def query_rent_avgzone(filename):
    """
        query mongo calculate the avg price of each zone
        return { zone : num}
    """
    # { zone : [price1,price2...]}
    rent_avgzone = {}
    res = RentHouse.objects.only('city', 'price', 'location')
    for item in res:
        tmp = item.location.split('-')
        zone = item.city + '-' + tmp[0]
        price = clean_price(item.price)
        if price == -1:
            continue
        if zone in rent_avgzone.keys():
            rent_avgzone[zone].append(price)
        else:
            rent_avgzone[zone] = [price]
    for key, value in rent_avgzone.items():
        s = Series(value)
        rent_avgzone[key] = s.mean()
    # write the result to cache file
    fd = open('./cache/' + filename, "w")
    fd.write(json.dumps(rent_avgzone))
    return rent_avgzone

def get_data(filename):
    """
        Select functions based on filename
    """
    data = {}
    if check_cache(filename):
        # use cache
        data = get_cache(filename)
    else:
        # no cache file or cache file expire, requery 
        if filename == "rent_count.txt":
            data = query_rent_count(filename)
        elif filename == "rent_avgprice.txt":
            data = query_rent_avgprice(filename)
        elif filename == "rent_avgzone.txt":
            data = query_rent_avgzone(filename)
        else:
            pass
    return data

def get_rent_count():
    """
        get the number of houses in each city
        return { city : num }
    """
    filename = "rent_count.txt"
    rent_count = get_data(filename)
    print(rent_count)
    data = []
    for k, v in rent_count.items():
        data.append({'name' : CITY_MAP[k],"value": v})
    res = wrap_res(data)
    return res

def get_rent_avgprice():
    """
        get the avg price in each city
        return { city : price }
    """
    filename = "rent_avgprice.txt"
    rent_avgprice = get_data(filename)
    data = []
    for k, v in rent_avgprice.items():
        data.append({'name' : CITY_MAP[k],"value": v})
    data = sorted(data, key=lambda x:x["value"],reverse=True)
    res = wrap_res(data)
    return res
    
def get_rent_avgzone():
    """
        get the avg price in each zone
        return { zone : price }
    """
    filename = "rent_avgzone.txt"
    rent_avgzone = get_data(filename)
    data = []
    for k, v in rent_avgzone.items():
        data.append({'name' : k,"value": v})
    data = sorted(data, key=lambda x:x["value"],reverse=True)
    res = wrap_res(data)
    return res
    

def render_rent_count(rent_count):
    data = []
    for city, count in rent_count.items():
        tmp = (CITY_MAP[city], int(count))
        data.append(tmp)
    geo = Geo(
        "test title",
        title_color = "#fff",
        title_pos = "center",
        width = 1530,
        height = 500,
        background_color = "#FAEBD7",
    )    
    attr, value = geo.cast(data)
    geo.add(
        "",
        attr,
        value,
        type = "scatter",
        maptype= "china",
        #symbol_size = 12,
        border_color = "#111",
        geo_normal_color = "#323c48",
        geo_emphasis_color = "#2a333d",
        geo_cities_coords = None,
        is_roam = True,
        visual_range = [0,50000],
        visual_text_color = "#fff",
        is_visualmap=True,
    )
    geo.render("./templates/china_rent_house.html")

def get_echart_script():
    fd = open("./templates/china_rent_house.html","r")
    china_html = fd.read()
    china_script = re.findall("<body>\n(.*?)</body>\n", china_html, re.S)
    fd = open("./templates/main.html","r")
    main_html = fd.read()
    main_html  = main_html.replace("</body>\n", china_script[0] + "</body>\n")
    return main_html

def wrap_res(data):
    res= {
        "status_code" : 200,
        "data" : data,
    }
    return res

def rentHouse(request):
    data_type = request.GET["type"]
    res = {}
    print(type(data_type))
    if data_type == '1':
        res = get_rent_count() 
    elif data_type == '2':
        res = get_rent_avgprice()
    elif data_type == '3':
        res = get_rent_avgzone()
    else:
        print("ERROR no this type %s" % data_type)
    print(res)
    return JsonResponse(res)

def home(request):
    rent_count = get_rent_count()
    rent_avgprice = get_rent_avgprice()
    rent_avgzone = get_rent_avgzone()
    render_rent_count(rent_count)
    print(rent_avgzone)
    html = get_echart_script()
    return HttpResponse(html)
