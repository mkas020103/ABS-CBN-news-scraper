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

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scraper():
    if request.method == 'POST':
        sites = request.form.get('site')  # get the csv or link from the form in index.html 
        print(type(sites))
        news_scraper = scrape(sites)  # scrape the news using the scrape class
        scraped_data = news_scraper.df.to_dict(orient='records')  # dataframe to dictionary
        return jsonify(scraped_data)  # return the scraped_data as JSON

'''
def main():
    # scrape dataframe 
    x = scrape('sites.csv') #change into a csv file or site link
    x.save('uncleaned.csv')
    
    # clean dataframe
    y_data = copy.copy(x.df)
    y = clean(y_data)
    y.save('cleaned.csv')

'''

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/functions')
def func():
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
    

