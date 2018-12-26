#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     TryGevent.py
   Author:         hejun
   date:          2018-12-20 07:42:04
   Description: 
-------------------------------------------------
"""


def demo():
    import gevent
    from gevent import socket
    urls = [
        'www.baidu.com',
        'www.itcast.cn',
        'www.youku.com'
    ]
    jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
    gevent.joinall(jobs, timeout=2)
    print([job.value for job in jobs])


# gevent并发下载器
from gevent import monkey

monkey.patch_all()

import gevent
import requests


def downloader(url):
    print("Start request: {}".format(url))
    resp = requests.get(url)
    file_name = url.split(".")[1]
    with open("./html/" + file_name + ".html", "wb") as f:
        f.write(resp.content)
    print("Saved: {}.".format(file_name))


def run():
    urls = [
        'http://www.baidu.com/',
        'http://www.itcast.cn/',
        'http://www.itheima.com/',
        'http://www.youku.com/',
        'http://www.taobao.com/',
        'http://www.jd.com/'
    ]
    import time
    start = time.time()
    gevent.joinall(
        [gevent.spawn(downloader, url) for url in urls]
    )
    end = time.time()
    print("gevent耗时: {} s.".format(end - start))
    # start = time.time()
    # for url in urls:
    #     downloader(url)
    # end = time.time()
    # print("单线程耗时: {} s.".format(end - start))


if __name__ == '__main__':
    # demo()
    run()
