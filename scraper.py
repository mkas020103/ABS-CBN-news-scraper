import requests
import re
import pandas as pd
 
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
    '''
    def __init__(self, sites, text_or_csv: int):
        self.text_or_csv = text_or_csv # 1 if text 0 if csv
        if self.text_or_csv == 1:
            self.sites_to_scrape = sites
        elif self.text_or_csv == 0:
            self.df= pd.read_csv('sites')
            self.sites_to_scrape = self.df.iloc[:, 0].tolist()
        else:
            return '\'text_or_csv\' parameter must be either 1 or 0.'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.html_content = []
        self.title = []
        self.authors = []
        self.contents = []
        self.dates = []
        
    def html_content_scrape(self):
        '''
        scrapes the html content of ABS-CBN returns the error code if it failed to scrape the data.
        '''
        for site in self.sites_to_scrape:
            response = requests.get(site, headers=self.header)
            if response.status_code == 200:
                self.html_content.append(response.text)
            else:
                self.html_content.append("Status code erorr: {}.".format(response.status_code))
                
    def scrape_essential_content(self):
        # Regular expression to each crucial data
        news_title_pattern = r'<h1 class="news-title">(.*?)</h1>'
        author_pattern = r''
        content_pattern = r''
        date_pattern = r''
        
        for content in self.html_content:
            # Search for a match in the HTML
            news_title_match = re.search(news_title_pattern, content)
            author_match = re.search(news_title_pattern, content)
            content_match = re.search(news_title_pattern, content)
            date_match = re.search(news_title_pattern, content)
            
            # Check if there was a content found for each data then append
            if news_title_match:
                self.title.append(news_title_match.group(1))
            else:
                self.title.append('**No News Title Found**')