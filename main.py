from utils import NewsCrawler
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dr_pth",
        "--driver_path",
        type=str,
        default="/home/alexander/Downloads/chromedriver",
    )
    parser.add_argument(
        "-head",
        "--headless",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-art_num",
        "--articles_amount",
        type=int,
        default=1000,
    )

    # TODO add categories ids as a parameter
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    scrapper = NewsCrawler(
        driver_path=args.driver_path,
        headless=args.headless,
    )
    scrapper("http://txt.newsru.com")
    scrapper.close()
