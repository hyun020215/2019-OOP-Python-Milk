import pickle


# 게시글 클래스
class Post:
    # 주제별 키워드
    file = open('category_keywords.pickle', 'rb')
    topics = pickle.load(file)
    file.close()

    # 초기 값 - date: 게시 시일(YYYY.MM.DD), text: 내용, like: 좋아요 및 공감 수, comment: 댓글 수
    def __init__(self, date: str, text: str, like: int = 0, comment: int = 0) -> None:
        self.date = date
        self.text = text
        self.like = like
        self.comment = comment

        # 게시글의 주제 분류, get_category 메써드를 제외하고 외부 접근 불가
        self.__category = []
        for topic, keywords in Post.topics.items():
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
