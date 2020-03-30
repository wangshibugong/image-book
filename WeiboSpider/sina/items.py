# -*- coding: utf-8 -*-
from scrapy import Item, Field


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()
    weibo_url = Field()
    created_at = Field()
    like_num = Field()
    repost_num = Field()
    comment_num = Field()
    content = Field()
    user_id = Field()
    tool = Field()
    image_url = Field()
    video_url = Field()
    origin_weibo = Field()
    crawl_time = Field()

class InformationItem(Item):
    """ 个人信息 """
    _id = Field()
    nick_name = Field()
    gender = Field()
    place=Field()
    brief_introduction = Field()
    birthday = Field()
    tweets_num = Field()
    follows_num = Field()
    fans_num = Field()
    crawl_time = Field()

class CommentItem(Item):
    """
    微博评论信息
    """
    _id = Field()
    comment_user_id = Field()
    content = Field()
    weibo_url = Field()
    created_at = Field()
    like_num = Field()
    crawl_time = Field()
