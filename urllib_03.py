__author__ = 'zhaoxingchun'
#coding=utf-8
#
# 抓取彩票数据
#

import urllib
import urllib2
import re
import time
import random
import MySQLdb
import datetime

def getHtml(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent':user_agent}

    resquestMsg = urllib2.Request(url=url,headers=headers)
    responseMsg = urllib2.urlopen(resquestMsg)
    content = responseMsg.read()
    return content

def getContent(Html):
    pattern = re.compile('<tbody[\s\S]*</tbody>')
    body = re.findall(pattern,str(Html))
    pattern=re.compile('>(.*?)<')

    stock_total=[]                          #stock_total：所有页面的股票数据 stock_page：某页的股票数据
    stock_page=re.findall(pattern,body[0])  #匹配>和<之间的所有信息
    stock_total.extend(stock_page)
    # time.sleep(random.randrange(1,4))       #每抓一页随机休眠几秒，数值可根据实际情况改动
    #
    #  # #删除空白字符
    stock_last=stock_total[:]               #stock_total：匹配出的股票数据

    for data in stock_total:               #stock_last：整理后的股票数据
        if data=='':
            stock_last.remove('')
    #print len(stock_last)
    x= 1
    for i in range(0,2800,14):
        #print ("第%s行" % x)
        print stock_last[i],"\t",stock_last[i+1],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'\t',stock_last[i+6],'\t',stock_last[i+7],'\t',stock_last[i+8],stock_last[i+9]
        x += 1

    A = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33']
    Total_A = [0]*33
    print 'A'
    print A
    for l in range(0,len(A)):
        for k in range(0,1400,14):
            if A[l] in [stock_last[k+2],stock_last[k+3],stock_last[k+4],stock_last[k+5],stock_last[k+6],stock_last[k+7],stock_last[k+8]]:
                Total_A[int(A[l])-1] += 1

    print "Total_A"
    print Total_A
    print('\033[1;31;40m')
    print "A:Total_A"
    #print dict(zip(A,Total_A))
    dicA = sorted(dict(zip(A,Total_A)).iteritems(),key=lambda asd:asd[1],reverse=False)
    #print dic
    for h in range(0,33,1):
        print dicA[h]
    #print dic[10]
    print('\033[0m')


    B = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
    print 'B'
    print B
    Total_B=[0]*16
    #print len(Total_B)


    for n in range(0,len(B)):
        for m in range(0,1400,14):
            if int( B[n]) == int(stock_last[m+9]):
                Total_B[int(B[n])-1] += 1

    # for n in range(0,len(B)):
    #     if B[n] in stock_last:
    #         Total_B[int(B[n])] += 1

    print "Total_B"
    print Total_B

    print('\033[1;31;40m')
    print "B:Total_B"
    dicB = sorted(dict(zip(B,Total_B)).iteritems(),key=lambda asd:asd[1],reverse=False)
    #print dicB
    for h in range(0,16,1):
        print dicB[h]
    #print dic[10]
    print('\033[0m')
    return stock_last


def saveNum(stock_last):
    host = "localhost"
    name = "root"
    password = "password"
    dbname = "csvt"

    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #打开数据库库
    db = MySQLdb.connect(host,name,password,dbname)
    #print "数据库连接成功"
    # sql = """INSERT INTO SHARES(SHARES_NAME,SHARES_CODE, NEW_PRICES, CHG,
    #         FLUCTUATION,5_MINUTE_GAIN,TURNOVER_RATE,SWING,LMR,COMMITTEE,PE)
    #      VALUES (stock_last[i], stock_last[i+1], stock_last[i+2], stock_last[i+3],
    #             stock_last[i+4],stock_last[i+5],stock_last[i+8],stock_last[i+9],
    #             stock_last[i+10],stock_last[i+11],stock_last[i+12])"""

    #使用cursor()方法获取操作游标
    cursor = db.cursor()

    for i in range(0, 2800,14):
        sql = "INSERT INTO EXCEL(ISSUE,EXCEL_DATE,RED_ONE,RED_TWO,RED_THREE,RED_FOUR,RED_FIVE,RED_SIX,BLUE)\
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (stock_last[i],stock_last[i+1],
            stock_last[i+2],stock_last[i+3],stock_last[i+4],stock_last[i+5],stock_last[i+6],
            stock_last[i+7],stock_last[i+9])
        try:
            #使用execute方法执行sql语句
            #print sql
            #print "执行插入"
            #print stock_last[i],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'   ','\t',stock_last[i+8],'\t',stock_last[i+9],'\t',stock_last[i+10],'\t',stock_last[i+11],'\t',stock_last[i+12],'\t'
            #if (float(stock_last[i+10]) > 2 and float(stock_last[i+11]) > 0.0):

                cursor.execute(sql)
                #提交到数据库执行
                db.commit()
            #print "数据提交成功"
        except:
            # Rollback in case there is any error
            print "插入错误"
            print db.error()
            db.rollback()

    #关闭数据库连接
    db.close()
    return

if __name__ ==  '__main__':
    print "期号","\t\t","日期","\t\t\t\t","红色开奖号码","\t\t\t\t\t\t\t","蓝色开奖号码"
    #url = 'http://baidu.lecai.com/lottery/draw/list/50?type=latest&num=100'
    url ='http://baidu.lecai.com/lottery/draw/list/50?type=range&start=2014160&end=2017090'
    html = getHtml(url)
    getContent(html)
    #saveNum(getContent(html))





