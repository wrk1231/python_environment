#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')
if(len(sys.argv) >=2):
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"请输入user_id: "))

cookie = {"Cookie":"SCF=AgRMuiETtFypy2n-QsLOfy2vdLej1n7uD-N5hHa7LLoaQNDvlxVL0EmNQg8oppUaLPLLpUtjjiomcmFuw_E7bEY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQMF-9mS0J5NbNa1gIGEkm5JpX5o2p5NHD95QE1KeNS0e4ShzfWs4DqcjZ9JHLdsLV9c8j9Btt; _T_WM=e6ad74cef182262d28c71ff1317ef21b; H5_INDEX=3; H5_INDEX_TITLE=feelingale; SUB=_2A250BenGDeRhGeRH6FUW8yfIyTmIHXVXCfeOrDV6PUJbkdBeLUfFkW1mvpwd2QxHyXXodcNiuDKmDT7Uvg..; SUHB=09P9HDSLmleeHE; SSOLoginState=1493277078; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D4101163215288027%26luicode%3D10000011%26lfid%3D1076032937739425%26uicode%3D20000174"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

html = requests.get(url, cookies = cookie).content
selector = etree.HTML(html)
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = "" 
urllist_set = set()
word_count = 1
image_count = 1

print u'爬虫准备就绪...'

for page in range(1,pageNum+1):

  #获取lxml页面
  url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
  lxml = requests.get(url, cookies = cookie).content

  #文字爬取
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count >= 4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1

  #图片爬取
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  for imgurl in urllist:
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    image_count +=1

fo = open("/Users/wrk/%s"%user_id, "wb")
fo.write(result)
word_path=os.getcwd()+'/%d'%user_id
print u'文字微博爬取完毕'

link = ""
fo2 = open("/Users/wrk/%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
  link = link + eachlink +"\n"
fo2.write(link)
print u'图片链接爬取完毕'

if not urllist_set:
  print u'该页面中不存在图片'
else:
  #下载图片,保存在当前目录的pythonimg文件夹下
  image_path=os.getcwd()+'/weibo_image'
  if os.path.exists(image_path) is False:
    os.mkdir(image_path)
  x=1
  for imgurl in urllist_set:
    temp= image_path + '/%s.jpg' % x
    print u'正在下载第%s张图片' % x
    try:
      urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp)
    except:
      print u"该图片下载失败:%s"%imgurl
    x+=1

print u'原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path)