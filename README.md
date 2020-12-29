<h1 align="center">🥪 멋쟁이사자 7기 : 원광대학교 주변 음식점 추천 사이트 🍔</h1>

---

<h1>멋쟁이사자 7기 : Django를 처음 이용하여 만든 웹 프로젝트</h1>

~~~
현재 내 위치 기준으로 음식의 장르를 선택하여 랜덤으로 해당 가게의 음식을 추천해주는 서비스
~~~

<h3 align="center">[[첫페이지]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/start_page.PNG"/>
</p>

~~~
랜덤으로 선택할 수 있는 종류를 '음식'과 '후식'으로 나누었다!
(디저트는 미완성)
~~~

<h3 align="center">[[선택페이지]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/select_page.PNG"/>
</p>

~~~
음식의 분류를 선택할 수 있는 창이 뜬다.
~~~

<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/select_page2.PNG"/>
</p>

~~~
분류를 선택하여 원하는 종류를 OR 하여 해당 선택한 분류들 중에서 추첨을 한다!
~~~

<h3 align="center">[[선택페이지 기능]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/around.PNG"/>
</p>

~~~
내 현재 위치의 좌표 기준에서 범위 0.7KM 반경의 식당에서 찾는다.
높이거나 줄일 수 있다.
~~~

<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/price.PNG"/>
</p>

~~~
가격대를 선정하여 해당 가격에 범위에 맞는 식당의 음식을 추천해준다.
~~~

<h3 align="center">[[선택 결과]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/selected_page.PNG"/>
</p>

~~~
랜덤으로 뽑힌 음식의 나와 가게 까지의 거리와 해당 가게의 위치를 Naver 지도 Map API를 이용하여 내 현재 위치 그리고 가게의 위치를 보여준다.
(현재 Naver API가 만료되어 보이지 않는다.)
~~~

<h3 align="center">[[선택 결과 추가 내용]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/selected_page2.PNG"/>
</p>

~~~
해당 가게의 다른 메뉴들 까지 볼 수가 있다.
~~~

<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/Map.PNG"/>
</p>

~~~
만약 네이버 지도를 이용해서 봤을 경우 이렇게 보인다.
~~~

<h3 align="center">[[사장 페이지(MyPage)]]</h3>
<p align="center">
<img alt="YAMUCKZA" src="https://github.com/cwadven/YAMUCKZA/blob/master/assets/my_page.PNG"/>
</p>

~~~
아이디 회원가입하면 사장님이 직접 상품을 등록할 수 있다!
기존에 들어가있는 음식 및 식당은 초기로 넣은 정보들이여서 User는 없다.
~~~

<h1>멋쟁이사자 프로젝트 팀원 소개</h1>

## 기획자 📃

👤 왕희승 (팀장)

- Github : https://github.com/aweking
- 작업 : 
    - 프로젝트 아이디어 제공 및 식당, 음식, 위치, 가격 정보 수집
- 기술스택 :
    - Excel
- 개발기간 :
    - 2019-08-29 ~ 2019-11-16

## 디자이너 🖼

👤 은휴

- Github : https://github.com/agustd0423
- 작업 : 
    - 이미지 및 디자인 UI 및 아이콘 수집
- 기술스택 : 
    - PhotoShop
- 개발기간 :
    - 2019-08-29 ~ 2019-11-16

## 개발자 👨‍💻

👤 이창우[메인 개발] (부팀장)

- Github : https://github.com/cwadven
- 작업 : 
    - Django 프로젝트 기본 기반 설정
    - DB 테이블 구축
    - Javascript로 작동하는 모든 것 구현
    - Naver 지도 API 시각적 요소 소스코드 추가
- 기술스택 :
    - Django
    - Javascript
    - HTML
    - CSS
- 개발기간 :
    - 2019-08-29 ~ 2019-11-16


👤 정현지

- Github : https://github.com/hyeonji0409
- 작업 : 
    - XML 디자인 및 레이어 작업
- 기술스택 :
    - HTML
    - CSS
- 개발기간 :
    - 2019-08-29 ~ 2019-11-16

👤 진형빈

- Github : https://github.com/gudqls5812
- 작업 :
    - Naver 지도 API 사용
    - 디자인 UI, UX 설정
    - Python 보조
- 기술스택 : 
    - HTML
    - Javascript
- 개발기간 :
    - 2019-08-29 ~ 2019-11-16

## 환경 구축

~~~
1. python -m venv myvenv (가상환경 생성)
2. python source myvenv/Script/activates (가상환경 실행)
3. pip install -r requirements.txt (의존성 모듈 설치)
4. python manage.py collectstatic (static 파일 생성)
8. python manage.py migrate (테이블 생성)
9. python manage.py createsuper (관리자 id 생성)
10. python manage.py runserver
~~~

## 2020-12-29 README.md 작성하는 내가 바라보는 프로젝트 코드

처음 Django를 사용하여 만든 프로젝트였다.

소스코드가 너무 엉망인 것을 느꼈다....

지금은 이때보다는 소스코드 이해도도 높아졌고, 확실히 이때에 비해 성장을 많이 한 것 같다.