__author__ = 'zhaoxingchun'
#coding=utf-8

import MySQLdb
import datetime

a = ['a','123','b','345','c','564']
print len(a)
# 打开数据库连接
db = MySQLdb.connect("localhost","root","password","csvt" )
print "数据库连接成功"

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
#sql = "SELECT * FROM LOGIN "
#sql = "INSERT INTO LOGIN (USERNAME,PASSWORD) VALUES (a[i][0],a[i][1])"
#print sql
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for i in range(0,len(a),2):
    x = a[i]
    y = a[i+1]
    print x,y
    sql = "INSERT INTO LOGIN (USERNAME,PASSWORD,CREATE_TIME) VALUES ('%s','%s','%s')" % (a[i],a[i+1],dt)
    print a[i],"\t",a[i+1]
    try:
        print sql
        # 执行SQL语句
        cursor.execute(sql)
        #cursor.execute(sql)
        print "执行查询"
        db.commit()
        print "插入成功"
    # # 获取所有记录列表
    # results = cursor.fetchall()
    # for row in results:
    #    fname = row[0]
    #    lname = row[1]
    #
    #    # 打印结果
    #    print "fname=%s,lname=%s" % \
    #           (fname, lname)
    except:
        print db.error()
        db.rollback()
    #print "Error: unable to fecth data"

# 关闭数据库连接
db.close()