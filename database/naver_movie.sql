create database naver_movie;
use naver_movie;

#후보키에 UNIQUE 속성 부여하기
#strong entity: movie, actor, director
#movie에 대한 weak entity: scope, country, photo, video, review, famous_line, user_rate, journalist_rate
#review에 대한 weak entity: comments
#intersection table: movie_director
#associdation table: movie_role

#strong entity
create table movie (
	mid int auto_increment primary key,  #0
    naver_key int unique,  #1
	kr_title varchar(100), #제목  2
    eng_title varchar(100), #영문 제목  3
    audience_rate float, #관람객 평점   4
    audience_count int, #관람객 수   5
	netizen_rate float, #네티즌 평점   6
    netizen_count int, #네티즌 수    7
    journalist_score float, #기자평론가 평점   8
    journalist_count int,    #기자평론가 수    9
    playing_time int, #러닝 타임    10
    opening_date datetime, #개봉일    11
    summary varchar(800), #줄거리   12
	movie_rate varchar(50), #관람 등급    13
    main_image varchar(200), #메인 이미지    14
    
    enter_date datetime default now()
);

#strong entity
create table actor(
	aid int auto_increment primary key,
    kr_name varchar(100), #이름
    eng_name varchar(100), #영어 이름
    image varchar(200), #프로필 사진
    enter_date datetime default now()
);

#strong entity
create table director(
	did int auto_increment primary key,
    kr_name varchar(100), #이름
    eng_name varchar(100), #영어 이름
    image varchar(200), #프로필 사진
    enter_date datetime default now()
);

#associdation table (N:M)
create table movie_role(
	rid int auto_increment,
    
	naver_key int, #영화 아이디
    aid int, #배우 아이디
    main_or_support varchar(5), #주연, 조연 
    role_name varchar(100), #배역
    
    primary key (rid, naver_key, aid),
    foreign key (naver_key) references movie(naver_key),
    foreign key (aid) references actor(aid),
    enter_date datetime default now()
);

#intersection table (N:M)
create table movie_director(
	mdid int auto_increment,
    
	naver_key int, #영화 아이디
    did int, #감독 아이디
    
    primary key (mdid, naver_key, did),
    foreign key (naver_key) references movie(naver_key),
    foreign key (did) references director(did),
    enter_date datetime default now()
);

