# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import re
import pymongo
import pymysql




class MongoPipeline(object):
    # 初始化参数
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 以依赖注入的方式获取settings.py中的配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # Spider开启时，初始化数据库连接
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 将item插入MongoDB，集合定义在item中
    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    # Spider结束后，关闭数据库连接
    def close_spider(self, spider):
        self.client.close()


class ImagePipeline(ImagesPipeline):
    # 返回文件名及其相对路径
    # 'https://img.aitaotu.cc:8089/Pics/2020/0115/22/04.jpg'
    # '/Pics/2020/0115/22/04.jpg'
    def file_path(self, request, response=None, info=None):
        image_name = request.meta['item']['image_name']
        image_name=re.search("(.*)\(.*?\)", image_name).group(1)
        name=re.search(r'(.*)/(.*)', request.url).group(2)
        path = 'images/' + image_name + '/' + name
        return path
        #return re.search('(.*)8089(.*)', request.url).group(2)

    # 若下载失败，则抛出异常
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    # 设置请求头，下载图片
    def get_media_requests(self, item, info):
        headers = {
            "Referer": item['referer'],
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }
        yield Request(item['image'], headers=headers,meta={'item':item})
