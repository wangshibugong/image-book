# encoding: utf-8
import random

import pymongo
from sina.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, DB_NAME
import urllib.request
import zlib
import linecache
import random
import requests
import json


class CookieMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """

    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']

    def process_request(self, request, spider):
        all_count = self.account_collection.find({'status': 'success'}).count()
        if all_count == 0:
            raise Exception('没账号了')
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({'status': 'success'})[random_index]
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account
class RedirectMiddleware(object):
    """
    检测账号是否正常
    302 / 403,说明账号cookie失效/账号被封，状态标记为error
    418,偶尔产生,需要再次请求
    """
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']
    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 302 or http_code == 403:
            self.account_collection.find_one_and_update({'_id': request.meta['account']['_id']},
                                                        {'$set': {'status': 'error'}}, )
            return request
        elif http_code == 418:
            spider.logger.error('ip 被封了!')
            return request
        else:
            return response

class IPProxyMiddleware(object):

    def fetch_proxy(self):

        # 如果需要加入代理IP，请重写这个函数
        # 这个函数返回一个代理ip，'ip:port'的格式，如'12.34.1.4:9090'

        req = requests.get(url="http://localhost:5555/random")

        ip=req.text
        print(ip)

        return ip

    def process_request(self, request, spider):
        proxy_data = self.fetch_proxy()
        if proxy_data:
            current_proxy = f'http://{proxy_data}'
            spider.logger.debug(f"当前代理IP:{current_proxy}")
            request.meta['proxy'] = current_proxy

# class ProxyMiddlleWare(object):
#     def __init__(self):
#         super(ProxyMiddlleWare, self).__init__()
#
#     def process_request(self, request, spider):
#         # 得到地址
#         proxy = self.get_Random_Proxy()
#         print(proxy + "**********")
#         # 设置代理
#         request.meta['proxy'] = "https://" + proxy
#
#     # 这个方法是从文档中读取id地址
#     def get_Random_Proxy(self):
#         with open(r"C:\英雄时刻\ip.txt", 'r') as file:
#             text = file.readlines()
#         proxy = random.choice(text).strip()
#         return proxy
#
#     def process_response(self, request, response, spider):
#         # 如果该ip不能使用，更换下一个ip
#         if response.status != 200:
#             proxy = self.get_Random_Proxy()
#             print('更换ip' + proxy)
#             request.meta['proxy'] = "http://" + proxy
#             return request
#

# if __name__ == "__main__":
#
#     def ip_get():
#         api_url = "http://dev.kdlapi.com/api/getproxy/?orderid=928476462524115&num=100&signature=3putftr5skvtw5zmsqk47eoae3pz6ld7&protocol=2&method=2&an_an=1&an_ha=1&sep=1"
#         headers = {"Accept-Encoding": "Gzip"}  #使用gzip压缩传输数据让访问更快
#
#         req = urllib.request.Request(url=api_url, headers=headers)
#
#         # 请求api链接
#         res = urllib.request.urlopen(req)
#
#         print(res.code)  # 获取Reponse的返回码
#         content_encoding = res.headers.get('Content-Encoding')
#         if content_encoding and "gzip" in content_encoding:
#             print(zlib.decompress(res.read(), 16 + zlib.MAX_WBITS).decode('utf-8'))  #获取页面内容
#             # io=zlib.decompress(res.read(), 16 + zlib.MAX_WBITS).decode('utf-8')
#             # i=io.split('\r\n')
#             # # li=linecache.getline(io,2)
#             # #print(i)
#             # ip=random.choice(i)
#             # # ip_1=i.split(':')
#             # # ip=ip_1[0]
#             # # port=ip_1[1]
#             #
#             # #ip="https://{0}:{1}".format(ip, port)
#             # print(ip)
#             # return ip
#         else:
#             print( res.read().decode('utf-8')) #获取页面内容
#     o=ip_get()
class ChangeProxy(object):
    def __init__(self):
        '''
        初始化变量
        get_url 是请求的api
        temp_url 是验证的地址
        ip_list 是ip
        '''
        self.get_url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=53bc33136ebc45dca0dd67981dc8fb3c&orderno=YZ20203272780JeQIQq&returnType=2&count=10"
        self.temp_url = "http://www.baidu.com"
        self.ip_list = []
        # 用来记录使用ip的个数，或者是目前正在使用的是第几个IP,本程序，我一次性获得了10个ip，所以count最大默认为9
        self.count = 0
        # 用来记录每个IP的使用次数,此程序，我设置为最大使用4次换下一个ip
        self.evecount = 0
    def getIPData(self):
        '''
        这部分是获得ip，并放入ip池（先清空原有的ip池）
        :return:
        '''
        temp_data = requests.get(url=self.get_url).text
        self.ip_list.clear()
        for eve_ip in json.loads(temp_data)["RESULT"]:
            print(eve_ip)
            self.ip_list.append({
                "ip":eve_ip["ip"],
                "port":eve_ip["port"]
            })
    def changeProxy(self,request):
        '''
        修改代理ip
        :param request: 对象
        :return:
        '''
        request.meta["proxy"] = "http://" + str(self.ip_list[self.count-1]["ip"]) + ":" + str(self.ip_list[self.count-1]["port"])
    def yanzheng(self):
        '''
        验证代理ip是否可用，默认超时5s
        :return:
        '''
        requests.get(url=self.temp_url,proxies={"http":str(self.ip_list[self.count-1]["ip"]) + ":" + str(self.ip_list[self.count-1]["port"])},timeout=5)
    def ifUsed(self,request):

        '''
        切换代理ip的跳板
        :param request:对象
        :return:
        '''
        try:
            self.changeProxy(request)
            self.yanzheng()
        except:
            if self.count == 0 or self.count == 10:
                self.getIPData()
                self.count = 1
            self.evecount = 0
            self.count = self.count + 1
            self.ifUsed(request)
    def process_request(self, request, spider):
        if self.count == 0 or self.count==10:
            self.getIPData()
            self.count = 1
        if self.evecount == 3:
            self.count = self.count + 1
            self.evecount = 0
        else:
            self.evecount = self.evecount + 1
        self.ifUsed(request)
