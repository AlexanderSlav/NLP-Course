from .article import Article
import json


class NewsTextDataset:
    def __init__(self):
        self.data = []

    def append(self, article: Article):
        self.data.append(article)

    def save(self, path):
        with open(path, "w") as fp:
            json.dump(
                [ob.__dict__ for ob in self.data],
                fp,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def __len__(self):
        return len(self.data)
