from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from tqdm import tqdm
from utils import Article, NewsTextDataset
import json

driver_path = "/home/alexander/Downloads/chromedriver"

CATEGORIES_IDXS = [5, 8]


class NewsCrawler:
    def __init__(
        self,
        driver_path: str = None,
        headless: bool = False,
        articles_desired_amount: int = 15,
    ):
        self.driver_path = driver_path
        self.articles_desired_amount = articles_desired_amount
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.wd = webdriver.Chrome(
            executable_path=driver_path,
            options=chrome_options,
        )

    def __call__(self, link):
        self.wd.get(link)
        start_link = self.wd.current_url
        dataset = NewsTextDataset()
        for idx in CATEGORIES_IDXS:
            while self.wd.current_url != start_link:
                self.wd.back()
            category_ref = self.wd.find_element_by_xpath(
                f"/html/body/table/tbody/tr[4]/td[1]/div/div[{idx}]",
            )
            try:
                # category = category_ref.text.lower()
                category_ref.find_element_by_tag_name("a").click()
            except:
                print("Something wrong")
            # for articles_amount in tqdm(range(self.articles_desired_amount)):
            main_news_container = self.wd.find_element_by_class_name(
                "content-column",
            )
            articles = main_news_container.find_elements_by_class_name(
                "index-news-item",
            )
            # articles_amount_by_page = len(articles)
            # prev_day = main_news_container.find_elements_by_css_selector(
            #     " body > table > tbody > tr:nth-child(3) >"
            #     " td.content-column > div",
            # )
            links = []
            titles = []
            for elem in articles:
                try:
                    link = elem.find_element_by_tag_name("a").get_attribute(
                        "href",
                    )
                    links.append(link)

                    title = elem.find_element_by_class_name(
                        "index-news-title",
                    ).text.replace('"', "")
                    titles.append(title)
                except:
                    print("No link provided!")

            for link, title in zip(links, titles):
                self.wd.get(link)
                text = self.wd.find_element_by_css_selector(
                    "body > table > tbody > tr:nth-child(3) > "
                    "td.content-column > div.article > div.article-text",
                ).text

                current_tags = [
                    ",".join(
                        tag.text
                        for tag in self.wd.find_elements_by_class_name(
                            "article-tags-list",
                        )[1].find_elements_by_tag_name("a")[1:]
                    ),
                ]
                article = Article()
                article.set_article_id(link)
                article.set_title(title)
                article.set_text(text)
                article.set_tags(current_tags)
                dataset.append(article)
                del article
                self.wd.back()
        dataset.save(path="../dataset.json")

    def close(self):
        self.wd.close()


scrapper = NewsCrawler(driver_path=driver_path, headless=False)
scrapper("http://txt.newsru.com")
scrapper.close()
