'''
January 23, 2024 7pm
'''
from flask import Flask, request, render_template, redirect, url_for, jsonify
from cleaner import clean
from scraper import scrape
import pandas as pd
import time
import copy

from flask import Flask, request, render_template, redirect, url_for, jsonify
from scraper import scrape
from cleaner import clean

app = Flask(__name__)

news_cleaner = None

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST','GET'])
def scraper():
    if request.method == 'POST' or request.method == 'GET':
        sites = request.form.get('sites_to_scrapes')  # get the csv or link from the form in index.html 
        news_scraper = scrape(sites)  # scrape the news using the scrape class
        global news_cleaner
        news_cleaner = clean(news_scraper.return_copy())
        return render_template("functions.html", data=news_cleaner.df.to_dict(orient='records'))
        
@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/functions', methods=['POST'])
def func():
    if request.method == 'POST':
        subs = request.form.get('substitute_words') # get the words to be substituted
        find = request.form.get('words_to_find')    # get the words to be find

        return render_template('functions.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':   
    app.run(debug=True)
    

'''
            
x = scrape('sites.csv')
x.save('uncleaned.csv')

y = x.return_copy()

z = clean(y)

print(z.df.head())
z.save('cleaned.csv')
'''