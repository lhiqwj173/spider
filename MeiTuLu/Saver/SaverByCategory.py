#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     Saver.py
   Author:         hejun
   date:          2018-12-17 13:04:26
   Description: 
-------------------------------------------------
"""
import os
import requests
from pymongo import MongoClient
from retrying import retry

"""
[
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
"""


class Saver(object):
    """图片保存器"""

    def __init__(self, category, start):
        self.category = category
        self.category_folder = "./images/" + category
        if not os.path.exists(self.category_folder):
            os.mkdir(self.category_folder)
        self.start = start
        self.img_url = "https://mtl.ttsqgs.com/images/img/{model_id}/{img_id}.jpg"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        }
        self.handle = MongoClient("localhost", 27017)
        self.coll = self.handle["spider"]["meitulu_12_17_13_00"]

    def read_data(self):
        models = self.coll.find({"category": self.category}, {"_id": 0}, no_cursor_timeout=True)
        for model in models[self.start:]:
            for i in range(1, model["img_nums"] + 1):
                yield dict(
                    Referer=model["detail_url"],
                    title=model["title"].replace("/", "&"),
                    model_id=model["model_id"],
                    url=self.img_url.format(
                        model_id=model["model_id"],
                        img_id=i
                    ),
                    img_id="0{}".format(i) if i < 10 else str(i)
                )

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, img):
        self.headers["Referer"] = img["Referer"]
        resp = requests.get(img["url"], headers=self.headers)
        if resp.status_code == 403:
            return None
        assert resp.status_code == 200
        return resp.content

    def req_save_img(self):
        for img in self.read_data():
            # print(img)
            img_content = self._parse_url(img)
            if not img_content:
                continue
            img_floder = "{c_floder}/{m_id}_{title}".format(
                c_floder=self.category_folder,
                m_id=img["model_id"],
                title=img["title"]
            )
            if not os.path.exists(img_floder):
                os.mkdir(img_floder)
            img_name = "{img_floder}/{img_id}.jpg".format(
                img_floder=img_floder,
                img_id=img["img_id"]
            )
            with open(img_name, "wb") as f:
                f.write(img_content)

    def run(self):
        try:
            self.req_save_img()
        except Exception as e:
            print(e)
            print("--" * 50)
            img_nums = [x for x in os.listdir(self.category_folder) if not x.startswith(".")]
            print(len(img_nums))
            print("--" * 50)

    def __del__(self):
        self.handle.close()


if __name__ == '__main__':
    import sys

    category = sys.argv[1]
    if len(sys.argv) == 2:
        start = 0
    else:
        start = int(sys.argv[2])
    saver = Saver(category, start)
    saver.run()
