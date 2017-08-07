__author__ = 'zhaoxingchun'
#coding=utf-8

#
#   简单的爬虫程序，爬取图片
#

import urllib;
import re
import glob
import os

def getHtml(url):

    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    #request = urllib2.Request(url,headers)

    response = urllib.urlopen(url)
    html = response.read()
    #print(html)
    return html

#抓取图片
def getImg(html,page):
    #reg = r'src="(.+?\.jpg)"'
    #reg = re.compile('<img pic_type="0" class="BDE_Image" style='cursor: url("http://tb2.bdstatic.com/tb/static-pb/img/cur_zin.cur"), pointer;' src="(.*?)"')
    reg = r'<img src="(.*?)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    #return imglist
    x = 0;
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,'%s.jpg' % (str(page)+str(x)))
        print("正在下载第%s张图片\n" % (str(page)+str(x)))
        x += 1
        #saveImg("img")

#保存图到相应的文件中
def saveImg(filename):
    a = glob.glob('*')
    if filename not in a:
        os.mkdir(filename)
    os.chdir(filename)


if __name__ == '__main__':
    saveImg("img")
    for page in range(1,100):
        if(page == 1):
            url = "http://www.mmjpg.com/"
        else:
             url ="http://www.mmjpg.com/home/"+str(page)
        html = getHtml(url)
        #html = getHtml("http://cl.d5j.biz/htm_mob/7/1612/2172569.html")
        getImg(html,page)
        #saveImg("img")
        #print(getImg(html))
