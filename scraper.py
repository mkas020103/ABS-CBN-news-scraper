'''
January 4, 2024 8pm
'''

import requests
import re
import pandas as pd
from nltk.tokenize import word_tokenize
 
sites = [
    'https://news.abs-cbn.com/video/news/01/02/24/sapul-sa-cctv-rambol-sa-caloocan-nauwi-sa-pamamaril',
    'https://news.abs-cbn.com/news/01/02/24/jeepney-modernization-seen-leading-to-higher-fares',
    'https://news.abs-cbn.com/news/01/01/24/female-employee-remains-in-hospital-following-bank-crash-qcpd',
]

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
        -self.debugging()
        -self.build_df()
    '''
    def __init__(self, sites):
        if type(sites) != str:
            raise IndexError("Must be a string")
        if sites.startswith('https://news.abs-cbn.com/') or sites.startswith('http://news.abs-cbn.com/'):
            self.sites_to_scrape = [sites]
        else:
            self.tempdf= pd.read_csv(sites)
            self.sites_to_scrape = self.tempdf.iloc[:, 0].tolist()
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.df = None
        self.html_content = []
        self.title = []
        self.authors = []
        self.contents = []
        self.dates = []
        
        # Call methods that scrapes, pre-clean, build the final dataframe
        self.html_content_scrape()
        self.scrape_essential_content()
        self.tokens = [word_tokenize(text) for text in self.contents]
        #self.debugging()
        self.build_df()
        
    def html_content_scrape(self):
        '''
        scrapes the html content of ABS-CBN returns the error code if it failed to scrape the data.
        '''
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
        # Regular expression to each crucial data
        news_title_pattern = r'<h1 class="news-title">(.*?)</h1>'
        author_pattern = r'<span class="editor">(.*?)</span>'
        content_pattern = r'<p(?:\s+style)?>\s*(.*?)\s*</p>'
        date_pattern = r'<span class="date-posted">(.*?)</span>'
        
        for content in self.html_content:
            # Search for a match in the HTML with their respective regular expression
            if not content.startswith('Status code erorr:') or not content.startswith('Not an ABSCBN site.'):
                news_title_match = re.search(news_title_pattern, content)
                author_match = re.search(author_pattern, content)
                content_match = re.findall(content_pattern, content, re.DOTALL)
                date_match = re.search(date_pattern, content)
            else:
                self.title.append(None)
                self.authors.append(None)
                self.contents.append(None)
                self.dates.append(None)
                continue
            
            # Check if there was content found for each data then append
            self.title.append(news_title_match.group(1) if news_title_match else '**No News Title Found**')
            self.authors.append(author_match.group(1) if author_match else '**No Author Found**')
            self.dates.append(date_match.group(1) if date_match else '**No Date Found**')

            if content_match:
                all_content = ' '.join(content_match)
                self.contents.append(all_content)
            else:
                self.contents.append('**No Content Found**')
                
    def build_df(self):
        data = {
            'links':self.sites_to_scrape,
            'titles':self.title,
            'authors':self.authors,
            'date':self.dates,
            'contents':self.contents,
            'content_tokens':self.tokens
        }
        self.df = pd.DataFrame(data)
                
                
    def print(self):
        print(self.df.head())
    
    def debugging(self):
        print('links: {}\ntitle: {}\nauthors: {}\ncontents: {}\ndates: {}\n'.format(self.sites_to_scrape, self.title, self.authors, self.contents, self.dates))
        print('links: {}\ntitle: {}\nauthors: {}\ncontents: {}\ndates: {}\ntokens: {}'.
              format(len(self.sites_to_scrape), len(self.title), len(self.authors), len(self.contents), len(self.dates), len(self.tokens)))

        
x = scrape('sites.csv')
x.print()