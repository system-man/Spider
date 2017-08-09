#coding:utf-8
import sys
import time
import random
import math
import json
import base64
import requests
import re
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf8')

weibo_accounts = [
    {'no': '13064564094', 'pa': 'abc123abc'},
    {'no': '13282261374', 'pa': 'abc123abc'},
]

class Getcookie:
    #预登录
    def __init__(self,account,password):
        self.account = account
        self.password = password
        self.session = requests.session()
        self.headers = {
           "Host": "passport.weibo.cn",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360EE",
           }
        self.index_url = "https://passport.weibo.cn/signin/login"
        self.session.get(self.index_url, headers=self.headers)

    def pre_login(self):

        prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
        username = base64.b64encode(self.account.encode("utf-8")).decode("utf-8")
        params = {
             "checkpin" : "1",
             "entry" : "mweibo",
             "su" : username,
             "callback" : "jsonpcallback" + str(long(int(time.time() * 1000) + math.floor(random.random() * 100000))),
        }

        self.headers["Host"] = "login.sina.com.cn"
        self.headers["Referer"] = self.index_url

        predata = self.session.get(prelogin_url,params = params, headers=self.headers)

        if predata.content == "":
            print "登录失败！"
        else:
            datastr = predata.content.encode("utf-8")
            p = re.compile('\((.*)\)')
            json_data = p.search(datastr).group(1)
            jsdata = json.loads(json_data)
            if jsdata["showpin"] == "1":
                headers["Host"] = "passport.weibo.cn"
                capt = self.session.get("https://passport.weibo.cn/captcha/image", headers=headers)
                capt_json = json.loads(capt)
                capt_base64 = capt_json['data']['image'].split("base64,")[1]
                with open('capt.jpg', 'wb') as f:
                    f.write(base64.b64decode(capt_base64))
                    f.close()
                im = Image.open("capt.jpg")
                im.show()
                im.close()
                cha_code = input("请输入验证码\n>")
                return cha_code, capt_json['data']['pcid']

            else:
                return ""

    def login(self):

        pincode = self.pre_login()
        postData = {
            'username' : self.account,
            'password' : self.password,
            'savestate' : '1',
            'r' : '',
            'ec' : '0',
            'pagerefer' : '',
            'entry' : '',
            'wentry' : '',
            'loginfrom' : '',
            'client_id' : '',
            'code' : '',
            'qq' : '',
            'mainpageflag' : '1',
            'hff' : '',
            'hfp' : '',
        }
        if pincode == '':
            pass
        else:
            postdata["pincode"] = pincode[0]
            postdata["pcid"] = pincode[1]
        self.headers["Host"] = "passport.weibo.cn"
        self.headers["Referer"] = self.index_url
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        login_url = "https://passport.weibo.cn/sso/login"
        login = self.session.post(login_url,data=postData,headers = self.headers)
        logindata = json.loads(login.content.decode("utf-8"))
        crossdomain = logindata["data"]["crossdomainlist"]

        uid = logindata["data"]["uid"]
        cn = crossdomain["sina.com.cn"]
    #   print crossdomain["sina.com.cn"]
        # 下面两个对应不同的登录 weibo.com 还是 m.weibo.cn
        # 一定要注意更改 Host
        # mcn = "https:" + crossdomain["weibo.cn"]
        # com = "https:" + crossdomain['weibo.com']
        self.headers["Host"] = "login.sina.com.cn"
        self.session.get(cn, headers=self.headers)
        self.headers["Host"] = "weibo.cn"
        ht = self.session.get("http://weibo.cn/%s/info" % uid, headers=self.headers)
        pa = r'<title>(.*?)</title>'
        res = re.findall(pa, ht.text)
        print "成功登录%s" % res[0][0:-3]
        home = self.session.get("https://m.weibo.cn/", headers=self.headers)
        cookie = self.session.cookies.get_dict()
        return cookie

from User_agent import agents

def Getcookies(weibo_ac):
    cookies=[]
    for elem in weibo_ac:
        account = elem['no']
        password = elem['pa']
        getcookie = Getcookie(account,password)
        getcookie.headers["User-Agent"] = random.choice(agents)
        cookie = getcookie.login()
#        print(cookie)
        if cookie != None:
            cookies.append(cookie)
        getcookie.session.cookies.clear()
    return cookies


cookies = Getcookies(weibo_accounts)


