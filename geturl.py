# -*- coding:utf-8 -*-
import urllib2
import re

import time
import MySQLdb
import chardet
import sys
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')


list_page = range(1,1191)

for page_num in list_page:
    if page_num == 1:
        # 第一页
        url = "http://www.myexception.cn/php/index.html"
    else:
        url = "http://www.myexception.cn/php/index_%s.html"%page_num
    try:
        print "正在打开url:"+url
        page = urllib2.urlopen(url,timeout=1)
        list_html = page.read()
        print "已打开"
    except:
        list_page.append(page_num)
        print "打开url:"+url+"失败,已重新追加到写入list_page"
        continue
    # 列表页的html
    list_url = re.findall("<li><a href=\"([\s\S]*?)\" target", list_html)
    del list_url[0]
    list_error = {}
    for one in list_url:
        #第一扁文章
        try:
            print "正在打开地址"+one
            one_html = urllib2.urlopen(one,timeout=1).read()
            print "已打开"
            title = re.search("<h1>(.*?)<\/h1>",one_html).group(1)
        except:
            # 如果请求失败，重新加入列表
            m2 = hashlib.md5()
            m2.update(one)
            key = m2.hexdigest()

            #记录出错误次数
            number = list_error.get(key,0)
            if number>3:
                print "url:"+one+"出现三次失败，跳过"
                #出错次数超过三次，直接跳过
                continue
            #不超过三次继续追加
            list_error[key] = number+1

            list_url.append(one)
            print "url:"+one+" 读取失败，重新加入列表"
            continue

        keywords = re.search("<meta name=\"keywords\" content=\"(.*?)\"",one_html).group(1)
        description = re.search("<meta name=\"description\" content=\"(.*?)\"", one_html).group(1)
        content = re.search("<div class=\"c_txt\">([\s\S]*?)<\/div><div class=\"c_a_4\">",one_html).group(1)
        transshipment = one
        pub_date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        sql = "insert into article_article(title,keywords,description,content,pub_date,update_time,transshipment) value ('%s','%s','%s','%s','%s','%s','%s')"%(\
            MySQLdb.escape_string(title),\
            MySQLdb.escape_string(keywords),\
            MySQLdb.escape_string(description),\
            MySQLdb.escape_string(content),pub_date,update_time,\
            MySQLdb.escape_string(transshipment))

        #入库

        try:
            db = MySQLdb.connect("127.0.0.1", "root", "root", "boke", charset="utf8")
            cursor = db.cursor()

            cursor.execute(sql)
            article_id = cursor.lastrowid
            column_id = 5
            sql2 = "insert into  article_article_column(article_id,column_id) value('%s','%s')"%(article_id,column_id)
            cursor.execute(sql2)
            print "insert data success"
            db.commit()
            db.close()
        except:
            print "insert data error"
            print sql
            print sql2
            exit()

