from typing import List


class Article:
    def __init__(
        self,
        url: str = None,
        title: str = None,
        category: str = None,
        tags: List[str] = None,
        text: str = None,
    ):
        self.article_id = url
        self.title = title
        self.category = category
        self.tags = tags
        self.text = text

    def set_article_id(self, url):
        self.article_id = url

    def set_title(self, title):
        self.title = title

    def set_category(self, category):
        self.category = category

    def set_tags(self, tags):
        self.tags = tags

    def set_text(self, text):
        self.text = text
