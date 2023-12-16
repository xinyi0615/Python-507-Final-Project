#############################################################
#############################################################
###   __  ___             _  __        __                 ###
###   \ \/ (_)_ __  _   _(_) \ \      / /_ _ _ __   __ _  ###
###    \  /| | '_ \| | | | |  \ \ /\ / / _` | '_ \ / _` | ###
###    /  \| | | | | |_| | |   \ V  V / (_| | | | | (_| | ###
###   /_/\_\_|_| |_|\__, |_|    \_/\_/ \__,_|_| |_|\__, | ###
###                 |___/                          |___/  ###
#############################################################
#############################################################
# Author: Xinyi Wang
# Student Unique name: xinyw
# Course Title:  SI 507
# Date: 2023-12-01

import Keys

import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from flask import Flask, render_template, request, redirect, url_for
import sys
from fredapi import Fred
import yfinance as yf
import praw
import nltk
#Some package maybe needed
#nltk.download('punkt')
#nltk.download('stopwords')
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
from selenium import webdriver
app = Flask(__name__)


def get_series_id(term):
    ensure_cache_folder('Series_ID')
    cache_filename = f"{'Series_ID'}/{term.replace(' ', '_')}_search_results.csv"
    if check_cache(cache_filename):
        print("Cache Found! ")
        data = read_cache(cache_filename)
    else:
        fred = Fred(Keys.api_fred)
        search_results = fred.search(term, limit=500, order_by="search_rank")
        columns_to_keep = ['id', 'title', 'notes']
        data = search_results[columns_to_keep]
        save_cache(data, cache_filename)
    return data

def econ_data(series_id, start_date='2012-01-01', end_date='2022-12-31'):
    ensure_cache_folder('Econ_data')
    cache_filename = f"{'Econ_data'}/{series_id}_econ_cache_{start_date}_{end_date}.csv"
    if check_cache(cache_filename):
        print("Cache Found! ")
        data = read_cache(cache_filename)
    else:
        fred = Fred(api_key=Keys.api_fred)
        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
        save_cache(data, cache_filename)

    show_econ_data(data, series_id)
    return data
    # print(fred.get_series_info(seris_id))

def show_econ_data(data, series_id):
    plt.plot(data)
    plt.title(f'Economic Data for {series_id}')
    plt.xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    econ_image_path = f'static/{series_id}_econ_chart.png'
    plt.savefig(econ_image_path)
    #plt.show()
    return econ_image_path

def get_stocks_id(term):
    df = pd.read_csv('Tickers.csv')
    matched_stocks = df[df['name'].str.contains(term, case=False) | df['ticker'].str.contains(term, case=False)]
    if not matched_stocks.empty:
        stock_ID = matched_stocks.iloc[0]['ticker']
        return stock_ID
    else:
        print("Company not found")
        return False

def stock_data(company_name='AAPL', start_date='2012-01-01', end_date='2022-12-31'):
    ensure_cache_folder('Stock_data')
    cache_filename = f"{'Stock_data'}/{company_name}_stock_cache_{start_date}_{end_date}.csv"
    if check_cache(cache_filename):
        print("Cache Found! ")
        data = read_cache(cache_filename)
    else:
        stock = yf.Ticker(company_name)
        data = stock.history(start=start_date, end=end_date)
        save_cache(data, cache_filename)

    show_stock_data(data, company_name)
    return data

def show_stock_data(data, company_name):
    plt.plot(data['Close'])
    plt.title(f'{company_name} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    stock_image_path = f'static/{company_name}_stock_chart.png'
    plt.savefig(stock_image_path)
    #plt.show()
    return stock_image_path


def reddit_data(company_name, search_terms=["stock", "market", "investment"], subreddits = "all", search_limit=100):
    ensure_cache_folder('Reddit_data')
    cache_filename = f"{'Reddit_data'}/{company_name}_reddit_cache.txt"
    if check_cache(cache_filename):
        print("Cache Found!")
        words = read_reddit_cache(cache_filename)
    else:
        reddit = praw.Reddit(client_id=Keys.client_id,
                             client_secret=Keys.client_secret,
                             username='Xinyiwang_Umich',
                             password=Keys.password,
                             user_agent='PythonFinal')

        subreddit = reddit.subreddit(subreddits)
        words = []
        for term in search_terms:
            for post in subreddit.search(f'{term} {company_name}', limit=search_limit):
                words += nltk.word_tokenize(post.title)

        stop_words = set(stopwords.words('english'))
        words = [word.lower() for word in words
                  if word.isalpha()
                  and word.lower() not in stop_words
                  and " " not in word]

        save_reddit_cache(words, cache_filename)
    show_wordcloud(words, company_name)
    return words

def show_wordcloud(words, company_name):
    word_counts = Counter(words)
    #print(word_counts.most_common(10))
    wordcloud = WordCloud(width=800,
                          height=800,
                          background_color='white',
                          min_font_size=10,
                          max_words=500).generate_from_frequencies(dict(word_counts))

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    wc_image_path = f'static/{company_name}_wc_chart.png'
    plt.savefig(wc_image_path)
    #plt.show()
    return wc_image_path

def ensure_cache_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def check_cache(cache_filename):
    return os.path.exists(cache_filename)

def read_cache(cache_filename):
    return pd.read_csv(cache_filename, index_col=0, parse_dates=True)

def save_cache(data, cache_filename):
    data.to_csv(cache_filename)

def read_reddit_cache(cache_filename):
    with open(cache_filename, 'r') as file:
        return file.read().splitlines()

def save_reddit_cache(data, cache_filename):
    with open(cache_filename, 'w') as file:
        file.write('\n'.join(data))
def exit_program():
    print("Exiting Program")
    sys.exit(0)
    return "Program Exited"

@app.route("/", methods=["GET", "POST"])
def index():

    image = None
    if request.method == "POST":
        choice = request.form["choice"]
        search_term = request.form["search_term"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        if choice == "stock":
            if get_stocks_id(search_term):
                data = stock_data(search_term, start_date, end_date)
                image = show_stock_data(data, search_term)

        elif choice == "economic":
            series_data = get_series_id(search_term)
            if not series_data.empty:
                series_id = series_data.iloc[0]['id']
                data = econ_data(series_id, start_date, end_date)
                image = show_econ_data(data, series_id)
        words = reddit_data(search_term)
        wordcloud_image = show_wordcloud(words, search_term)

        return render_template('results.html', data=data, image=image, wordcloud_image=wordcloud_image)

    return render_template("index.html")

#def main():
    #get_series_id("GDP")
    #econ_data("GDP")
    #stock_data()
    #reddit_data("AAPL")
    #pass

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'static'
    app.run(debug=True, threaded=True, use_reloader=False)
    browser = webdriver.Chrome()
    app_url = "http://127.0.0.1:5000/"
    browser.get(app_url)
