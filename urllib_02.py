__author__ = 'zhaoxingchun'
#coding=utf-8
#
#抓取证券之星的股票数据
#
import urllib2
import re
import time
import random
import MySQLdb
import datetime

def getHtml(url):
    #抓取所需内容
    user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    #headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64)"}  #伪装浏览器请求报头
    request=urllib2.Request(url=url,headers={"User-Agent":random.choice(user_agent)})  #请求服务器
    response=urllib2.urlopen(request)  #服务器应答
    content=response.read()           #以一定的编码方式查看源码
    #print(content)  #打印页面源码
    return content

def getMsg(html):
    pattern=re.compile('<tbody[\s\S]*</tbody>')
    body=re.findall(pattern,str(html))   #匹配<tbody和</tbody>之间的所有代码
    pattern=re.compile('>(.*?)<')

    stock_total=[]                          #stock_total：所有页面的股票数据 stock_page：某页的股票数据
    stock_page=re.findall(pattern,body[0])  #匹配>和<之间的所有信息
    stock_total.extend(stock_page)
    time.sleep(random.randrange(1,4))       #每抓一页随机休眠几秒，数值可根据实际情况改动
    # #删除空白字符
    stock_last=stock_total[:]               #stock_total：匹配出的股票数据

    for data in stock_total:               #stock_last：整理后的股票数据
        if data=='':
            stock_last.remove('')

    # for k in range(0,len(stock_last),13):
    #     stock_last[k+1] = stock_last[k+1]
    #打印部分结果
    #print "代码",'\t','最新价','\t','涨跌幅','\t','涨跌额','\t','5分钟涨幅','\t','换手率','\t','振幅','\t','量比','\t','委比','\t','市盈率'
    #print("代码\t简称\t最新价\t涨跌幅\t涨跌额\t5分钟涨幅")

    # for i in range(0,len(stock_last),13):        #网页总共有13列数据
    #     print stock_last[i],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'   ','\t',stock_last[i+8],'\t',stock_last[i+9],'\t',stock_last[i+10],'\t',stock_last[i+11],'\t',stock_last[i+12],'\t'

    for i in range(0,len(stock_last),13):        #网页总共有13列数据
        #print(type(stock_last[i+12]))
        #print i
        #if(((stock_last[i+10] >=1 and stock_last[i+10]<=10) and stock_last[i+11]>1) and stock_last[i+12]<300):
        #if(float(stock_last[i+10]) >= 2 and float(stock_last[i+11]) > 0):
        if (float(stock_last[i+10]) > 2.5 and float(stock_last[i+11]) > 0.3):


        #if (stock_last[i] == '000858'):
            print stock_last[i],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'   ','\t',stock_last[i+8],'\t',stock_last[i+9],'\t',stock_last[i+10],'\t',stock_last[i+11],'\t',stock_last[i+12],'\t'
        #print stock_last[i],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'   ','\t',stock_last[i+8],'\t',stock_last[i+9],'\t',stock_last[i+10],'\t',stock_last[i+11],'\t',stock_last[i+12],'\t'

    return stock_last

def printCode(stock_last):
    for i in range(0,len(stock_last),13):        #网页总共有13列数据
        print(stock_last[i],'\t',u'stock_last[i+1]'.decode('utf-8'),'\t','\t','\t',stock_last[i+2],'  ','\t',stock_last[i+3],'  ','\t',stock_last[i+4],'  ','\t',stock_last[i+5])

def saveDB(stock_last):
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

    for i in range(0, len(stock_last),13):
        sql = "INSERT INTO SHARES(SHARES_NAME,SHARES_CODE, NEW_PRICES, CHG,\
            FLUCTUATION,TURNOVER_RATE,SWING,LMR,COMMITTEE,PE,CREATE_TIME)\
        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (stock_last[i+1],stock_last[i],
            stock_last[i+2],stock_last[i+3],stock_last[i+5],stock_last[i+8],stock_last[i+9],
            stock_last[i+10],stock_last[i+11],stock_last[i+12],dt)
        try:
            #使用execute方法执行sql语句
            #print sql
            #print "执行插入"
            #print stock_last[i],'\t',stock_last[i+2],'\t',stock_last[i+3],'\t',stock_last[i+4],'\t',stock_last[i+5],'   ','\t',stock_last[i+8],'\t',stock_last[i+9],'\t',stock_last[i+10],'\t',stock_last[i+11],'\t',stock_last[i+12],'\t'
            if (float(stock_last[i+10]) > 2 and float(stock_last[i+11]) > 0.0):
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
    print "代码",'\t','最新价','\t','涨跌幅','\t','涨跌额','\t','5分钟涨幅','\t','换手率','\t','振幅','\t','量比','\t','委比','\t','市盈率'
    for page in range(1,109):
        #print page
        url='http://quote.stockstar.com/stock/ranklist_a_3_1_'+str(page)+'.html'
        html = getHtml(url)
        #getMsg(html)
        saveDB(getMsg(html))