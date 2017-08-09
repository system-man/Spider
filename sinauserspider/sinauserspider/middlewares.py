# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from User_agent import agents
from login import cookies


class UserAgentMiddleware(object):
    """
    更换User-Agent
    """
    def process_request(self,request,spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class CookieMiddleware(object):
     """
     更换cookie
     """
     def process_request(self,request,spider):
         cookie = random.choice(cookies)
         request.cookies = cookie