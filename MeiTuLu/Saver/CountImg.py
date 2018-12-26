#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     CountImg.py
   Author:         hejun
   date:          2018-12-17 13:55:42
   Description: 
-------------------------------------------------
"""
from pymongo import MongoClient

CATEGORYS = [
    "toutiaonvshen",
    "fengsuniang",
    "qizhi",
    "jipin",
    "nvshen",
    "nenmo",
    "youwu",
    "wangluohongren",
    "baoru",
    "xinggan",
    "youhuo",
    "meixiong",
    "shaofu",
    "mengmeizi",
    "loli",
    "keai",
    "changtui",
    "huwai",
    "gangtai",
    "bijini",
    "qingchun",
    "weimei",
    "guochan",
    "qingxin",
    "rihan"
]

handle = MongoClient("localhost", 27017)
coll = handle["spider"]["meitulu_12_18_08_25"]


def cate_model_nums():
    result = dict()
    for cate in CATEGORYS:
        result[cate] = coll.find({"category": cate}).count()
    handle.close()
    res = sorted(result.items(), key=lambda x: x[1])
    print(res)


def check():
    res = coll.find({"category": "baoru"})
    for x in res[305: 315]:
        print(x["detail_url"])
    handle.close()


def distinct_id():
    res = coll.distinct("model_id")
    res = [int(x) for x in res]
    res.sort()
    per_len = 1500
    n = (len(res) // per_len) + 1
    for i in range(n + 1):
        with open("./model_ids/model_ids_" + str(i + 1), "w") as f:
            f.write(str(res[per_len * i: per_len * (i + 1)]))
    handle.close()


def test():
    res = coll.find({"category": "loli"})
    print(type(res))
    res = list(res)
    print(type(res))
    handle.close()


def try_reqeust_not_exsist():
    import requests
    model_id = "1066"
    img_id = 30
    ref = "https://www.meitulu.com/item/1066.html"
    url = "https://mtl.ttsqgs.com/images/img/{model_id}/{img_id}.jpg".format(
        model_id=model_id,
        img_id=img_id
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Referer": ref
    }
    resp = requests.get(url=url, headers=headers)
    print(resp.status_code)
    print("--" * 40)
    print(resp.text)
    print("--" * 40)


if __name__ == '__main__':
    # cate_model_nums()
    # check()
    # distinct_id()
    test()
    # try_reqeust_not_exsist()
