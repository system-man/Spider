# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,codecs
from items import SinauserspiderItem
from settings import *
import MySQLdb

class MySQLstorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user=dbuser,passwd=dbpass,db=dbname, host=dbhost, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def check_re(self,id):
        checksql = 'SELECT EXISTS (SELECT 1 FROM userinfo WHERE id = %(id)s);'
        checkvalue = {'id': id}
        self.cursor.execute(checksql, checkvalue)
        return self.cursor.fetchall()[0]

    def process_item(self, item, spider):
        id = item['_id']
        check_result = self.check_re(id)
        if check_result[0] == 1:
            print "重复数据"
            pass
        else:
            username=item['username']
            level=item['level']
            location=item['location']
            gender=item['gender']
            education=item['education']
            work=item['work']
            birthday=item['birthday']
            personalurl=item['personalurl']
            about_me=item['about_me']
            sexOrientation=item['sexOrientation']
            sentiment=item['sentiment']
            emailaddress=item['emailaddress']
            insertsql = 'INSERT INTO userinfo \
                         (username,level,location,gender,education,work,birthday,personalurl,about_me,sexOrientation,sentiment,emailaddress,id) VALUES \
                         (%(username)s,%(level)s,%(location)s,%(gender)s,%(education)s,%(work)s,%(birthday)s,%(personalurl)s,%(about_me)s,%(sexOrientation)s,%(sentiment)s,%(emailaddress)s,%(id)s);'
            insertvalues = {
                'username':username,
                'level':level,
                'location':location,
                'gender':gender,
                'education':education,
                'work':work,
                'birthday':birthday,
                'personalurl':personalurl,
                'about_me':about_me,
                'sexOrientation':sexOrientation,
                'sentiment':sentiment,
                'emailaddress':emailaddress,
                'id':id,
            }
            self.cursor.execute(insertsql,insertvalues)
            self.conn.commit()
        return item


class jsonwithEncodingUserPipeline(object):
    """
    summary:json持久化
    """
    def __init__(self):
        self.file = codecs.open('sina.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item), ensure_ascii = False) + "," + "\n"
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()
