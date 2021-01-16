# newspaper-scraping[russian]
This script scraping news data from http://txt.newsru.com

![](demo.gif)
## Installation

Setup the environment  `pip install -r requirements-dev.txt`

## Usage

```
usage: main.py [-h] [-dr_pth DRIVER_PATH] [-head HEADLESS]
               [-art_num ARTICLES_AMOUNT]

optional arguments:
  -h, --help            show this help message and exit
  -dr_pth DRIVER_PATH, --driver_path DRIVER_PATH
                        Path to chromedriver for selenium
  -head HEADLESS, --headless HEADLESS
                        If true scrapping will be processed without
                        visualization
  -art_num ARTICLES_AMOUNT, --articles_amount ARTICLES_AMOUNT
                        The desired amount of articles by category



```
