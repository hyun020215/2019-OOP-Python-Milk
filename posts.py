class Post:
    def __init__(self, date, text, like=0, comment=0):
        self.date = date
        self.text = text
        self.like = like
        self.comment = comment
        self.topic = []

    def has_keywords(self, *keywords):
        for i in keywords:
            if i in self.text:
                return True
        return False

    def find_topic(self):
        if not self.topic:
            if self.has_keywords(['기숙사', '사감', '정독', '소학', '요양', '벌점', '자습', '냉장', '점호', '폰', '스탠딩']):
                self.topic.append('dormitory')
            if self.has_keywords(['급식', '영양사', '조리사', '메뉴', '점심', '잔반', '배식']):
                self.topic.append('cafeteria')
            if self.has_keywords(['입시', '대학', '면접', '논술', '원서']):
                self.topic.append('college')
            if self.has_keywords(['음악실', '노래방', '악기', '피아노', '드럼', '바이올린']):
                self.topic.append('music')
            if self.has_keywords(['신입생', '예비', '입학']):
                self.topic.append('freshmen')
            if self.has_keywords(['대나무숲', '페이지', '대숲', '건의사항', '신문고', '규정']):
                self.topic.append('suggestion')
            if self.has_keywords(['본관', '도서관', '공강', '성적', '미술실', '레이저', '홈룸', '수업', '체육관']):
                self.topic.append('school')
            if self.has_keywords(['쓰레기', '청소']):
                self.topic.append('clean')
            if self.has_keywords(['종소리', '벨소리', '기상송', '방송부']):
                self.topic.append('bell')
            if self.has_keywords(['운동장']):
                self.topic.append('exercise')

