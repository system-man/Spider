# -*- coding: utf-8 -*-
import math
import datetime
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from sinauserspider.items import  SinauserspiderItem
import re

class SinauserSpider(scrapy.Spider):
    #通过cookie 登录移动端，爬取信息

    name = 'sinauser'
    allowed_domains = ['https://weibo.cn']
    start_urls = ['https://weibo.cn/5762793904/follow']
    # 存储基本信息已被获取的用户的id,等待爬取其所关注的人的基本信息
    all_ID = set()

    def parse(self,response):
        # 主要获取关注者的id
        ID = re.findall('(\d+)/follow', response.url)[0]
        selector = Selector(response)
        text_f = ";".join(selector.xpath('//td[@valign="top"]/a').extract())
        uids = set(re.findall('href="https://weibo.cn/u/(.*?)">'.decode('utf8'), text_f))
        for uid in uids:
            self.all_ID.add(uid)
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_basic_info,dont_filter=True)
        #当页所有人信息爬取完毕后，获取下一页链接，并对下一页发起请求
        next_page = ";".join(selector.xpath('//div[@class="pa"]').extract())
        p = re.compile('a href="(.*?)">下页')
        nextpage = p.search(next_page.encode("utf-8"))
        if nextpage is None:
            id = self.all_ID.pop()
            if id:
                yield Request(url="https://weibo.cn/%s/follow" % id, callback=self.parse, dont_filter=True)
        else:
            next_url = "https://weibo.cn" + nextpage.group(1)
            yield Request(url=next_url, callback=self.parse, dont_filter=True)



    def parse_basic_info(self, response):

        #解析用户数据,基本信息

        item=SinauserspiderItem()
        selector=Selector(response)
        ID = re.findall('(\d+)/info', response.url)[0]
        try:
            text1 = ";".join(selector.xpath('//div//text()').extract())    # 获取标签里的所有text()
            username = re.findall('昵称[：:]?(.*?);'.decode('utf8'), text1)
            gender = re.findall('性别[：:]?(.*?);'.decode('utf8'), text1)
            location = re.findall('地区[：:]?(.*?);'.decode('utf8'), text1)
            about_me = re.findall('简介[：:]?(.*?);'.decode('utf8'), text1)
            birthday = re.findall('生日[：:]?(.*?);'.decode('utf8'), text1)
            sexOrientation = re.findall('性取向[：:]?(.*?);'.decode('utf8'), text1)
            sentiment = re.findall('感情状况[：:]?(.*?);'.decode('utf8'), text1)
            education = re.findall('学习经历;(.*？);'.decode('utf-8'), text1)
            work = re.findall('工作经历;(.*？);'.decode('utf-8'), text1)
            emailaddress = re.findall(';([a-zA-Z0-9]@[a-zA-Z0-9]\.com|cn)'.decode('utf8'),text1)
            personalurl = re.findall('互联网[：:]?(.*?);'.decode('utf8'),text1)
            print personalurl[0]
            level = re.findall('会员等级[：:]?(.*?);'.decode('utf8'), text1)

            item['_id'] = ID

            if username and username[0]:
                 item["username"] = username[0].replace(u"\xa0", "")
            if gender and gender[0]:
                 item["gender"] = gender[0].replace(u"\xa0", "")
            else:
                item["gender"] = u"\xa0"
            if location and location[0]:
                 item["location"] = location[0].replace(u"\xa0", "")
            else:
                item["location"] = u"\xa0"
            if about_me and about_me[0]:
                 item["about_me"] = about_me[0].replace(u"\xa0", "")
            else:
                item["about_me"] = u"\xa0"
            if birthday and birthday[0]:
                 # try:
                 #     birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                 #     item["birthday"] = birthday - datetime.timedelta(hours=8)
                 # except Exception:
                 item['birthday'] = birthday[0]  # 有可能是星座，而非时间
            else:
                item["birthday"] = u"\xa0"
            if sexOrientation and sexOrientation[0]:
                  if sexOrientation[0].replace(u"\xa0", "") == gender[0]:
                     item["sexOrientation"] = "同性恋"
                  else:
                     item["sexOrientation"] = "异性恋"
            else:
                item["sexOrientation"] = u"\xa0"
            if sentiment and sentiment[0]:
                  item["sentiment"] = sentiment[0].replace(u"\xa0", "")
            else:
                item["sentiment"] = u"\xa0"
            if level and level[0]:
                  item["level"] = level[0].replace(u"\xa0", "")
            if personalurl:
                  item["personalurl"] = personalurl[0]
            else:
                item["personalurl"] = u"\xa0"
            if education and education[0]:
                item["education"] = education[0].replace(u"\xa0", "")
            else:
                item["education"] = u"\xa0"
            if work and work[0]:
                item["work"] = work[0].replace(u"\xa0", "")
            else:
                item["work"] = u"\xa0"
            if emailaddress and emailaddress[0]:
                item["emailaddress"] = emailaddress[0].replace(u"\xa0", "")
            else:
                item["emailaddress"] = u"\xa0"
        except Exception as e:
                print "信息提取出错"
                pass
        yield item






























