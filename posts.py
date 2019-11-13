# 게시글 클래스
class Post:
    # 주제별 키워드(set_topics 메써드 제외 외부 접근 불가)
    __topics = {
        '기숙사': ['기숙사', '사감', '정독', '소학', '요양', '벌점', '자습', '냉장', '점호', '폰', '스탠딩'],
        '급식': ['급식', '영양사', '조리사', '메뉴', '점심', '잔반', '배식'],
        '입시': ['입시', '대학', '면접', '논술', '원서'],
        '음악실': ['음악실', '노래방', '악기', '피아노', '드럼', '바이올린'],
        '신입생': ['신입생', '예비', '입학'],
        '건의사항': ['대나무숲', '페이지', '대숲', '건의사항', '신문고', '규정', '폰'],
        '본관': ['본관', '도서관', '공강', '성적', '미술실', '레이저', '홈룸', '수업', '체육관'],
        '청결': ['쓰레기', '청소'],
        '종소리': ['종소리', '벨소리', '기상송', '방송부'],
        '운동장': ['운동장', '축구']
    }

    # 사용자가 원하는 키워드를 주제별 키워드에 추가(미완, 개발 도중 필요에 따라 수정 필요)
    # 매개변수 - topic: 주제, keywords: 키워드(문자열) 묶음
    @ staticmethod
    def set_topics(topic: str, keywords: list) -> None:
        if topic in Post.__topics:  # 만약 이미 주제가 존재한다면 키워드 추가
            Post.__topics[topic].append(keywords)
        else:  # 기존에 없던 주제라면 주제와 키워드 동시 삽입
            Post.__topics[topic] = keywords

    # 초기 값 - date: 게시 시일, text: 내용, like: 좋아요 및 공감 수, comment: 댓글 수
    def __init__(self, date: str, text: str, like: int = 0, comment: int = 0) -> None:
        self.date = date
        self.text = text
        self.like = like
        self.comment = comment

        # 게시글의 주제 분류, get_category 메써드를 제외하고 외부 접근 불가
        self.__category = []
        for topic, keywords in Post.__topics.items():
            if self.has_keywords(keywords):
                self.__category.append(topic)

    # 게시글이 해당 키워드 중 하나라도 갖고 있는지 판별
    # 매개변수 - keywords: 키워드 묶음
    def has_keywords(self, keywords: list) -> bool:
        for i in keywords:  # 키워드 중 하나라도 갖고 있으면 True return
            if i in self.text:
                return True
        return False  # 키워드 중 어느 것도 포함되지 않으면 False return

    # 게시글의 주제 가져오기
    def get_category(self):
        return self.__category


if __name__ == '__main__':
    post = Post('2019.11.12', '입시도 끝났는데 급식 먹기 싫어요 폰도 안 내면 안 돼요?')
    print(post.get_category())
