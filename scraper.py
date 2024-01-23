'''
January 23, 2024 7pm
'''

import requests
import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import os

class scrape:
    '''
    Functions:
        - Accepts only ABS-CBN sites.
        - Scrapes the whole html content of the ABS-CBN site.
        - Saves only the crucial contents like the author, date, news into a CSV file.
    
    Parameters:
        - CSV file: contains the links of all ABS-CBN news or articles.
        - Text (str): a simple string containing a valid link to a site.
        
    Attribute:
        -self.sites_to_scrape
        -self.header
        -self.df
        -self.html_content
        -self.title
        -self.authors
        -self.contents
        -self.dates
        -self.tokens
        
    Methods:
        -self.html_content_scrape()
        -self.scrape_essential_content()
        -self.build_df()
    '''
    def __init__(self, sites):
        if type(sites) != str:
            raise IndexError("Must be a string")
        if sites.startswith('https://news.abs-cbn.com/') or sites.startswith('http://news.abs-cbn.com/'):
            self.sites_to_scrape = [sites]
        else:
            try:
                self.tempdf= pd.read_csv(sites)
            except:
                raise Exception("No File Found: {}".format(sites))
            self.sites_to_scrape = self.tempdf.iloc[:, 0].tolist()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.df = None
        self.html_content = []
        self.title = []
        self.authors = []
        self.contents = []
        self.dates = []
        self.tokens = []
        
        # Call methods that scrapes, pre-clean, build the final dataframe
        self.html_content_scrape()
        self.scrape_essential_content()
        self.tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+')
        # Tokenize the contents and build the dataframe
        self.contents = [text.strip() for text in self.contents]
        self.tokens = [self.tokenizer.tokenize(text) for text in self.contents]
        self.build_df()
        
    def html_content_scrape(self):
        '''
        scrapes the html content of ABS-CBN returns the error code if it failed to scrape the data.
        '''
        # Iterate over each site then append html text if everything works properly
        for site in self.sites_to_scrape:
            if site.startswith('https://news.abs-cbn.com/') or site.startswith('http://news.abs-cbn.com/'):
                response = requests.get(site, headers=self.header)
                if response.status_code == 200:
                    self.html_content.append(response.text)
                else:
                    self.html_content.append("Status code erorr: {}.".format(response.status_code))
            else:
                self.html_content.append("Not an ABSCBN site.")
                
    def scrape_essential_content(self):
        for content in self.html_content:
            # Check if the content has a valid data to scrape
            if content.startswith('Status code erorr:'):
                self.title.append('**No News Title Found**')
                self.authors.append('**No Author Found**')
                self.dates.append('**No Date Found**')
                self.contents.append('**No Content Found**')
                break
            
            # Initialize string for each important html content
            title = ''
            authors = ''
            contents = ''
            dates = ''
            temp_str = ''
            
            # Initialize flags for important html contents
            is_title = False
            is_author = False
            is_content = False
            is_date = False
            number_dates = 1
            
            # Iterate over the whole html content while saving the important parts
            for char in content:
                # If a probable important html content
                if char  == '>' or is_title or is_author or is_content or is_date:
                    # If a character is probably a closing to a code in html
                    if char == '>':
                        start_date_match = temp_str[-len('<span class="date-posted"'):]
                        start_content_match = temp_str[-len('<p'):]
                        start_author_match = temp_str[-len('<span class="editor"'):]
                        start_title_match = temp_str[-len('<h1 class="news-title"'):]
                        end_date_match = dates[-len('</span'):]
                        end_content_match = contents[-len('</p'):]
                        end_author_match = temp_str[-len('</span'):]
                        end_title_match = temp_str[-len('</h1'):]
                        
                        # If a start of an important html content
                        if start_title_match == '<h1 class="news-title"':
                            is_title = not is_title
                        if start_author_match == '<span class="editor"':
                            is_author = not is_author
                        if start_content_match == '<p':
                            is_content= not is_content
                            if end_content_match == '</p':
                                contents = contents[:len(contents)-3]
                        if start_date_match == '<span class="date-posted"'and number_dates <= 2:
                            is_date= not is_date
                            number_dates += 1
                            if end_date_match == '</span':
                                dates = dates[:len(dates)-6]
                            
                        # If an end of an important html content, append then re-initialize
                        if start_title_match == True and end_title_match == '</h1':
                            is_title = not is_title
                        if start_author_match == True and end_author_match == '</span':
                            is_author = not is_author
                            
                    # If a character is an important html content, append
                    elif is_title:
                        title += char
                    elif is_author:
                        authors += char
                    elif is_content:
                        contents += char
                    elif is_date:
                        dates += char
                # Else append the character
                else:
                    temp_str += char
            
            # Check if there was content found for each data then append
            self.title.append(title[:len(title)-4] if title else '**No News Title Found**')
            self.authors.append(authors[:len(authors)-6] if authors else '**No Author Found**')
            self.dates.append(dates if dates else '**No Date Found**')
            self.contents.append(contents if contents else '**No Content Found**')  
                    
                
    def build_df(self):
        # Plot the data
        data = {
            'links':self.sites_to_scrape,
            'titles':self.title,
            'authors':self.authors,
            'date':self.dates,
            'contents':self.contents,
            'content_tokens':self.tokens
        }
        self.df = pd.DataFrame(data)
                
    def save(self, filename):
        # If the filename is valid, save into csv file
        if filename.endswith('.csv') and all(char not in '&*^%$#@!\'"\\/' for char in filename):
            # Get the current working directory
            current_path = os.getcwd()

            # Full path to the CSV file
            csv_file_path = os.path.join(current_path, filename)
            
            self.df.to_csv(csv_file_path)
        else:
            print('Must be a valid filename that ends with .csv')