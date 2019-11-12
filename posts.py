class Post:
    def __init__(self, date, text, like=0, comment=0):
        self.date = date
        self.text = text
        self.like = like
        self.comment = comment
        self.topic = 'default'

    def has_keywords(self, *keywords):
        for i in keywords:
            if i in self.text:
                return True
        return False

    def set_topic(self, topic):
        self.topic = topic
