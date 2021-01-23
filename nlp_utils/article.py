from typing import List


class Article:
    def __init__(
        self,
        url: str = None,
        title: str = None,
        category: str = None,
        tags: List[str] = None,
        text: str = None,
        dict_object: dict = None,
    ):
        self.article_id = url
        self.title = title
        self.category = category
        self.tags = tags
        self.text = text
        self.tokenized_text = None

        if dict_object is not None:
            self.set_article_id(dict_object["article_id"])
            self.set_title(dict_object["title"])
            self.set_category(dict_object["category"])
            self.set_tags(dict_object["tags"])
            self.set_text(dict_object["text"])
            if "tokenized_text" in dict_object.keys():
                self.set_tokenized_text(dict_object["tokenized_text"])

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

    def set_tokenized_text(self, text):
        self.tokenized_text = text

    def to_dict(self):
        return {
            "category": self.category,
            "tokenized_text": self.tokenized_text,
        }
