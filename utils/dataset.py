from .article import Article
import json


class NewsTextDataset:
    def __init__(self):
        self.data = []
        self.unique_ids = []

    def append(self, article: Article):
        if article.article_id not in self.unique_ids:
            self.unique_ids.append(article.article_id)
            self.data.append(article)
            return True
        else:
            return False

    def save(self, path):
        with open(path, "w") as fp:
            data = {
                "catalog": [ob.__dict__ for ob in self.data],
            }
            json.dump(
                data,
                fp,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def __len__(self):
        return len(self.data)
