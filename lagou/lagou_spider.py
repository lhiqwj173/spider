import requests
from retrying import retry
from pymongo import MongoClient

from utils import delay, local_mongo_verify


class LagouSpider(object):
    def __init__(self):
        self.start_url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0"
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "26",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=ABAAABAABEEAAJA2E1CFC7644D4E76BDF777708FAC3CC5D; index_location_city=%E5%85%A8%E5%9B%BD; _ga=GA1.2.967899761.1520866326; user_trace_token=20180312225202-ec61e2db-2604-11e8-b1dd-5254005c3644; LGSID=20180312225202-ec61e5bd-2604-11e8-b1dd-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3De5NxPMk2Dq14n7N24DDS-_P4wTnEPZ41knSNxcxvSQG%26wd%3D%26eqid%3D808ac59a0001e139000000025aa693fe; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180312225202-ec61e938-2604-11e8-b1dd-5254005c3644; X_HTTP_TOKEN=d31df6dfac3252098891a8300e99f3d0; _putrc=8CD25F99333E401B; login=true; unick=%E4%BD%95%E5%90%9B; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=c2c3a877bb5db979b66d70ffeeba47f5667744b191db8eaa; hideSliderBanner20180305WithTopBannerC=1; TG-TRACK-CODE=index_search; SEARCH_ID=89e28abe46e14ee7a9742442bb851731; LGRID=20180312225629-8bac4ed6-2605-11e8-ad5b-525400f775ce",
            "Host": "www.lagou.com",
            "Origin": "https://www.lagou.com",
            "Referer": "https//www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "X-Anit-Forge-Code": "0",
            "X-Anit-Forge-Token": "None",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.client = MongoClient(**local_mongo_verify)
        self.coll = self.client["spider"]["lagou"]

    @retry(stop_max_attempt_number=5)
    def _make_response(self, url, **kwargs):
        if 'method' not in kwargs:
            kwargs['method'] = 'GET'

        new_kwargs = {}
        for k, v in kwargs.items():
            if k in ['method', 'url', 'params', 'data', 'headers', 'cookies', 'files', 'auth', 'timeout',
                     'allow_redirects', 'proxies',
                     'hooks', 'stream', 'verify', 'cert', 'json']:
                new_kwargs[k] = v
            else:
                print('[出现不能解析的 req 请求参数][{0}]'.format(k))
        new_kwargs["timeout"] = 5

        response = requests.request(url=url, **new_kwargs)
        assert response.status_code == 200
        return response

    @delay
    def make_response(self, form):
        try:
            res = self._make_response(self.start_url, data=form, headers=self.headers, method='POST')
        except Exception as e:
            print(e)
            res = None
        return res

    def parse(self, res):
        res_json = res.json()
        position_list = res_json["content"]["positionResult"]["result"]
        items = list()
        for position in position_list:
            item = dict()
            item["companyId"] = position["companyId"]
            item["positionId"] = position["positionId"]
            item["positionName"] = position["positionName"]  # 岗位名称
            item["createTime"] = position["createTime"]  # 发布时间
            item["positionAdvantage"] = position["positionAdvantage"]  # 职位福利
            item["salary"] = position["salary"]  # 薪资
            item["workYear"] = position["workYear"]  # 工作年限
            item["education"] = position["education"]  # 学历
            item["city"] = position["city"]  # 城市
            item["companyLogo"] = "https://www.lagou.com/" + position["companyLogo"]  # 公司图标
            item["jobNature"] = position["jobNature"]  # 职位性质
            item["industryField"] = position["industryField"]  # 公司领域
            item["financeStage"] = position["financeStage"]  # 资产等级
            item["companyLabelList"] = "|".join(position["companyLabelList"])  # 公司标签
            item["companySize"] = position["companySize"]  # 公司规模
            item["companyFullName"] = position["companyFullName"]  # 公司全称
            items.append(item)
        return items

    def insert_mongo(self, items):
        for item in items:
            self.coll.insert(item)

    def run(self):
        for n in range(0, 30):
            form = {
                'first': True if n == 0 else False,
                'kd': 'python',
                'pn': n
            }
            res = self.make_response(form)
            items = self.parse(res)
            self.insert_mongo(items)
            print("已完成{}页".format(n + 1))

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    lagou = LagouSpider()
    lagou.run()
