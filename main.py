'''
January 23, 2024 7pm
'''
from flask import Flask, request, render_template, redirect, url_for, jsonify
from cleaner import clean
from scraper import scrape
import pandas as pd
import time
import copy

def main():
    # scrape dataframe 
    x = scrape('sites.csv') #change into a csv file or site link
    x.save('uncleaned.csv')
    
    # clean dataframe
    y_data = copy.copy(x.df)
    y = clean(y_data)
    y.save('cleaned.csv')

'''

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods = ['POST'])
def scraper():
    if request.methods == 'POST':
        sites = request.form.get('sites')
        scraper = scrape(sites)
        return 

@app.route('/cleaner')
def cleaner():
    return render_template('cleaner.html')

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/sub')
def substitute():
    return render_template('sub.html')
 
'''


if __name__ == '__main__':
    main()

