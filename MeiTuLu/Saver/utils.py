#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:      urils.py
   Author:         hejun
   date:          2018-12-20 23:36:54
   Description: 
-------------------------------------------------
"""

import os

import shutil
from pymongo import MongoClient

handle = MongoClient("localhost", 27017)
coll = handle["spider"]["meitulu_12_18_08_25"]


def classify(path):
    os.chdir(path)
    models = [x for x in os.listdir(".") if not x.startswith(".")]
    for model in models:
        m_id = model.split("_")[0]
        res = coll.find_one({"_id": m_id})
        cate = res["category"]
        if not os.path.exists(cate):
            os.mkdir(cate)
        shutil.move(model, cate)

    handle.close()


def check_downlod_missing(path):
    p_id = path.split("/")[-1].split("_")[-1]
    with open("./model_ids/model_ids_{}".format(p_id)) as f:
        tasks = eval(f.read())
    os.chdir(path)
    models = [x for x in os.listdir(".") if not x.startswith(".")]
    i = 0
    for model in models:
        m_id = model.split("_")[0]
        res = coll.find_one({"_id": m_id})
        img_nums = int(res["img_nums"])
        file_nums = len([x for x in os.listdir(model) if x.endswith(".jpg")])
        if img_nums == file_nums:
            tasks.remove(int(m_id))
        else:
            i += 1
            print(i, m_id, img_nums, file_nums)
    print("还有{}个model未完成下载.".format(len(tasks)))


def update_img_nums(path):
    os.chdir(path)
    models = [x for x in os.listdir(".") if not x.startswith(".")]
    for model in models:
        m_id = model.split("_")[0]
        res = coll.find_one({"_id": m_id})
        img_nums = int(res["img_nums"])
        file_nums = len([x for x in os.listdir(model) if x.endswith(".jpg")])
        if img_nums != file_nums:
            coll.update_one({'_id': m_id}, {'$set': {'img_nums': str(file_nums)}})
    print("[{}] data has been updated.".format(path))
    os.chdir("..")
    handle.close()


def extract_folder(path):
    os.chdir(path)
    cates = [x for x in os.listdir(".") if not x.startswith(".")]
    for cate in cates:
        models = [x for x in os.listdir(cate) if not x.startswith(".")]
        for model in models:
            shutil.move(cate+"/"+model, ".")

    os.chdir("..")


if __name__ == '__main__':
    check_downlod_missing("./images/part_10")
    # update_img_nums("./images/part_8")
    # classify("./images/part_8")
