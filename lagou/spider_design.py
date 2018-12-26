from retrying import retry

from utils import delay


class LagouSpider(object):
    """拉勾网爬虫"""
    def __init__(self):
        """必要初始化操作"""
        pass

    def _make_response(self):
        """发送请求"""
        pass

    def make_response(self):
        """获取响应"""
        pass

    def parse(self):
        """数据解析"""
        pass

    def insert_mongo(self):
        """数据插入mongoDB"""
        pass

    def run(self):
        """爬虫启动"""
        pass

    def __del__(self):
        """爬虫析构，资源关闭"""
        pass


if __name__ == '__main__':
    lagou = LagouSpider()
    lagou.run()
