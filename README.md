# BizCoin Scraper
A simple Jupyter notebook that scrapes 4chan’s /biz/ board to measure the “hotness” of specific crypto tokens, offering a potential data point for making investment decisions.

## Rational 
The idea behind this project is straightforward:
1. Low-market-cap token holders (“bag-holders”) often promote their coins on social platforms like 4chan to create hype and push the price upward.
2. If a potential investor (ie me) can identify which tokens are gaining traction before a major pump and sell before the inevitable dump, there may be a profit window to exploit.
3. This script aims to track increases in token mentions (i.e., “hotness”) across 4chan /biz/, under the theory that early spikes in discussion might signal upcoming price action.

## How it works
1. The script uses BeautifulSoup to scrape all current threads and comments from 4chan’s /biz/ board.
2. A list of valid token tickers (e.g., Bitcoin → BTC) are pulled from CoinMarketCap.
3. The script counts how often each valid token ticker is mentioned across all scraped pages and builds a frequency table of mentions.

# Disclaimer from the author
1. Given the nature of 4chan as a service, a profanity filter was required, as a result this repository contains a `stopwords` array.
2. This is a side project done for fun, it is not in anyway a valid way to do informed investing