# Multivalued Attributes (weak 1:n)
create table scope( #개요
	sid int auto_increment,
    
    naver_key int not null,
    scope_str varchar(10),
    
    enter_date datetime default now(),
    
    primary key (sid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes (weak 1:n)
create table country( #국가
	cid int auto_increment,
    
    naver_key int not null,
    country_str varchar(20),
    
    enter_date datetime default now(),
    
    primary key (cid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes
create table photo( #포토
	pid int auto_increment,
    
    naver_key int not null,
    link varchar(200), 
	enter_date datetime default now(),
    
    primary key (pid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes
create table video( #동영상
	vid int auto_increment ,
    
    naver_key int not null,
    image varchar(200), #사진
    link varchar(200), #동영상 링크
    title varchar(200), #제목
    video_date datetime, #동영상 날짜
	enter_date datetime default now(),
    
    primary key (vid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes (영화와 리뷰 1:N)
create table review( #리뷰 
	rid int auto_increment,

    naver_r_key int unique,
    naver_key int not null,
    rate int, #평점
    title varchar(200), #제목
	review_date datetime, #리뷰 작성 날짜
    original_link varchar(200), #원문 링크
	writer varchar(300), #작성자
	views int, #조회수
    star int, #추천수
    contents varchar(500), #내용

	enter_date datetime default now(),
    primary key (rid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);
 
# Multivalued Attributes (리뷰와 댓글 1:N)
create table comments( #댓글
	cid int auto_increment,
    
    naver_r_key int not null,
	writer varchar(300), #작성자
    contents varchar(500), #내용
    comment_date datetime, #리뷰 작성 날짜
    good int, #곰감수
    bad int, #비공감수
    
	enter_date datetime default now(),
    
    primary key (cid, naver_r_key),
    foreign key (naver_r_key) references review(naver_r_key)
);

# Multivalued Attributes (영화와 명대사 1:N)
create table famous_line( #명대사
	fid int auto_increment,
    
    naver_key int not null,
    role_image varchar(200), #역할 이미지
    contents varchar(200), #내용
    role_name varchar(100), #역할 이름
    actor varchar(100), #배우 이름
    writer varchar(300), #작성자
    famous_line_date datetime, #명대사 작성 날짜
    
	enter_date datetime default now(),
    
    primary key (fid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes (weak 1:N)
create table user_rate( #사용자 평점
	uid int auto_increment,
    
    naver_key int not null,
	rate int, #평점
    contents varchar(200), #내용
    writer varchar(300), #작성자
    good int, #곰감수
    bad int, #비공감수
    user_rate_date datetime, #사용자 평점 작성 날짜
    
	enter_date datetime default now(),
    
    primary key (uid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

# Multivalued Attributes
create table journalist_rate( #기자 평론가 평점
	jid int auto_increment,
    
    naver_key int not null,
    writer_image varchar(300), #작성자 이미지
	writer varchar(300), #작성자
    title varchar(200), #제목
    rate int, #평점
    contents varchar(500), #내용
    
	enter_date datetime default now(),
    
    primary key (jid, naver_key),
    foreign key (naver_key) references movie(naver_key)
);

select * from movie;
select * from actor;
select * from director;

select * from scope;
select * from country;
select * from photo;
select * from video;
select * from review;
select * from famous_line;
select * from user_rate;
select * from journalist_rate;

select * from comments;

select * from movie_director;
select * from movie_role;

#검색 속성: 영화 제목, 배우 이름, 감독이름, 장르, 년도, 국가
#정렬 속성: 가나다순, 년도순, 평점순

#검색 가이드라인
# 이미 정해저있는 장르, 년도, 국가 등은 Exact match하도록 한다.
# Join Queries에 대해서는 외래키에 대한 인덱스를 만든다.
# 조건절에 있는 애트리뷰트에 대한 인덱스를 만든다.

#영화 제목으로 검색
#한국 제목
select * from movie where kr_title like "인투%";

#영어 제목
select * from movie where eng_title like "%r%";

# 배우이름으로 검색
# 한국 이름
select distinct m.*
from  actor a, movie_role r, movie m
where a.aid = r.aid and r.naver_key = m.naver_key and kr_name like "고아성";

# 영어 이름
select distinct m.*
from  actor a, movie_role r, movie m
where a.aid = r.aid and r.naver_key = m.naver_key and eng_name like "%a%";

#감독이름으로 검색
# 한국 이름
select distinct m.*
from  director d, movie_director md, movie m
where d.did = md.did and md.naver_key = m.naver_key and kr_name like "젠디 타타코브스키";

# 영어 이름
select distinct m.*
from  director d, movie_director md, movie m
where d.did = md.did and md.naver_key = m.naver_key and eng_name like "%a%";

# 장르로 검색
select distinct m.*
from  scope s, movie m
where s.naver_key = m.naver_key and s.scope_str = "드라마";

# 날짜 검색
select * from movie where DATE_FORMAT(opening_date,'%Y') = '2022';
select * from movie where DATE_FORMAT(opening_date,'%m') = '01';
select * from movie where DATE_FORMAT(opening_date,'%d') = '24';

select * from movie where DATE_FORMAT(opening_date,'%d') between '24' and '31';

# 국가 검색
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국";

# 정렬
# 가나다 순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by m.kr_title;

# 가나다 역순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by m.kr_title desc;

# 오래된 순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by year(opening_date);

# 최신 순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by year(opening_date) desc;

# 평점 높은 순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by m.audience_rate desc;

# 평점 낮은 순
select distinct m.*
from  country c, movie m
where c.naver_key = m.naver_key and c.country_str = "한국"
order by m.audience_rate;

#사진 찾기
select * from photo where naver_key = '189141';

#감독 찾기
select d.kr_name, d.eng_name, d.image
from movie_director md, director d
where md.did = d.did and md.naver_key = 192608;

#배우 찾기
select a.kr_name, mr.role_name
from movie_role mr, actor a
where mr.aid = mr.aid and mr.naver_key = 192608;

#인덱스 설정
create index idx_movie_kr_title on movie(kr_title);
create index idx_movie_opening_date on movie(opening_date);
create index idx_movie_kr_title_opening_date on movie(kr_title, opening_date);

create index idx_actor_kr_name on actor(kr_name);
create index idx_director_kr_name on director(kr_name);
create index idx_scope_scope_str on scope(scope_str);
create index idx_country_country_str on country(country_str);
