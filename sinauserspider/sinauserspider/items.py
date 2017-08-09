# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class SinauserspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    username:昵称
    follows:关注
    followers:粉丝
    articles:微博数
    level:等级
    location:所在地
    gender:性别
    birthday:生日
    personalurl:个性域名
    about_me:简介
    emailaddress:邮箱地址
    _id:用户ID
    """
    username=Field()
    level=Field()
    location=Field()
    gender=Field()
    education=Field()
    work=Field()
    birthday=Field()
    personalurl=Field()
    about_me=Field()
    sexOrientation=Field()
    sentiment=Field()
    emailaddress=Field()
    _id=Field()
