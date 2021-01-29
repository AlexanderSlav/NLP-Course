from nlp_utils import NewsCrawler
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dr_pth",
        "--driver_path",
        type=str,
        default="/home/alexander/Downloads/chromedriver",
        help="Path to chromedriver for selenium",
    )
    parser.add_argument(
        "-head",
        "--headless",
        type=bool,
        default=False,
        help="If true scrapping will be  processed without visualization",
    )
    parser.add_argument(
        "-art_num",
        "--articles_amount",
        type=int,
        default=1000,
        help="The desired amount of articles by category",
    )
    parser.add_argument(
        "-save_path",
        "--output_save_path",
        type=str,
        default="../datasets/final_dataset.json",
        help="The desired amount of articles by category",
    )

    # TODO add categories ids as a parameter
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    scrapper = NewsCrawler(
        driver_path=args.driver_path,
        headless=args.headless,
        articles_desired_amount=args.articles_amount,
        output_save_path=args.output_save_path,
    )
    scrapper("http://txt.newsru.com")
    scrapper.close()
