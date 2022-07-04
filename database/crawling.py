from bs4 import BeautifulSoup
import pymysql
from selenium import webdriver
import time

driver = webdriver.Firefox(
    executable_path='/Users/geckodriver.exe')
driver.implicitly_wait(3)

movie_buffer = []
movie_role_buffer = []
movie_director_buffer = []

scope_buffer = []
country_buffer = []
photo_buffer = []
video_buffer = []
famous_line_buffer = []
user_rate_buffer = []
journalist_rate_buffer = []

review_buffer = []
comments_buffer = []


def open_db():
    conn = pymysql.connect(host='localhost', user='user',
                           password='password', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    return conn, cur


def close_db(conn, cur):
    cur.close()
    conn.close()


def insert_review_comments(naver_key, url):
    global review_buffer
    global comments_buffer

    review_conn, review_cur = open_db()
    insert_review_sql = """insert ignore into review(naver_r_key, naver_key, rate, title, review_date,
                            original_link, writer, views, star, contents)
                                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ul = soup.select_one(".rvw_list_area")
    if ul == None:
        return
    lis = ul.find_all("li")

    review_url = "https://movie.naver.com/movie/bi/mi/reviewread.naver?code="+naver_key
    for li in lis:
        nid = li.find("a")["onclick"].replace(
            "clickcr(this, 'rli.title', '', '', event); showReviewDetail(", "").replace(")", "")
        custom_review_url = review_url + "&nid="+nid
        driver.get(custom_review_url)
        time.sleep(0.3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #Review
        review = {}
        review["naver_r_key"] = nid
        review["naver_key"] = naver_key

        div = soup.select_one(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior > div")
        if div == None:
            review["rate"] = None
        else:
            ems = div.find_all("em")
            review["rate"] = ""
            for em in ems:
                review["rate"] = review["rate"] + em.text

        review["title"] = soup.find("strong", class_="h_lst_tx")
        if review["title"] != None:
            review["title"] = review["title"].text
        review["review_date"] = soup.select_one(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior > span")
        if review["review_date"] != None:
            review["review_date"] = review["review_date"].text
        review["original_link"] = soup.select_one(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > ul > li:nth-child(1) > a")
        if review["original_link"] != None:
            review["original_link"] = review["original_link"]["href"]
        review["writer"] = soup.select_one(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > ul > li:nth-child(2) > a > em")
        if review["writer"] == None:
            review["writer"] = soup.select_one(
                "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > ul > li > a > em")
            if review["writer"] == None:
                continue
            else:
                review["writer"] = review["writer"].text
        else:
            review["writer"] = review["writer"].text

        review["views"] = soup.select_one(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > div > span:nth-child(1) > em")
        if review["views"] != None:
            review["views"] = review["views"].text
        review["star"] = soup.select_one("#goodReviewCount")
        if review["star"] != None:
            review["star"] = review["star"].text

        ps = soup.select(
            "#content > div.article > div.obj_section.noline.center_obj > div.review > div.user_tx_area")
        contents = ""

        for p in ps:
            contents = contents + \
                p.text.replace("\n", " ").replace(
                    "\xa0", "").replace("\xa06", "")
            if len(contents) > 500:
                break
        review["contents"] = contents

        t = (review["naver_r_key"], review["naver_key"], review["rate"], review["title"], review["review_date"], review["original_link"],
             review["writer"], review["views"], review["star"], review["contents"])

        review_cur.execute(insert_review_sql, t)
        review_conn.commit()

        #Comments
        ul = soup.select_one(
            "#cbox_module_wai_u_cbox_content_wrap_tabpanel > ul")

        if ul == None:
            continue
        else:
            lis = ul.find_all("li")
            for li in lis:
                comments = {}
                comments["naver_r_key"] = nid
                comments["writer"] = li.find("span", class_="u_cbox_nick")
                if comments["writer"] == None:
                    continue
                else:
                    comments["writer"] = comments["writer"].text
                comments["contents"] = li.find(
                    "span", class_="u_cbox_contents").text
                comments["comment_date"] = li.find( 
                    "span", class_="u_cbox_date").text
                comments["good"] = li.find(
                    "em", class_="u_cbox_cnt_recomm").text
                comments["bad"] = li.find(
                    "em", class_="u_cbox_cnt_unrecomm").text

                c_tupple = (comments["naver_r_key"], comments["writer"], comments["contents"],
                            comments["comment_date"], comments["good"], comments["bad"])

                comments_buffer.append(c_tupple)
    close_db(review_conn, review_cur)


def insert_famous_line(naver_key, url):
    global famous_line_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ul = soup.select_one("#iframeDiv > ul")
    if ul == None:
        return
    lis = ul.find_all("li")

    for li in lis:
        famous_line = {}
        famous_line["naver_key"] = naver_key
        famous_line["role_image"] = li.find("img").get("src")
        famous_line["contents"] = li.find("p", class_="one_line").text
        famous_line["role_name"] = li.select_one("div > p.char_part > span")
        if famous_line["role_name"] != None:
            famous_line["role_name"] = famous_line["role_name"].text
        famous_line["actor"] = li.select_one("div > p.char_part > a")
        if famous_line["actor"] == None:
            famous_line["actor"] = li.select_one("div > p:nth-child(2) > a").text
        else:
            famous_line["actor"] = famous_line["actor"].text
        famous_line["writer"] = li.select_one("div > p.etc_lines > span:nth-child(1) > a").text
        famous_line["famous_line_date"] = li.find("em", class_="date").text

        t = (famous_line["naver_key"], famous_line["role_image"], famous_line["contents"], famous_line["role_name"], famous_line["actor"],
                famous_line["writer"], famous_line["famous_line_date"])

        famous_line_buffer.append(t)

def insert_user_rate_journalist_rate(naver_key, url):
    global user_rate_buffer
    global journalist_rate_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #Journalist_rate
    ul = soup.select_one(
        "#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.reporter > ul")
    if ul != None:
        lis = ul.find_all("li")
        for li in lis:
            journalist_rate = {}

            journalist_rate["naver_key"] = naver_key
            journalist_rate["writer_image"] = li.select_one(
                "div.reporter_line > p > a > img").get("src")
            journalist_rate["writer"] = li.select_one(
                "div.reporter_line > dl > dt > a").text
            journalist_rate["title"] = li.select_one(
                "div.reporter_line > dl > dd").text
            journalist_rate["rate"] = li.select_one(
                "div.re_score_grp > div > div > em").text
            journalist_rate["contents"] = li.find("p", class_="tx_report").text.replace(
                '"', "").replace("\n", "").replace("\t", "")

            t = (journalist_rate["naver_key"], journalist_rate["writer_image"], journalist_rate["writer"],
                 journalist_rate["title"], journalist_rate["rate"], journalist_rate["contents"])

            journalist_rate_buffer.append(t)

    driver.switch_to.frame("pointAfterListIframe")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #User_rate
    ul = soup.select_one("body > div > div > div.score_result > ul")
    if ul == None:
        return
    lis = ul.find_all("li")
    for li in lis:
        user_rate = {}

        user_rate["naver_key"] = naver_key
        user_rate["rate"] = li.select_one("div.star_score > em").text
        user_rate["contents"] = li.select_one(
            "div.score_reple > p > span:nth-child(2)")
        if user_rate["contents"] == None:
            user_rate["contents"] = li.select_one(
                "div.score_reple > p > span:nth-child(1)").text.replace("\n", "").replace("\t", "")
        else:
            user_rate["contents"] = user_rate["contents"].text.replace(
                "\n", "").replace("\t", "")
        user_rate["writer"] = li.select_one(
            "div.score_reple > dl > dt > em:nth-child(1) > a > span").text
        user_rate["good"] = li.select_one(
            "div.btn_area > a._sympathyButton > strong").text
        user_rate["bad"] = li.select_one(
            "div.btn_area > a._notSympathyButton > strong").text
        user_rate["user_rate_date"] = li.select_one(
            "div.score_reple > dl > dt > em:nth-child(2)").text

        t = (user_rate["naver_key"], user_rate["rate"], user_rate["contents"], user_rate["writer"], user_rate["good"],
             user_rate["bad"], user_rate["user_rate_date"])

        user_rate_buffer.append(t)


def insert_video(naver_key, url):
    global video_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    uls = soup.select("ul.video_thumb")
    for ul in uls:
        lis = ul.find_all("li")

        for li in lis:
            video = {}
            video["naver_key"] = naver_key
            video["image"] = li.find("img").get("src")
            video["link"] = "https://movie.naver.com/" + \
                li.find("a", class_="video_obj")["href"]
            video["title"] = li.select_one("p.tx_video.ico > a").text
            video["video_date"] = li.find("p", class_="video_date").text

            t = (video["naver_key"], video["image"], video["link"],
                 video["title"], video["video_date"])

            video_buffer.append(t)


def insert_photo(naver_key, url):
    global photo_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ul = soup.select_one("#gallery_group")
    if ul == None:
        return
    lis = ul.find_all("li")

    for li in lis:
        photo = {}
        photo["naver_key"] = naver_key
        photo["link"] = li.find("img").get("src")

        t = (photo["naver_key"], photo["link"])

        photo_buffer.append(t)

def insert_scope_country(naver_key, url):
    global scope_buffer
    global country_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #Scope
    span = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1)")
    if span == None:
        return
    a_tags = span.find_all("a")

    for a in a_tags:
        scope = {}
        scope["naver_key"] = naver_key
        scope["scope_str"] = a.text

        t = (scope["naver_key"], scope["scope_str"])

        scope_buffer.append(t)

    #Scope
    span2 = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(2)")
    if span2 == None:
        return
    a2_tags = span2.find_all("a")

    for a in a2_tags:
        country = {}
        country["naver_key"] = naver_key
        country["country_str"] = a.text

        t = (country["naver_key"], country["country_str"])

        country_buffer.append(t)


def insert_actor_director(naver_key, url):
    global movie_role_buffer
    global movie_director_buffer

    #Actor
    actor_conn, actor_cur = open_db()
    insert_actor_sql = """insert ignore into actor(kr_name, eng_name, image)
                        values(%s, %s, %s)"""
    select_actor_aid = """select max(aid) as aid from actor"""

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ul = soup.select_one(
        "#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul")
    if ul == None:
        return
    lis = ul.find_all("li")

    for li in lis:
        actor = {}
        actor["kr_name"] = li.find("a", class_="k_name")
        if actor["kr_name"] == None:
            continue
        else:
            actor["kr_name"] = actor["kr_name"].text
        actor["eng_name"] = li.find("em", class_="e_name").text
        actor["image"] = li.find("p", class_="p_thumb").find("img").get("src")

        t = (actor["kr_name"], actor["eng_name"], actor["image"])

        actor_cur.execute(insert_actor_sql, t)
        actor_conn.commit()

        movie_role = {}
        movie_role["naver_key"] = naver_key

        aid_conn, aid_cur = open_db()
        aid_cur.execute(select_actor_aid)

        r = aid_cur.fetchone()
        movie_role["aid"] = r['aid']
        movie_role["main_or_support"] = li.find("em", class_="p_part").text
        movie_role["role_name"] = li.find("p", class_="pe_cmt")
        if movie_role["role_name"] != None:
            movie_role["role_name"] = movie_role["role_name"].find(
                "span").text.replace(" 역", "")

        tr = (movie_role["naver_key"], movie_role["aid"],
              movie_role["main_or_support"], movie_role["role_name"])
        movie_role_buffer.append(tr)
        close_db(aid_conn, aid_cur)

    #Director
    director_conn, director_cur = open_db()
    insert_director_sql = """insert ignore into director(kr_name, eng_name, image)
                        values(%s, %s, %s)"""
    select_director_did = """select max(did) as did from director"""

    div = soup.select_one(
        "#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div")
    if div == None:
        return
    objs = div.find_all("div", class_="dir_obj")

    for obj in objs:
        director = {}
        director["kr_name"] = obj.find("a", class_="k_name")
        if director["kr_name"] == None:
            continue
        else:
            director["kr_name"] = director["kr_name"].text
        director["eng_name"] = obj.find("em", class_="e_name").text
        if director["eng_name"] == "":
            director["eng_name"] = None
        director["image"] = obj.find(
            "p", class_="thumb_dir").find("img").get("src")

        t = (director["kr_name"], director["eng_name"], director["image"])

        director_cur.execute(insert_director_sql, t)
        director_conn.commit()

        movie_director = {}
        movie_director["naver_key"] = naver_key

        did_conn, did_cur = open_db()
        did_cur.execute(select_director_did)

        r = did_cur.fetchone()
        movie_director["did"] = r['did']

        tr = (movie_director["naver_key"], movie_director["did"])
        movie_director_buffer.append(tr)
        close_db(did_conn, did_cur)

    close_db(director_conn, director_cur)
    close_db(actor_conn, actor_cur)


def insert_movie(url):
    global movie_buffer

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    movie = {}

    movie["naver_key"] = url.split("=")[-1]
    movie["kr_title"] = soup.find("h3", class_="h_movie")

    if movie["kr_title"] == None:
        return -1
    else:
        movie["kr_title"] = movie["kr_title"].find("a").text

    movie["eng_title"] = soup.find("strong", class_="h_movie2").text.split(",")[
        0].replace('\t', "").replace('\n', "")

    audience_rate_list = soup.find("div", class_="star_score").find_all("em")
    audience_rate = ""
    for rate in audience_rate_list:
        audience_rate += rate.text

    if audience_rate == "":
        movie["audience_rate"] = None
    else:
        movie["audience_rate"] = audience_rate

    movie["audience_count"] = soup.find(
        "div", class_="ly_count", id="actualPointCountBasic")
    if movie["audience_count"] != None:
        movie["audience_count"].find("em").text.replace(",", "")

    netizen_rate = ""
    netizen_rate_list = soup.find("a", id="pointNetizenPersentBasic")
    if netizen_rate_list != None:
        netizen_rate_list.find_all("em")

        for rate in netizen_rate_list:
            netizen_rate += rate.text

    if netizen_rate == "":
        movie["netizen_rate"] = None
    else:
        movie["netizen_rate"] = netizen_rate

    movie["netizen_count"] = soup.find(
        "div", class_="ly_count", id="pointNetizenCountBasic")
    if movie["netizen_count"] != None:
        movie["netizen_count"] = movie["netizen_count"].find(
            "em").text.replace(",", "")

    journalist_score = ""
    journalist_score_list = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div")
    if journalist_score_list == None:
        journalist_score = None
    else:
        journalist_score_list.find_all("em")
        for score in journalist_score_list:
            journalist_score += score.text.replace('\n', "")
    movie["journalist_score"] = journalist_score

    movie["journalist_count"] = soup.select_one(
        "#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.special_score > div > span > em")
    if movie["journalist_count"] != None:
        movie["journalist_count"] = movie["journalist_count"].text
    movie["playing_time"] = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)")
    if movie["playing_time"] != None:
        movie["playing_time"] = movie["playing_time"].text.strip().replace("분", "")

    year = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(1)")
    if year != None:
        year = year.text.strip()

    date = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(2)")
    if date != None:
        date = date.text.strip()

    if year == None and date == None:
        movie["opening_date"] = None
    else:
        movie["opening_date"] = (str(year) + str(date)).replace(".", "-")
    movie["summary"] = soup.select_one(
        "#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p")
    if  movie["summary"] != None:
        movie["summary"] = movie["summary"].text.replace("\xa0", " ").replace("\n", "")
    movie["movie_rate"] = soup.select_one(
        "#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a")
    if movie["movie_rate"] != None:
        movie["movie_rate"] = movie["movie_rate"].text
    else:
        movie["movie_rate"] = None
    movie["main_image"] = soup.select_one(
        "#content > div.article > div.mv_info_area > div.poster > a > img")
    if movie["main_image"] != None:
        movie["main_image"] = movie["main_image"].get("src")
    else:
        movie["main_image"] = None

    print(movie['kr_title'])
    t = (movie['naver_key'], movie['kr_title'], movie['eng_title'], movie['audience_rate'], movie['audience_count'],
         movie['netizen_rate'], movie['netizen_count'], movie['journalist_score'], movie['journalist_count'], movie['playing_time'],
         movie['opening_date'], movie['summary'], movie['movie_rate'], movie['main_image'])

    movie_buffer.append(t)

    return movie['naver_key']


def crawling():
    global movie_buffer
    global movie_role_buffer
    global movie_director_buffer
    global scope_buffer
    global country_buffer
    global photo_buffer
    global video_buffer
    global review_buffer
    global comments_buffer
    global famous_line_buffer
    global user_rate_buffer
    global journalist_rate_buffer

    movie_conn, movie_cur = open_db()
    insert_movie_sql = """insert ignore into movie(naver_key, kr_title, eng_title, audience_rate, audience_count,
                        netizen_rate, netizen_count, journalist_score, journalist_count, playing_time,
                        opening_date, summary, movie_rate, main_image)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    movie_role_conn, movie_role_cur = open_db()
    insert_movie_role_sql = """insert ignore into movie_role(naver_key, aid, main_or_support, role_name)
                        values(%s, %s, %s, %s)"""

    movie_director_conn, movie_director_cur = open_db()
    insert_movie_director_sql = """insert ignore into movie_director(naver_key, did)
                        values(%s, %s)"""

    scope_conn, scope_cur = open_db()
    insert_scope_sql = """insert ignore into scope(naver_key, scope_str)
                        values(%s, %s)"""

    country_conn, country_cur = open_db()
    insert_country_sql = """insert ignore into country(naver_key, country_str)
                        values(%s, %s)"""

    photo_conn, photo_cur = open_db()
    insert_photo_sql = """insert ignore into photo(naver_key, link)
                        values(%s, %s)"""

    video_conn, video_cur = open_db()
    insert_video_sql = """insert ignore into video(naver_key, image, link, title, video_date)
                        values(%s, %s, %s, %s, %s)"""

    review_conn, review_cur = open_db()
    insert_review_sql = """insert ignore into review(naver_r_key, naver_key, rate, title, review_date, original_link, writer, views, star, contents)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    comments_conn, comments_cur = open_db()
    insert_comments_sql = """insert ignore into comments(naver_r_key, writer, contents, comment_date, good, bad)
                        values(%s, %s, %s, %s, %s, %s)"""

    famous_line_conn, famous_line_cur = open_db()
    insert_famous_line_sql = """insert ignore into famous_line(naver_key, role_image, contents, role_name, actor, writer, famous_line_date)
                        values(%s, %s, %s, %s, %s, %s, %s)"""

    user_rate_conn, user_rate_cur = open_db()
    insert_user_rate_sql = """insert ignore into user_rate(naver_key, rate, contents, writer, good, bad, user_rate_date)
                        values(%s, %s, %s, %s, %s, %s, %s)"""

    journalist_rate_conn, journalist_rate_cur = open_db()
    insert_journalist_rate_sql = """insert ignore into journalist_rate(naver_key, writer_image, writer, title, rate, contents)
                        values(%s, %s, %s, %s, %s, %s)"""

    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?grade=1001003&page='

    for i in range(500, 691):  
        driver.get(url+str(i))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ul = soup.select_one("#old_content > ul")
        lis = ul.find_all("li", recursive= False)
        for li in lis:
            a_tag = li.find("a")["href"]
            link = "https://movie.naver.com"+a_tag

            naver_key = insert_movie(link)
            if naver_key != -1:
                origin_link = link
                insert_scope_country(naver_key, link)

                link = origin_link.replace("basic", "review")+"&page=1"
                insert_review_comments(naver_key, link)

                link = origin_link.replace("basic", "point")
                insert_user_rate_journalist_rate(naver_key, link)

                link = origin_link.replace("basic", "script")+"&page=1"
                insert_famous_line(naver_key, link)

                link = origin_link.replace("basic", "detail")
                insert_actor_director(naver_key, link)

                link = origin_link.replace("basic", "media")
                insert_video(naver_key, link)

                link = origin_link.replace(
                    "basic", "photo")+"&page=1#movieEndTabMenu"
                insert_photo(naver_key, link)

            if len(movie_buffer) // 5 >= 1:
                movie_cur.executemany(insert_movie_sql, movie_buffer)
                movie_conn.commit()
                movie_buffer = []

            if len(movie_role_buffer) // 5 >= 1:
                movie_role_cur.executemany(
                    insert_movie_role_sql, movie_role_buffer)
                movie_role_conn.commit()
                movie_role_buffer = []

            if len(movie_director_buffer) // 5 >= 1:
                movie_director_cur.executemany(
                    insert_movie_director_sql, movie_director_buffer)
                movie_director_conn.commit()
                movie_director_buffer = []

            if len(scope_buffer) // 5 >= 1:
                scope_cur.executemany(insert_scope_sql, scope_buffer)
                scope_conn.commit()
                scope_buffer = []

            if len(country_buffer) // 5 >= 1:
                country_cur.executemany(insert_country_sql, country_buffer)
                country_conn.commit()
                country_buffer = []

            if len(photo_buffer) // 5 >= 1:
                photo_cur.executemany(insert_photo_sql, photo_buffer)
                photo_conn.commit()
                photo_buffer = []

            if len(video_buffer) // 5 >= 1:
                video_cur.executemany(insert_video_sql, video_buffer)
                video_conn.commit()
                video_buffer = []

            if len(review_buffer) // 5 >= 1:
                review_cur.executemany(insert_review_sql, review_buffer)
                review_conn.commit()
                review_buffer = []

            if len(comments_buffer) // 5 >= 1:
                comments_cur.executemany(insert_comments_sql, comments_buffer)
                comments_conn.commit()
                comments_buffer = []

            if len(famous_line_buffer) // 5 >= 1:
                famous_line_cur.executemany(
                    insert_famous_line_sql, famous_line_buffer)
                famous_line_conn.commit()
                famous_line_buffer = []

            if len(user_rate_buffer) // 5 >= 1:
                user_rate_cur.executemany(
                    insert_user_rate_sql, user_rate_buffer)
                user_rate_conn.commit()
                user_rate_buffer = []

            if len(journalist_rate_buffer) // 5 >= 1:
                journalist_rate_cur.executemany(
                    insert_journalist_rate_sql, journalist_rate_buffer)
                journalist_rate_conn.commit()
                journalist_rate_buffer = []

    if movie_buffer:
        movie_cur.executemany(insert_movie_sql, movie_buffer)
        movie_conn.commit()

    if movie_role_buffer:
        movie_role_cur.executemany(insert_movie_role_sql, movie_role_buffer)
        movie_role_conn.commit()

    if movie_director_buffer:
        movie_director_cur.executemany(
            insert_movie_director_sql, movie_director_buffer)
        movie_director_conn.commit()

    if scope_buffer:
        scope_cur.executemany(insert_scope_sql, scope_buffer)
        scope_conn.commit()

    if country_buffer:
        country_cur.executemany(insert_country_sql, country_buffer)
        country_conn.commit()

    if photo_buffer:
        photo_cur.executemany(insert_photo_sql, photo_buffer)
        photo_conn.commit()

    if video_buffer:
        video_cur.executemany(insert_video_sql, video_buffer)
        video_conn.commit()

    if review_buffer:
        review_cur.executemany(insert_review_sql, review_buffer)
        review_conn.commit()

    if comments_buffer:
        comments_cur.executemany(insert_comments_sql, comments_buffer)
        comments_conn.commit()

    if famous_line_buffer:
        famous_line_cur.executemany(insert_famous_line_sql, famous_line_buffer)
        famous_line_conn.commit()

    if user_rate_buffer:
        user_rate_cur.executemany(insert_user_rate_sql, user_rate_buffer)
        user_rate_conn.commit()

    if journalist_rate_buffer:
        journalist_rate_cur.executemany(
            insert_journalist_rate_sql, journalist_rate_buffer)
        journalist_rate_conn.commit()

    close_db(movie_conn, movie_cur)
    close_db(movie_role_conn, movie_role_cur)
    close_db(movie_director_conn, movie_director_cur)
    close_db(scope_conn, scope_cur)
    close_db(country_conn, country_cur)
    close_db(photo_conn, photo_cur)
    close_db(video_conn, video_cur)
    close_db(review_conn, review_cur)
    close_db(comments_conn, comments_cur)
    close_db(famous_line_conn, famous_line_cur)
    close_db(user_rate_conn, user_rate_cur)
    close_db(journalist_rate_conn, journalist_rate_cur)


if __name__ == '__main__':
    crawling()
