# -*- coding: utf-8 -*-
import sys
import time
import json
import base64
import requests
import re
import rsa
import binascii
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')


weibo_accounts = [
    {'no': '13064564094', 'pa': 'abc123abc'},
    {'no': '13252260463', 'pa': 'abc123abc'},
    {'no': '13282261374', 'pa': 'abc123abc'},
]


def getcookie(account,password):
    try:
        browser = webdriver.Firefox()
        browser.get("http://weibo.com/login")
        time.sleep(1)

        count = 0
        while "微博" in browser.title and count < 3:
            count += 1

            username = browser.find_element_by_xpath('//input[@node-type="username"]')
            username.clear()
            username.send_keys(account)

            pad = browser.find_element_by_xpath('//input[@type="password"]')
            pad.clear()
            pad.send_keys(password)

            time.sleep(4)

            try:
                browser.save_screenshot("yzm.png")
                yzm = browser.find_element_by_xpath('//input[@name="verifycode"]')
                yzm.clear()
                verify_code = raw_input("请手动输入验证码，从目录下新获取的截图中寻找～")
                #try:
                #    from PIL import Image
                #    img =
                yzm.send_keys(verify_code)
            except Exception as e:
                print "验证码无法输入"
                pass

            commit = browser.find_element_by_xpath('//a[@node-type="submitBtn"]')
            commit.click()
            time.sleep(10)

            if "我的首页" not in browser.title:
                time.sleep(5)

        cookie={}
        if "我的首页" in browser.title:
            for elem in browser.get_cookies():
                cookie[elem["name"]] = elem["value"]

        return json.dumps(cookie)
    except Exception as e:
        return ""
    finally:
        try:
            browser.quit()
        except Exception as e:
            pass



def get_cookie(account,password):
    '''
    1.用base64加密用户名之后仿造一个预登陆，用正则匹配得到各项参数
    2.用上一步里得到的参数，拼接密码明文，再用RSA加密得到密文，并构造POST的form data。
    3.使用构造好的form data仿造登录请求
    4.用正则匹配获得跳转的目标链接。
    5.为了保持登陆，使用session保存cookie。


    会话对象requests.Session能够跨请求地保持某些参数，
    比如cookies，即在同一个Session实例发出的所有请求都保持同一个cookies,
    而requests模块每次会自动处理cookies，这样就很方便地处理登录时的cookies问题。
    '''
      login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
      username = base64.b64encode(account.encode("utf-8")).decode("utf-8")

      url1 = "https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.15)" % username
              "https://login.sina.com.cn/sso/prelogin.php?checkpin =1&entry=mweibo&su=%s=&callback=jsonpcallback" % username
      session = requests.session()
      data = session.get(url1)
      datastr = data.content.encode("utf-8")
      p = re.compile('\((.*)\)')
      json_data = p.search(datastr).group(1)
      datainfo = json.loads(json_data)
      servertime = datainfo["servertime"]
      nonce = datainfo["nonce"]
      pubkey = datainfo["pubkey"]
      rsakv = datainfo["rsakv"]

      rsaPublickey = int(pubkey, 16)
      key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
      message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
      passwd = rsa.encrypt(message, key)  # 加密
      passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。

      postData = {
            "cdult": "3",
            "domain": "sina.com.cn",
            "encoding": "UTF-8",
            "entry": "sso",
            "from": "null",
            "gateway": "1",
            "pagerefer": "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)",
            "prelt": "139",
            "pwencode": "rsa2",
            "returntype": "TEXT",
            "rsakv" : rsakv,
            "savestate": "30",
            "servertime" : servertime,
            "service": "sso",
            "sp" : passwd,
            "nonce" : nonce,
            "sr": "1366 * 768",
            "su": username,
            "useticket": "0",
            "vsnf": "1",
      }
      r = session.post(login_url,data=postData)

      url2 = "https://login.sina.com.cn/crossdomain2.php?action=login&r=https%3A%2F%2Flogin.sina.com.cn%2Fsso%2Flogin.php%3Fclient%3Dssologin.js(v1.4.18)"
      data2 = session.get(url2)
      data2str = data2.content
      p2 = re.compile('location.replace\(\'(.*)\'\)')
      to_url2 = p2.search(data2str).group(1)
#      print type(data2.content)
#      print to_url2

      data3 = session.get(to_url2)
      data3str = data3.content
      p3 = re.compile('location.replace\(\"(.*)\"\)')
      to_url3 = p3.search(data3str).group(1)

      data4 = session.get(to_url3)
      data4str = data4.content
      p4 = re.compile('location.replace\(\'(.*)\'\)')
      to_url4 = p4.search(data4str).group(1)

      data5 = session.get(to_url4)
      data5str = data5.content
      p5 = re.compile('location.replace\(\"(.*)\"\)')
      to_url5 = p5.search(data5str).group(1)

#      print to_url5

      data_end = session.get(to_url5)
      print data_end.content
      cookie = session.cookies.get_dict()
#           print type(cookie)
      return cookie



def Getcookies(weibo_ac):
    cookies=[]
    for elem in weibo_ac:
        account = elem['no']
        password = elem['pa']
        cookie = get_cookie(account,password)

        print(cookie)

        if cookie != None:
            cookies.append(cookie)

    return cookies


cookies = Getcookies(weibo_accounts)



