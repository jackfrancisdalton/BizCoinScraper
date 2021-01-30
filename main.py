import requests
from bs4 import BeautifulSoup
import os.path
import numpy as np
import json

BASE_URL = 'https://boards.4channel.org/biz/'

# Fetch and format list of all coin symbols from CoinGeko api
coingeko__coin_list = json.loads(requests.get('https://api.coingecko.com/api/v3/coins/list').text)
coingeko__coin_list = [coin_entry['symbol'].upper() for coin_entry in coingeko__coin_list]

# List of words to exclude as we do not care about them
stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'i\'m', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'got', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime', 'time']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['gonna', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where', 'day', ]
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your', 'WTF', 'drop', 'gme,', 'gme.']
stopwords += ['yours', 'yourself', 'yourselves', 'shit', 'dip']
stopwords += ['want', 'make', 'think', 'just', 'like', 'going', 'don\'t', 'it\'s']
stopwords += ['dont', 'can\'t', 'im', 'coming', 'right', 'it.', 'know', 'right', 'said', 'does']
stopwords += ['SEC', 'BTC', 'AMC', 'NOK', 'GME', 'BUY', 'DAY', 'TRY', 'fall', 'WSB', 'fuck', 'hype']
stopwords += ['sell', 'buy', 'jew', 'jews', 'bb', 'amd', 'push', 'send', 'hold', 'hodl', 'moon']
stopwords += ['KYC', 'PUT', 'CEO', 'STOP', 'SOLD', 'LOL', 'LOOK', 'FUD', 'pump']
stopwords = [x.upper() for x in stopwords]


# =========== PRINT METHODS
def printTitle(title):
    print('>>>' + title)
    
def printDone():
    print('...Done!')
    
    
def printPostsRelatingToCoin(target, posts_by_thread_dict):
    target = target.upper()
    for thread_key in posts_by_thread_dict:
        for post in posts_by_thread_dict[thread_key]:
            if target in post.upper():
                print(thread_key)
                print(post + '\n')


# =========== SCRAPE 4CHAN METHODS

def getAllThreadURLsFromPage(page_soup):
    thread_reply_links = page_soup.find_all('a', attrs={'class': 'replylink'})
    thread_urls = []

    for thread_reply_link in thread_reply_links:
        target_url = BASE_URL + thread_reply_link.attrs['href']
        
        # remove optional end path to avoid duplicates and slug change issues         
        end_path = os.path.split(target_url)[1]
        if end_path.isnumeric():
            thread_urls.append(BASE_URL + thread_reply_link.attrs['href'])
        
    return thread_urls


def getAllMessagesInThread(thread_url):       
    thread_page = requests.get(thread_url)
    thread_page_soup = BeautifulSoup(thread_page.content, 'html.parser')
    thread_post_soup = thread_page_soup.find_all(attrs={'class': 'postMessage'})
    
    thread_post_messages = []

    for thread_post in thread_post_soup:
        thread_post_messages.append(thread_post.get_text())
                        
    return thread_post_messages


# TODO: make requests async to speed up time
def fetchAllPostsFromBiz():
    # fetch threads linked on the home page
    printTitle('fetching home page thread links...')
    home_page = requests.get(BASE_URL)
    home_soup = BeautifulSoup(home_page.content, 'html.parser')
    all_thread_urls = getAllThreadURLsFromPage(home_soup)
    printDone()

    # fetch threads links from all other pages
    for i in range(2, 10):
        printTitle('fetching page ' + str(i) + ' thread links...')
        page = requests.get(BASE_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_thread_urls = all_thread_urls + getAllThreadURLsFromPage(soup)
        printDone()


    # fetch every post from all threads on 4chan 
    all_posts_by_thread_dict = {}
    inc_count = 1
    total_count = len(all_thread_urls)

    for thread_url in all_thread_urls:
        printTitle('fetching thread content ' + str(inc_count) + ' of ' + str(total_count) + ' : ' + thread_url)    
        specific_thread_messages = getAllMessagesInThread(thread_url)
        all_posts_by_thread_dict[thread_url] = specific_thread_messages
        inc_count += 1
        printDone()
    
    return all_posts_by_thread_dict


# =========== DATA CLEANING AN CALCULATION 

def getPotentialTickerWords(sentance):
    # TODO: can probably be removed as we are now comparing against coingeko tickers     
    wordlist = sentance.split()
    wordlist = [w for w in wordlist if len(w) < 6 and len(w) > 2] # no ticker longer than 5
    wordlist = [w for w in wordlist if w.isupper()]
    wordlist = [word.replace(".", "") for word in wordlist]
    wordlist = [w for w in wordlist if w not in stopwords] # remove stop words
    
    return wordlist

def filterByOnCoinGeko(word_list):
    return [w for w in word_list if w not in coingeko__coin_list]

def calculateWordFreq(wordlist, word_freq = {}):
    for word in wordlist:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1
            
    return word_freq


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def flattenPostContent(content_of_threads_on_page):
    all_posts_flattened = []
    
    for thread_key in content_of_threads_on_page:
        for post in content_of_threads_on_page[thread_key]:
            all_posts_flattened.append(post)
            
    return all_posts_flattened


def calculateCoinOccurencyFrequency(list_of_posts):
    coin_freq_dict = {}

    for sentance in list_of_posts:
        potential_tickers = getPotentialTickerWords(sentance)
        confirmed_tickers = filterByOnCoinGeko(potential_tickers)
        coin_freq_dict = calculateWordFreq(potential_tickers, coin_freq_dict)
        
    return coin_freq_dict


# ========== MAIN

# fetch every post from /biz/ returning a dict with the format
# { <thread url>: ['message 1', message2]}
all_posts_by_thread_dict = fetchAllPostsFromBiz()    

# flatten messages into a 1D array of strings (the post content)
all_posts_flattened = flattenPostContent(content_of_threads_on_page)

# Find coin tickers, calculate their frequency and sort by freq
coin_freq_dict = sortFreqDict(calculateCoinOccurencyFrequency(all_posts_flattened))

# Print top 10 coins
for entry in coin_freq_dict[0:10]:
    print(entry)

# Print posts about the top coin
top_rated_coin_ticker = coin_freq_dict[0][1]
printTitle('Printing messages related to most mentiond coin: ' + top_rated_coin_ticker)
printPostsRelatingToCoin(top_rated_coin_ticker, all_posts_by_thread_dict)