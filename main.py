import requests
from bs4 import BeautifulSoup
import os.path
import numpy as np
import json
import re


BASE_URL = 'https://boards.4channel.org/biz/'

# Fetch and format list of all coin symbols from CoinGeko api
coingeko__coin_list = json.loads(requests.get('https://api.coingecko.com/api/v3/coins/list').text)
coingeko__coin_list = [coin_entry['symbol'].upper() for coin_entry in coingeko__coin_list]


stopwords  = []


# =========== PRINT METHODS
def print_title(title):
    print('>>>' + title)
    
def print_done():
    print('...Done!')
    

def print_posts_mentioning_coin(target, posts_by_thread_dict):
    target = target.upper()
    for thread_key in posts_by_thread_dict:    
        for post in posts_by_thread_dict[thread_key]:
            
            target_found = re.search(rf"\b{target}\b", post, re.IGNORECASE)
            
            if target_found:
                print(thread_key)
                print(post + '\n')


# =========== SCRAPE 4CHAN METHODS

def fetch_all_thread_urls_from_page(page_soup):
    thread_reply_links = page_soup.find_all('a', attrs={'class': 'replylink'})
    thread_urls = []

    for thread_reply_link in thread_reply_links:
        target_url = BASE_URL + thread_reply_link.attrs['href']
        
        # remove optional end path to avoid duplicates and slug change issues         
        end_path = os.path.split(target_url)[1]
        if end_path.isnumeric():
            thread_urls.append(BASE_URL + thread_reply_link.attrs['href'])
        
    return thread_urls


def fetch_all_posts_from_thread(thread_url):       
    thread_page = requests.get(thread_url)
    thread_page_soup = BeautifulSoup(thread_page.content, 'html.parser')
    thread_post_soup = thread_page_soup.find_all(attrs={'class': 'postMessage'})
    
    all_thread_posts = []

    for thread_post in thread_post_soup:
        all_thread_posts.append(thread_post.get_text())
                        
    return all_thread_posts


# TODO: make requests async to speed up time
def fetch_all_posts_on_biz():
    # fetch threads linked on the home page
    print_title('fetching home page thread links...')
    home_page = requests.get(BASE_URL)
    home_soup = BeautifulSoup(home_page.content, 'html.parser')
    all_thread_urls = fetch_all_thread_urls_from_page(home_soup)
    print_done()

    # fetch threads links from all other pages
    for i in range(2, 10):
        print_title('fetching page ' + str(i) + ' thread links...')
        page = requests.get(BASE_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_thread_urls = all_thread_urls + fetch_all_thread_urls_from_page(soup)
        print_done()


    # fetch every post from all threads on 4chan 
    all_posts_by_thread_dict = {}
    inc_count = 1
    total_count = len(all_thread_urls)

    for thread_url in all_thread_urls:
        print_title('fetching thread content ' + str(inc_count) + ' of ' + str(total_count) + ' : ' + thread_url)    
        specific_thread_messages = fetch_all_posts_from_thread(thread_url)
        all_posts_by_thread_dict[thread_url] = specific_thread_messages
        inc_count += 1
        print_done()
    
    return all_posts_by_thread_dict


# =========== DATA CLEANING AN CALCULATION 

def filter_for_potential_ticker_references(sentance):
    # TODO: can probably be removed as we are now comparing against coingeko tickers     
    wordlist = sentance.split()
    wordlist = [w for w in wordlist if len(w) < 6 and len(w) > 2] # no ticker longer than 5
    wordlist = [w for w in wordlist if w.isupper()]
    wordlist = [word.replace(".", "") for word in wordlist]
    wordlist = [w for w in wordlist if w.upper() not in stopwords] # remove stop words
    
    return wordlist

def filter_for_coins_list_on_coingecko(word_list):
    return [w for w in word_list if w not in coingeko__coin_list]

def calculate_freq_of_word(wordlist, word_freq = {}):
    for word in wordlist:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1
            
    return word_freq


def sort_freq_dict(freq_dict):
    aux = [(freq_dict[key], key) for key in freq_dict]
    aux.sort()
    aux.reverse()
    return aux


def flatten_post_by_thread_dict(content_of_threads_on_page):
    all_posts_in_dict = []
    
    for thread_key in content_of_threads_on_page:
        for post in content_of_threads_on_page[thread_key]:
            all_posts_in_dict.append(post)
            
    return all_posts_in_dict


def calculate_freq_of_coin_tickers_in_posts(list_of_posts):
    coin_freq_dict = {}

    for sentance in list_of_posts:
        potential_tickers = filter_for_potential_ticker_references(sentance)
        confirmed_tickers = filter_for_coins_list_on_coingecko(potential_tickers)
        coin_freq_dict = calculate_freq_of_word(potential_tickers, coin_freq_dict)
        
    return coin_freq_dict



# ========== MAIN

# fetch every post from /biz/ returning a dict with the format
# { <thread url>: ['message 1', message2]}
all_posts_by_thread_dict = fetch_all_posts_on_biz()    

# flatten messages into a 1D array of strings (the post content)
all_posts_flattened = flatten_post_by_thread_dict(all_posts_by_thread_dict)

# Find coin tickers, calculate their frequency and sort by freq
coin_freq_dict = sort_freq_dict(calculate_freq_of_coin_tickers_in_posts(all_posts_flattened))


# Print top 10 coins
for entry in coin_freq_dict[0:10]:
    print(entry)