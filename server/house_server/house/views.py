#coding=utf-8
from __future__ import unicode_literals
import os
import sys
import json
import time
from pyecharts import Geo,Map
from house.models import RentHouse
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
#    reload(sys)
#    sys.setdefaultencoding(default_encoding)

EXPIRED = 86400
CACHE_FILENAME = ".rent_house_count"
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
}

def _query_mongo():
    """
        query mongo to calculate the number of houses in each city
        return {"city" : num}
    """
    rent_count = {}
    res = RentHouse.objects.only('city')
    for item in res:
        city = item.city
        if city in rent_count.keys():
            rent_count[city] += 1
        else:
            rent_count[city] = 1
    # write the result to cache file
    fd = open(CACHE_FILENAME, "w")
    fd.write(json.dumps(rent_count))
    return rent_count

def _get_rent_count():
    """
        get the number of houses in each city
        return {"city" : num}
    """
    rent_count = {}
    # cur path
    path = os.getcwd()
    # all file and dir in cur path
    listdir = os.listdir(path)
    # check if have cache file 
    if CACHE_FILENAME in listdir:
        update_time = os.path.getmtime(path + '/' + CACHE_FILENAME)
        now = time.time()
        # if cache file last update time less than EXPIRED , get cache
        if now - update_time < EXPIRED:
            fd = open(CACHE_FILENAME, 'r')
            s = fd.read()
            rent_count = json.loads(s)
    # no cache file or cache file expire, requery 
    if rent_count == {}:
        rent_count = _query_mongo()
    return rent_count

def _render_rent_count(rent_count):
    data = []
    for city, count in rent_count.items():
        tmp = (CITY_MAP[city], int(count))
        data.append(tmp)
    print(data)
    geo = Geo(
        "test title",
        title_color = "#fff",
        title_pos = "center",
        width = 1200,
        height = 600,
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
    geo.render("./templates/test.html")

def home(request):
    rent_count = _get_rent_count()
    _render_rent_count(rent_count)
    fd = open("./templates/test.html","r")
    html = fd.read()
    return HttpResponse(html)
