from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tqdm.auto import trange
from utils import Article, NewsTextDataset
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

CATEGORIES_IDXS = [8, 5, 9, 13]


class NewsCrawler:
    def __init__(
        self,
        driver_path: str = None,
        headless: bool = False,
        articles_desired_amount: int = 100,
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
        self.save_steps = [100, 500, 1000, 2000, 3000]

    def __call__(self, link):
        self.wd.get(link)
        start_link = self.wd.current_url
        dataset = NewsTextDataset()
        for i in trange(len(CATEGORIES_IDXS), desc="Iterate over categories"):
            unique_ids = []
            idx = CATEGORIES_IDXS[i]
            start = time.time()
            self.wd.get(start_link)
            print("Start link is:", self.wd.current_url)
            category_ref = self.wd.find_element_by_xpath(
                f"/html/body/table/tbody/tr[4]/td[1]/div/div[{idx}]",
            )
            try:
                category = category_ref.text.lower()
                logging.info(
                    f"\nStarting downloding data from {category} category",
                )
                category_ref.find_element_by_tag_name("a").click()
            except:
                print("Something wrong")
            added_articles_amount = 0
            watched_articles_amount = 0
            while added_articles_amount < self.articles_desired_amount:
                main_news_container = self.wd.find_element_by_class_name(
                    "content-column",
                )
                articles = main_news_container.find_elements_by_class_name(
                    "index-news-item",
                )
                articles_amount_by_page = len(articles)
                prev_day = (
                    main_news_container.find_elements_by_css_selector(
                        " body > table > tbody > tr:nth-child(3) >"
                        " td.content-column > div",
                    )[0]
                    .find_element_by_tag_name("a")
                    .get_attribute(
                        "href",
                    )
                )
                links = []
                titles = []
                for elem in articles:
                    try:
                        link = elem.find_element_by_tag_name(
                            "a",
                        ).get_attribute(
                            "href",
                        )
                        if link in unique_ids:
                            logging.info("Duplicate!")
                            watched_articles_amount += 1
                            continue
                        else:
                            unique_ids.append(link)
                            links.append(link)
                            watched_articles_amount += 1
                            title = elem.find_element_by_class_name(
                                "index-news-title",
                            ).text.replace('"', "")
                            titles.append(title)
                    except:
                        print("No link provided!")

                for link, title in tqdm(zip(links, titles)):
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
                    article.set_category(category)
                    article.set_title(title)
                    article.set_text(text)
                    article.set_tags(current_tags)
                    if dataset.append(article):
                        added_articles_amount += 1
                    else:
                        logging.info("Duplicate appending!")
                    print("\n Running dataset size:", dataset.size)
                    del article
                    self.wd.back()
                    if added_articles_amount >= self.articles_desired_amount:
                        break

                if dataset.size in self.save_steps:
                    logging.info("Saving dataset\n")
                    path = f"../datasets/{dataset.size}_articles_dataset.json"
                    dataset.save(path=path)

                if watched_articles_amount == articles_amount_by_page:
                    watched_articles_amount = 0
                    self.wd.get(prev_day)

            logging.info(
                f"Downloaded data from {category} category.\n "
                f" It took {round(time.time() - start, 2)} seconds\n"
                f"The dataset size now is {len(dataset)}",
            )

        logging.info(
            f"Download finished\n" f"{len(dataset)} articles were downloaded!",
        )
        logging.info("Saving dataset\n")

        dataset.save(path="../final_dataset.json")

    def close(self):
        self.wd.close()
