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
from gevent import monkey

monkey.patch_all()
import os
import requests

import gevent
from pymongo import MongoClient
from retrying import retry
from TryLogging import get_logger

"""
{
    "_id" : ObjectId("5c172d60b0b0fb2a02393585"),
    "category" : "toutiaonvshen",
    "img_nums" : 33,
    "model_name" : "王紫琳",
    "labels" : "美胸_OL",
    "title" : "[TouTiao头条女神] 王紫琳 - 王紫琳OL 写真套图",
    "detail_url" : "https://www.meitulu.com/item/15473.html",
    "model_id" : "15473"
}
"""

# todo
"""
实现多任务处理：
1. 查询数据库后，做任务分发
2. 一个协程完成100个model的保存
"""

"""
合并文件夹
------
➜  test tree .
.
├── a
│   └── a1
│       └── PDF_430396971.pdf
└── b
    └── a1
        ├── PDF_430396971.pdf
        └── PDF_430696425.pdf
--------
➜  a rsync -av a1 ../b/
building file list ... done
a1/
a1/PDF_430396971.pdf

sent 202858 bytes  received 48 bytes  405812.00 bytes/sec
total size is 202678  speedup is 1.00
"""


class Saver(object):
    """图片保存器"""

    def __init__(self, part):
        self.part = part
        part_folder = "./images/part_{}".format(self.part)
        if not os.path.exists(part_folder):
            os.mkdir(part_folder)
        self.part_folder = part_folder
        self.img_url = "https://mtl.ttsqgs.com/images/img/{model_id}/{img_id}.jpg"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        }
        self.logger = get_logger("part{}".format(part))
        self.handle = MongoClient("localhost", 27017)
        self.coll = self.handle["spider"]["meitulu_12_18_08_25"]

    def read_data(self):
        # models = self.coll.find({"category": self.category}, {"_id": 0}, no_cursor_timeout=True)
        with open("./model_ids/model_ids_{}".format(self.part)) as f:
            model_ids = eval(f.read())
        model_ids = [str(x) for x in model_ids]
        saved_models = [x for x in os.listdir(self.part_folder) if not x.startswith(".")]
        for s_model in saved_models:
            m_id = s_model.split("_")[0]
            res = self.coll.find_one({"_id": m_id})
            img_nums = int(res["img_nums"])
            file_nums = len([x for x in os.listdir(self.part_folder + "/" + s_model) if x.endswith(".jpg")])
            if img_nums == file_nums:
                model_ids.remove(m_id)
        print("本轮需要下载[{}]个model.".format(len(model_ids)))
        models = self.coll.find({"_id": {"$in": model_ids}})
        models = list(models)
        self.handle.close()
        return models

    def make_task(self, models):
        for model in models:
            for i in range(1, model["img_nums"] + 1):
                yield dict(
                    Referer=model["detail_url"],
                    title=model["title"].replace("/", "&"),
                    model_id=model["_id"],
                    url=self.img_url.format(
                        model_id=model["_id"],
                        img_id=i
                    ),
                    img_id="0{}".format(i) if i < 10 else str(i)
                )

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, img):
        self.headers["Referer"] = img["Referer"]
        resp = requests.get(img["url"], headers=self.headers)
        if resp.status_code != 200:
            self.logger.warn("url: [{url}] got status_code:[{s_code}].".format(
                url=img["url"],
                s_code=resp.status_code
            ))
            return None
        return resp.content

    def req_save_img(self, models):
        for img in self.make_task(models):
            # print(img)
            img_floder = "{p_folder}/{m_id}_{title}".format(
                p_folder=self.part_folder,
                m_id=img["model_id"],
                title=img["title"]
            )
            if not os.path.exists(img_floder):
                os.mkdir(img_floder)
            img_name = "{img_floder}/{img_id}.jpg".format(
                img_floder=img_floder,
                img_id=img["img_id"]
            )
            if os.path.exists(img_name):  # 文件已存在，跳过，不必请求网络文件
                continue
            img_content = self._parse_url(img)
            if not img_content:
                continue
            with open(img_name, "wb") as f:
                f.write(img_content)
            self.logger.info(
                "model_id is: [{model_id}], img_id: [{img_id}] saved.".format(
                    img_id=img["img_id"],
                    model_id=img["model_id"],
                ))

    def run(self):
        try:
            models = self.read_data()
            gevent.joinall(
                [gevent.spawn(
                    self.req_save_img,
                    models[i:50 + i]
                ) for i in range(0, len(models), 50)]
            )
        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    import sys

    saver = Saver(sys.argv[1])
    saver.run()
