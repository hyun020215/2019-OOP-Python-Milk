# 2019-2 객체지향 프로그래밍 프로젝트 - **우유 팀**
구성원: 2-1 정유진 | 2-5 양우현

## 1. 주제
'세종과학예술영재학교 대나무숲' 페이스북 페이지 게시글 분석 프로그램

## 2. 동기
'세종과학예술영재학교 대나무숲' 페이스북 페이지는 익명성이 보장되는 온라인 공간으로,
우리 학교의 학생을 비롯한 관계자들이 의견 표명으로 가해질 불이익을 걱정하지 않고
자신의 입장과 생각을 온전하게 표현할 수 있는 창구이기도 하다.
따라서 이 공간에서는 다양한 사람들이 어떤 분야에 관심을 갖고 있으며, 어떤 글에 공감하는지에 대한 정보를 얻을 수 있다.
그러나 이러한 정보를 교내 여러 단체에서 제대로 활용하고 있지 못하다는 생각이 들었고,
이에 페이지의 게시글을 통계적으로 정리하여 경향성을 쉽게 파악할 수 있는 프로그램을 제작하게 되었다.

## 3. 프로그램 사용 대상
학생회와 기숙사자치위원회 등 학생들의 여론을 파악해야 하는 단체

## 4. 목적
'세종과학예술영재학교 대나무숲' 페이지의 게시글을 분석하여 학생들이 어떤 분야에 관심을 갖고 있으며,
어떤 글에 공감하는가를 통계적으로 분석하고 시각화하여 사용자에게 제공한다.

## 5. 주요기능
1. 원하는 기간을 입력하면 그 기간 내의 '대나무숲' 게시글을 검색하여 리스트로 보여준다.
2. 리스트의 게시글을 올라온 시간 순서대로, 좋아요 및 공감 수 순서대로, 주제별로 정렬한다.
3. 게시글을 주제별로 분류한 다음 시각화 과정을 거쳐 그래프로써 사용자에게 통계 결과를 보여준다. 
4. GUI를 이용하여 사용자가 원하는 주제, 날짜 등을 입력받고 통계 결과를 출력한다.

## 6. 프로젝트 핵심
프로젝트의 핵심은 페이스북 페이지로부터 필요한 데이터를 가져오고, 그 데이터를 목적에 맞게 가공하여 정렬하는 것이다.
이를 구현하는 과정에서 객체지향의 특징을 활용했다.
예컨대 가져온 게시글의 특징을 총괄하는 클래스를 만들어 이 클래스를 바탕으로 게시글 각각의 객체를 만드는 방법이나,
시각화를 제공하는 클래스(그래프의 이름, 그래프가 해당하는 날짜 등)를 상속하여
막대그래프, 표, 파일 내보내기 등이 구현된 클래스를 만드는 방법이 있을 것이다.


## 7. 구현에 필요한 라이브러리나 기술
1. 기술
    - web parsing : 웹 사이트에서 원하는 정보를 자동으로 수집하는 것
2. 라이브러리
    - Beautifulsoup : 웹 데이터를 가져올 때 사용되는 라이브러리이다. 페이지의 HTML 소스를 가져올 때,
    태그를 읽어서 우리가 이용할 부분인 게시글이나 좋아요를 분리해서 찾아주는 기능을 구현하기 위해 사용된다.
    > &nbsp;&nbsp;공식 사이트 - https://www.crummy.com/software/BeautifulSoup/

    - pyautogui : 파이썬을 이용하여 마우스와 키보드의 움직임을 제어할 수 있는 기능을 제공한다.
    자동 스크롤을 구현하여 대나무숲의 예전 게시글들을 읽어 올 것이다.
    Facebook Open API에 페이지 연동 기능이 구현되어 있으나,
    해당 페이지의 관리자 권한과 토큰이 필요한 관계로 사용이 불가하다.
    > &nbsp;&nbsp;공식 사이트 - https://pyautogui.readthedocs.io/en/latest/#

    - matplotlib : 파이썬에서 자료를 표나 그래프로 시각화시키는 기능을 제공한다.
    대나무숲에서 획득한 데이터를 그래프화 시키는 데 사용될 것이다.
    > &nbsp;&nbsp;공식 사이트 - https://matplotlib.org/

    - pyqt5 : GUI 구성을 할 수 있는 기능을 제공한다. 데이터를 분석한다는 기본 기능을 완전히 구현한 프로그램을 만든 뒤,
    이를 GUI로 구현하고 싶어진다면 사용할 라이브러리이다.
    > &nbsp;&nbsp;공식 사이트 - https://pypi.org/project/PyQt5/
    >
    > &nbsp;&nbsp;한국어 사용법 사이트 - https://wikidocs.net/book/2165

## 8. **분업 계획**
1. '세종과학예술영재학교 대나무숲' 페이지로부터 게시글을 html 파싱하는 모듈 개발 - 정유진, 양우현
2. 글의 키워드, 주제, 공감 수, 포스팅 시간 등의 속성을 갖는 post 클래스 개발 - 정유진
3. 파싱한 게시글들을 post 객체로 만든 후 리스트로 반환하는 모듈 개발 - 정유진
4. 각 게시글의 데이터를 분석하여 주제별, 시간대별, 공감 수별로 분류하는 모듈 개발 - 양우현 
5. 분류 결과를 주제별 게시글 수(막대 그래프), 시간대별 동일 주제 게시글 증가 추이(꺾은선 그래프) 등
다양한 그래프로 사용자에게 보여주는 GUI 구현 모듈 개발 - 정유진, 양우현

## 9. 기타

<hr>

#### readme 작성관련 참고하기 [바로가기](https://heropy.blog/2017/09/30/markdown/)

#### 예시 계획서 [[예시 1]](https://docs.google.com/document/d/1hcuGhTtmiTUxuBtr3O6ffrSMahKNhEj33woE02V-84U/edit?usp=sharing) | [[예시 2]](https://docs.google.com/document/d/1FmxTZvmrroOW4uZ34Xfyyk9ejrQNx6gtsB6k7zOvHYE/edit?usp=sharing) | [[예시 3]](https://github.com/goldmango328/2018-OOP-Python-Light) | [[예시4]](https://github.com/ssy05468/2018-OOP-Python-lightbulb) | [[모두보기]](https://github.com/kadragon/oop_project_ex/network/members)
