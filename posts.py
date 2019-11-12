class Post:
    words = {
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

    def __init__(self, date, text, like=0, comment=0):
        self.date = date
        self.text = text
        self.like = like
        self.comment = comment
        self.category = []

    def has_keywords(self, keywords):
        for i in keywords:
            if i in self.text:
                return True
        return False

    def find_category(self):
        if not self.category:
            for topic, keywords in Post.words.items():
                if self.has_keywords(keywords):
                    self.category.append(topic)
        return self.category


if __name__ == '__main__':
    post = Post('2019.11.12', '급식 먹기 싫어요 폰도 안 내면 안 돼요?')
    print(post.find_category())
