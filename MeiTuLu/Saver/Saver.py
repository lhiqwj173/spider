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
1. 403请求可以用日志记录
2. 为了方便查看，可以在保存日志记录中添加【分类】字段.
"""


class Saver(object):
    """图片保存器"""

    def __init__(self, part, start):
        self.part = part
        part_folder = "./images/part_{}/".format(self.part)
        if not os.path.exists(part_folder):
            os.mkdir(part_folder)
        self.part_folder = part_folder
        self.start = start
        self.img_url = "https://mtl.ttsqgs.com/images/img/{model_id}/{img_id}.jpg"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
        }
        self.logger = get_logger("part{}".format(part))
        self.handle = MongoClient("localhost", 27017)
        self.coll = self.handle["spider"]["meitulu_12_18_08_25"]

    def check_category_folder(self):
        self.category_folder = self.part_folder + self.category
        if not os.path.exists(self.category_folder):
            os.mkdir(self.category_folder)

    def read_data(self):
        # models = self.coll.find({"category": self.category}, {"_id": 0}, no_cursor_timeout=True)
        with open("./model_ids/model_ids_{}".format(self.part)) as f:
            model_ids = eval(f.read())
        model_ids = [str(x) for x in model_ids]
        models = self.coll.find({"_id": {"$in": model_ids}})
        models = list(models)
        self.handle.close()
        for m_id, model in enumerate(models):
            if m_id < self.start:
                continue
            self.category = model["category"]
            self.check_category_folder()
            self.logger.info(
                "No.[{saved_id}] begin to save, it's model_id is: [{model_id}] and category: [{category}].".format(
                    saved_id=m_id,
                    model_id=model["_id"],
                    category=self.category
                ))
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

    def req_save_img(self):
        for img in self.read_data():
            # print(img)
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
            if os.path.exists(img_name):  # 当前要保存的文件已存在，跳过
                continue
            img_content = self._parse_url(img)
            if not img_content:
                continue
            
            with open(img_name, "wb") as f:
                f.write(img_content)


    def run(self):
        try:
            import time
            start = time.time()
            self.req_save_img()
            end = time.time()
            print("单线程保存200个model耗时: {}".format(end - start))
        except Exception as e:
            self.logger.error(e)
            return


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        start = 0
    else:
        start = int(sys.argv[2])
    saver = Saver(sys.argv[1], start)
    saver.run()
