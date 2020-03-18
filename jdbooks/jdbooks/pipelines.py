# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from .settings import MONGODB_HOST,MONGODB_PORT,MONGODB_DBNAME,MONGODB_DOCNAME,IMAGES_STORE
import pymongo
import os
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
class JdbooksPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        #settings = get_project_settings()
        # 获取setting主机名、端口号和数据库名
        host = MONGODB_HOST
        port = MONGODB_PORT
        dbname = MONGODB_DBNAME

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[MONGODB_DOCNAME]
    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.insert(data)
        return item



class JiandanPipeline(ImagesPipeline):
    #重定义
    def get_media_requests(self, item, info):
        #for image_url in item['image_urls']:
        image_url = item['image_url']
        yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        # path = super(JiandanPipeline, self).file_path(request, response, info)
        # second_title = request.item.get('second_title')
        # image_store = IMAGES_STORE
        # title_path = os.path.join(image_store, second_title)
        # if not os.path.exists(title_path):
        #     os.makedirs(title_path)
        # image_name = path.replace("full/", "")
        # image_path = os.path.join(title_path, image_name)
        image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
        return image_guid
        #return image_path,image_guid

    #重定义
    def item_completed(self, results, item, info):
        '''
        for ok, x in results:
             if ok:
                print(x['path'])
        :param results:
        :param item:
        :param info:
        :return:
        '''
        images_paths = [x['path'] for ok, x in results if ok]
        if not images_paths:
           raise DropItem("Item contains no images")
        return item
