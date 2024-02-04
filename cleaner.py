'''
February 1, 2024 4am
'''

import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import os

class clean:
    def __init__(self, df):
        self.df = df
        self.tokens = []
        self.tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
        self.patterns = [
            [r'id.*\\\\\\',''],
            [r'/span',''],
            [r'\\u003c',''],
            [r'/em',''],
            [r'<br',''],
            [r'\\u003ekj',''],
            [r'u003e',''],
            [r'"',''],
            [r'\\u0026','\''],
            [r'&mdash;','—'],
            [r';',''],
            [r'&#;','\''],
            [r'&#39;','\''],    
            [r'&quot','"'],
            [r'.&nbsp;',','],
            [r'<strong',''],
            [r'</strong',''],
            [r'\\',''],
            [r'/pu',''],
            [r'/p',''],
            [r'quot',''],
            [r'\bbr\b',''],
            [r'\'ldquo',''],
            [r'\'lde','T'],
            [r'\'',''],
            [r'rsquo',''],
            [r'rdquo',''],
            [r'#39',''],
            [r',',''],
            [r'\.',''],
            [r'\?',''],
            [r'\!',''],
            [r'--',''],
            [r'id=ispasted',''],
            [r'/',''],
            [r'=',''],
            [r'body_html_middle',''],
            [r'body_html_mddle',''],
            [r'strong',''],
            [r':',''],
            [r'-',''],
            [r'body_html_mdle',''],
            [r'&#x27',''],
            [r'\(miff\)',''],
            [r'\b\w*dataivske\w*\b',''],
            [r'\b\w*ivsplayer\w*\b',''],
            [r'\b\w*datawsci\w*\b',''],
            [r'\b\w*dataws\w*\b',''],
            [r'\b\w*datascay\w*\b',''],
        ]
        self.preprocess()
        self.tokenize()
        
        
    def preprocess(self):
        for _, row in self.df.iterrows():
            for pattern in self.patterns:
                row['contents'] = row['contents'].strip().lower()
                row['contents'] = re.sub(pattern[0], pattern[1], row['contents'])
                row['titles'] = row['titles'].strip().lower()
                row['titles'] = re.sub(pattern[0], pattern[1], row['titles'])
        
    def substitute(self, list_of_text):
        try:
            list_of_text = self.parse_input_string(list_of_text)
        except:
            raise ValueError("Wrong format")
        for index, row in self.df.iterrows():
            for text in list_of_text:
                row['contents'] = re.sub(text[0], text[1], row['contents'])
            # Set the modified value back to the DataFrame
            self.df.at[index, 'contents'] = row['contents']
        self.tokenize()

    def parse_input_string(self, whole_string):
            list_of_text = []
            current_pair = []
            inside_pair = False

            for char in whole_string:
                if char == '(':
                    inside_pair = True
                    current_pair = []
                elif char == ')':
                    if inside_pair:
                        inside_pair = False
                        key, value = map(str.strip, ''.join(current_pair).split(':'))
                        list_of_text.append((key, value))
                    else:
                        # Handle the case where ')' is encountered without '('
                        raise ValueError("Mismatched parentheses in the input string.")
                elif inside_pair:
                    current_pair.append(char)

            if inside_pair:
                # Handle the case where there are unmatched '('
                raise ValueError("Mismatched parentheses in the input string.")
        
            x = list_of_text[0]
            print(list_of_text)
            print(type(list_of_text))
            print(x)
            print(type(x))
            print(x[1])
            print(type(x[1]))
            return list_of_text

        
    def find(self, pattern):
        self.expression = r'\b{}\b'.format(pattern)  # Regular expression pattern to match the word or words
        self.filtered_comments = self.df[self.df['contents'].str.contains(self.expression, case=False, regex=True)]
        if not self.filtered_comments.empty:
            self.df=self.filtered_comments
        else:
            self.df

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






'''from scraper import scrape
            
x = scrape('sites.csv')
x.save('uncleaned.csv')

y = x.return_copy()

z = clean(y)
z.substitute('(president:mr pres)')

print(z.df.head())
z.save('cleaned.csv')'''
