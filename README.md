# 네이버 영화 데이터베이스 구축 및 웹 구현

## 요약
네이버 영화 사이트(movies.naver.com)로부터 영화 데이터를 수집하여 mySQL에 DB화하고,
검색 인터페이스 제공하는 프로젝트  

## 개발 환경
- DB: MySQL
- 크롤링: Python, BeautifulSoup, Selenium
- 웹 및 서버: Django    

## DB 설계
1. E-R 다이어그램  
![image](https://user-images.githubusercontent.com/63103070/177087071-faf4e15d-8c61-4ca0-93bd-8e026b63bef4.png)

2. 관계형 테이블
- Database: naver_movie
- Strong Entity: movie, actor, director
- Movie weak entity: scope, country, photo, video, review, famous_line, user_rate, 
journalist_rate
- Review weak entity: comments
- Intersection table: movie_director
- Association table: movie_role   

## Crawling
- python에서 requests, BeautifulSoup, selenium 패키지를 사용하여 각 영화 정보를 크롤링
- movie table에 대한 정보를 먼저 수집하고 scope와 country를 수집
- url을 변경하면서 review, comments, user_rate, journalist_rate, famous_line, actor_director, video, photo를 수집
- Executemany를 사용해 데이터를 한꺼번에 insert
- 각 항목을 크롤링 하면서 null 일 경우에 대한 예외 처리를 진행
- 총 영화 10,035개, 배우 50,000개, 감독 10,141개, 장르 17,809개, 국가 11,047개, 사진 94,804개, 영상 20,161개, 리뷰 20,503개, 명대사 35,749개, 사용자 평점 53,960개, 평론가 평점 4,115개, 댓글 86,440개, 영화-감독 관계 10035개, 영화-배우 관계 87,825개로 총 512,624개의 투플을 수집하여 DB를 구축
- *crawling.py 코드 참조  


## 검색 인터페이스 구현
- 파이썬으로 작성된 오픈 소스 웹 프레임워크인 Django를 사용하여 웹 검색 인터페이스를 구현
- 검색 화면, 검색 결과 화면, 영화 상세 화면, 댓글 화면으로 총 4개의 화면으로 구성
![image](https://user-images.githubusercontent.com/63103070/177087828-8968ce7e-b3d5-4c4f-9674-35b0394745e8.png)

- 검색 속성: 제목, 배우, 감독, 장르, 날짜(해당 날짜 이후 개봉, 년도 별 영화), 국가
- 정렬 속성: 가나다 순, 가나다 역순, 오래된 순, 최신 순, 평점 높은 순, 평점 낮은 순
- 검색 속도의 향상을 위해 index를 구축. Select 문에서 주로 사용하는 애트리뷰트를 기준으로 index를 생성했으며 그 결과 검색 속도는 최대 0.25sec ~ 최소 0.00sec으로 유지  
![image](https://user-images.githubusercontent.com/63103070/177087950-89b2076b-ca1c-42a4-b29e-c6645a5a8c40.png)   

## 시연 영상
https://youtu.be/yfTa_d_8WvQ
