from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader

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

def naver_key_select_movie(query):
    conn, cur = open_db()
    sql = """select * from movie where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()

    t = (r['mid'], r['naver_key'], r['kr_title'], r['eng_title'], r['audience_rate'],
            r['audience_count'], r['netizen_rate'], r['netizen_count'], r['journalist_score'], r['journalist_count'],
            r['playing_time'], r['opening_date'], r['summary'], r['movie_rate'], r['main_image'])

    close_db(conn, cur)
    
    return t

def naver_key_select_scope(query):
    conn, cur = open_db()
    sql = """select * from scope where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['scope_str'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    
    my_set = set(list)
    return my_set

def naver_key_select_country(query):
    conn, cur = open_db()
    sql = """select * from country where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['country_str'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_photo(query):
    conn, cur = open_db()
    sql = """select * from photo where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['link'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_video(query):
    conn, cur = open_db()
    sql = """select * from video where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['image'], r['link'], r['title'], r['video_date'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_user_rate(query):
    conn, cur = open_db()
    sql = """select * from user_rate where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['rate'], r['contents'], r['writer'], r['good'], r['bad'], r['user_rate_date'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_journalist_rate(query):
    conn, cur = open_db()
    sql = """select * from journalist_rate where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['writer_image'], r['writer'], r['title'], r['rate'], r['contents'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_famous_line(query):
    conn, cur = open_db()
    sql = """select * from famous_line where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['role_image'], r['contents'], r['role_name'], r['actor'], r['writer'], r['famous_line_date'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_user_review(query):
    conn, cur = open_db()
    sql = """select * from review where naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['naver_r_key'], r['rate'], r['title'], r['review_date'], r['writer'], r['views'], r['star'], r['contents'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_comments(query):
    conn, cur = open_db()
    sql = """select * from comments where naver_r_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['writer'], r['contents'], r['comment_date'], r['good'], r['bad'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set
    

def naver_key_select_director(query):
    conn, cur = open_db()
    sql = """select d.kr_name, d.eng_name, d.image
            from movie_director md, director d
            where md.did = d.did and md.naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['kr_name'], r['eng_name'], r['image'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def naver_key_select_actor(query):
    conn, cur = open_db()
    sql = """select a.kr_name, a.eng_name, a.image, mr.main_or_support, mr.role_name
            from movie_role mr, actor a
            where mr.aid = a.aid and mr.naver_key = %d;
         """ %(query)
    cur.execute(sql)

    r = cur.fetchone()
    list = []
    while r:
        t = (r['kr_name'], r['eng_name'], r['image'], r['main_or_support'], r['role_name'])
        list.append(t)
        r = cur.fetchone()

    close_db(conn, cur)
    my_set = set(list)
    return my_set

def simple_select(query):
    conn, cur = open_db()
    sql = """select * from movie where kr_title like "%s";
         """ %(query+'%')
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

def search(request):
    q = request.POST.get('query_str', '')
    lists = simple_select(q)

    template = loader.get_template('home/search_result.html')
    context = {
        'lists': lists,
    }

    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('home/home.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))

def movie_detail(request, id):
    movie = naver_key_select_movie(id)
    scope = naver_key_select_scope(id)
    country = naver_key_select_country(id)
    director = naver_key_select_director(id)
    actor = naver_key_select_actor(id)
    photo = naver_key_select_photo(id)
    video = naver_key_select_video(id)
    user_rate = naver_key_select_user_rate(id)
    review = naver_key_select_user_review(id)
    journalist_rate = naver_key_select_journalist_rate(id)
    famous_line = naver_key_select_famous_line(id)

    template = loader.get_template('home/movie_detail.html')
    context = {
        'movie': movie,
        'scope': scope,
        'country': country,
        'director': director,
        # 'actor': actor,
        'photo': photo,
        'video': video,
        'user_rate': user_rate,
        'review': review,
        'journalist_rate': journalist_rate,
        'famous_line': famous_line,
        'actor': actor,
    }
    return HttpResponse(template.render(context, request))

def comments(request, id):
    comments = naver_key_select_comments(id)

    template = loader.get_template('home/comments.html')
    context = {
        'comments': comments,
    }
    return HttpResponse(template.render(context, request))
