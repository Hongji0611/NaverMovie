from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import pymysql

def open_db():
    pw = getattr(settings, 'PASSWORD', 'localhost')
    conn = pymysql.connect(host='localhost', user='db2022', 
            password=pw, db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def simple_select():
    conn, cur = open_db()
    sql = """select * from movie where kr_title like "형%";
         """
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['mid'], r['naver_key'], r['kr_title'], r['eng_title'], r['audience_rate'],
                r['audience_count'], r['netizen_rate'], r['netizen_count'], r['journalist_score'], r['journalist_count'],
                r['playing_time'], r['opening_date'], r['summary'], r['movie_rate'], r['main_image'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    
    return list

def index(request):
    lists = simple_select()
    return HttpResponse(lists)