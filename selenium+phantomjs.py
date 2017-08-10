#coding:utf-8
from bs4 import BeautifulSoup
import random
import re
from selenium import webdriver
import time

addr = []
def getaddr(n):
    for i in range(1,n):
      driver = webdriver.PhantomJS()
      time.sleep(1)
      url="http://www.maikeji.cn/technologies?page=%d$sort=-verifiedAt,-star,-pageViews" % i
      try:
        driver.get(url)
        pagesource=driver.page_source
        time.sleep(1)
        bs=BeautifulSoup(pagesource,'html.parser')
        hrefs = bs.find_all("a", href=re.compile("^/technology/[a-zA-Z0-9]*$"))
        for href in hrefs:
          addr.append(href.attrs["href"])
         # print(href.attrs["href"])
        driver.quit()
      except:
          return "产生异常"
    #print(addr)
    return addr


def gettext(segment):
    driver = webdriver.PhantomJS()
    realurl='http://www.maikeji.cn' + segment 
    try:
        driver.get(realurl)
        pagesource=driver.page_source
        time.sleep(1)
        bs=BeautifulSoup(pagesource,'html.parser')
        #print(bs.prettify())
        contents=bs.find_all("div", {"class":"fr-view ng-binding"})
        data=[]
        for content in contents:
          text = content.get_text()
          data.append(text)
        driver.quit()
        txt ='\n'.join(data)
        return txt
    except:
           return "产生异常"

    

def save(segment):
      with open(root,'at',encoding='utf-8') as fw:
         data=gettext(segment)
         fw.write(data)
         fw.write('\n----------------------------------------------------------\n')

               
if __name__=="__main__":
    n=int(input("输入要爬取的页数："))
    root=input("数据存入文件名（例子：*.txt）：")
    n +=1
    print("开始获得信息url,请等待~~")
    addresses=getaddr(n)
    length=len(addresses)
    print("开始写入！")
    count=0
    for segment in addresses:
       count+=1
       save(segment)
       print('\r当前进度：{:.2f}%'.format(count*100/length),end="")
    print("完毕！")

    
