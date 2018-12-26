#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     TryLogging.py
   Author:         hejun
   date:          2018-12-18 09:13:45
   Description: 
-------------------------------------------------
"""
import logging
import logging.handlers


def get_logger(log_file_name=None):
    if not log_file_name:
        log_file_name = "save"
    LOG_FILE = './log/{}.log'.format(log_file_name)
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=50  # 当个日志最大10M,保存50个备份
    )
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger(log_file_name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
