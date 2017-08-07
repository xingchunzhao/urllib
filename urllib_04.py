__author__ = 'zhaoxingchun'
#coding=utf-8
#
#抓取文章
#

import urllib
import re
import os
import glob

#获取html
def getHtml(url):

    response = urllib.urlopen(url)
    html = response.read()
    return html

#获取html信息
def getMsg(html):

    Msg = re.compile('<a class="title" target="_blank" href="(.*?)">(.*?)</a>')
    MsgList = re.findall(Msg,html)
    #Title = re.compile('<a class="title" target="_blank" href="(.*?)">(.*?)</a>')
    #TitleList = re.findall(Title,html)
    #print MsgList
    #print TitleList
    return MsgList
    # for Msg in MsgList:
    #     Msg = url + MsgList
    #     print Msg

def makeFile(MsgList,filename):
    for i in range(0,len(MsgList),1):
        filename = 'F:\SoftwareSetup\AutoTest\Project\Test_Try1\urllib\Note\\' + MsgList[i][0][3:] + '.html'
        if os.path.exists(filename) == False:
            os.mkdir(filename)
        os.chdir(filename)

#保存文章
def saveMsg(url,MsgList):
    for i in range(0,len(MsgList),1):
        print "标题：",MsgList[i][1]
        MsgUrl = url + MsgList[i][0]
        print "链接：",MsgUrl
        response = urllib.urlopen(MsgUrl).read()
        filename = MsgList[i][1].decode('utf-8') + '.html'
        #filename1 = MsgList[i][0][3:]+ '.html'
        # if os.path.exists(filename) == False:
        #      os.mkdir(filename)
        # os.chdir(filename)
        f = open(filename.replace('|', '_'),'w+')
        a = ['/','\\','*','?','|','<','>']
        f = open(filename,'w+')

        #a = glob.glob('*')
        f.writelines(response)
        f.close()

    return


if __name__=='__main__':
    url = 'http://www.jianshu.com/'
    html = getHtml(url)
    MsgList = getMsg(html)
    #print MsgList
    #makeFile(MsgList,'Note')
    saveMsg(url,MsgList)




