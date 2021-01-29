from .article import Article
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import re
from alphabet_detector import AlphabetDetector
from tqdm import tqdm

ad = AlphabetDetector()
nltk.download("stopwords")


class NewsTextDataset:
    def __init__(self):
        self.data = []
        self.unique_ids = []
        self.mystem = Mystem()
        self.russian_stopwords = stopwords.words("russian")
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+",
        )

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

    def load(self, path):
        with open(path) as json_file:
            data = json.load(json_file)
        self.data = [Article(dict_object=obj) for obj in data["catalog"]]

    def preprocess(self):
        for idx, article in tqdm(enumerate(self.data)):
            # remove english text, dollar sign, and brackets
            text = re.sub(r"[a-zA-Z]|\$|\d*|\(|\)|/@", u"", article.text)
            text = self.emoji_pattern.sub(u"", text)
            tokens = self.mystem.lemmatize(text.lower())
            tokens = [
                token
                for token in tokens
                if token not in self.russian_stopwords
                and token != " "
                and token.strip() not in punctuation
                and ad.is_cyrillic(token)
            ]
            article.tokenized_text = tokens
            self.update(article, idx)

    def dump_to_pandas(self):
        return pd.DataFrame.from_records(
            [article.to_dict() for article in self.data],
        )

    def __len__(self):
        return len(self.data)

    def update(self, article, idx):
        self.data[idx].tokenized_text = article.tokenized_text

    # Useless for now
    def __getitem__(self, idx):
        return self.data[idx]
