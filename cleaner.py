import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from scraper import scrape
import os

class clean:
    def __init__(self, df):
        self.df = df
        self.tokens = []
        self.tokenizer = RegexpTokenizer(r'\b(?:[a-zA-Z]+\d+|\d+[a-zA-Z]+)\b')
        self.patterns = [
            [r'<a href="/"share',''],
            [r'share$',''],
            [r'&mdash;','—'],
            [r'&#;','\''],
            [r'&#39;','\''],    
            [r'&quot','"'],
            [r'.&nbsp;',','],
            [r'<strong',''],
            [r'</strong',''],
        ]
        self.preprocess()
        
        
    def preprocess(self):
        for _, row in self.df.iterrows():
            for pattern in self.patterns:
                row['contents'] = row['contents'].strip().lower()
                row['contents'] = re.sub(pattern[0], pattern[1], row['contents'])
        self.tokenize()
        
    def substitute(self, list_of_text):
        for _, row in self.df:
            for text in list_of_text:
                row['contents'] = re.sub(text[0], text[1], row['contents'])
        self.tokenize()
        
    def find(self, pattern):
        self.expression = r'\b{}\b'.format(pattern)  # Regular expression pattern to match the word or words
        self.filtered_comments = self.df[self.df['contents'].str.contains(self.expression, case=False, regex=True)]

    def tokenize(self):
        self.tokens = [self.tokenizer.tokenize(text) for text in self.df['contents']]
        self.df['content_tokens'] = self.tokens
        
    def save(self, filename):
        if filename.endswith('.csv') and all(char not in '&*^%$#@!\'"\\/' for char in filename):
            # Get the current working directory
            current_path = os.getcwd()

            # Full path to the CSV file
            csv_file_path = os.path.join(current_path, filename)
            
            self.df.to_csv(csv_file_path)
        else:
            print('Must be a valid filename that ends with .csv')