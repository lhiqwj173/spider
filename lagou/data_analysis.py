import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import matplotlib as mpl  # 配置字体
from pyecharts import Geo  # 地理图
from pymongo import MongoClient

from utils import local_mongo_verify


def mongo2csv():
    client = MongoClient(**local_mongo_verify)
    coll = client["spider"]["lagou"]
    # 岗位名称, 工作年限, 学历, 职位性质, 资产等级, 城市, 薪资, 职位福利, 公司全称
    result = coll.find({}, {'_id': 0,
                            'positionName': 1,
                            'workYear': 1,
                            'education': 1,
                            'jobNature': 1,
                            'financeStage': 1,
                            'city': 1,
                            'salary': 1,
                            'positionAdvantage': 1,
                            'companyFullName': 1})

    df = pd.DataFrame(list(result))
    df.to_csv('lagou_position.csv', index=False)
    client.close()


if __name__ == '__main__':
    mongo2csv()
