'''
January 31, 2024 4am
'''

import requests
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
        self.html_title_text_finder = '<div class="MuiTypography-root MuiTypography-h1 css-bz0a2f'
        self.html_author_text_finder = '<div class="MuiTypography-root MuiTypography-h5 MuiTypography-gutterBottom css-vldcmf'
        self.html_content_text_finder = '\\u003cp'
        self.html_date_text_finder = '<div class="MuiTypography-root MuiTypography-h5 css-37gmgr'
        self.title_ender = '</div'
        self.author_ender = '</div'
        self.content_ender = '\\u003c/p\\u003e\\'
        self.date_ender = '</div'
        self.top_content = 'body_html_top'
        self.lower_content = 'href='
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
        # Tokenize the contents and build the dataframe
        self.contents = [text.strip() for text in self.contents]
        #self.tokens = [text.split() for text in self.contents]
        self.build_df()
        
    def html_content_scrape(self):
        '''
        scrapes the html content of ABS-CBN returns the error code if it failed to scrape the data.
        '''
        # Iterate over each site then append html text if everything works properly
        for site in self.sites_to_scrape:
            if site.startswith('https://news.abs-cbn.com/') or site.startswith('http://news.abs-cbn.com/'):
                # Send a GET request to the specified URL
                response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

                # Check if the request was successful (status code 200)
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
            tag = ''
            
            # Initialize flags for important html contents
            is_title = False
            is_author = False
            is_content = False
            is_date = False
            is_tag = False
            date_encoutered = False
            can_scrape_content = False

            # Iterate over the whole html content while saving the important parts
            all_content = []
            for char in content:
                # Content finder (for debugging)
                overall_content_start = temp_str[-len(self.top_content):]
                overall_content_end = temp_str[-len(self.lower_content):]
                
                # If character is in html tag and not part of other important content 
                if char == '<' and not is_date and not is_content and not is_author and not is_title:
                    is_tag = not is_tag
                # Else if character is in html tag and part of other important content
                elif char == '<' and (is_date or is_content or is_author or is_title):
                    is_title = False
                    is_author = False
                    is_content = False
                    is_date = False
                    is_tag = False
                # If character is end of html tag and not part of other important content
                if char == '>' and (not is_date or not is_content or not is_author or not is_title) and is_tag:
                    # reset tag value
                    tag = ''
                    is_tag = not is_tag
                    temp_str += char
                    continue
                # If part of an important content
                if (is_date or is_content or is_author or is_title) and not is_tag:
                    # If a character is an important html content, append
                    if is_title:
                        title += char
                        temp_str += char
                        continue
                    elif is_author:
                        authors += char
                        temp_str += char
                        continue
                    elif is_content:
                        contents += char
                    elif is_date:
                        dates += char
                        temp_str += char
                        continue
                # Scrape content after date
                if date_encoutered:
                    # If its the start of the content area in an html
                    if overall_content_start == self.top_content:
                        can_scrape_content = not can_scrape_content
                    if overall_content_end == self.lower_content and can_scrape_content:
                        can_scrape_content = not can_scrape_content
                        break
                    
                    if can_scrape_content:
                        # is part of the content
                        start = temp_str[-len(self.html_content_text_finder):]
                        end = temp_str[-len(self.content_ender):]
                        if start == self.html_content_text_finder and not is_content:
                            is_content = not is_content
                        elif end == self.content_ender:
                            is_content = not is_content
                            all_content.append(contents)
                            contents = ''
                if is_tag:
                    tag += char
                    temp_str += char
                    # If no important tag is found yet keep checking
                    if not is_title or not is_author or not is_date or not is_content:
                        if tag == self.html_title_text_finder:
                            is_title = not is_title
                            continue
                        if tag == self.html_author_text_finder and not is_author:
                            is_author = not is_author
                            continue
                        if tag == self.html_date_text_finder and not is_date:
                            is_date = not is_date
                            date_encoutered = True
                            continue
                else:
                    temp_str += char
            
            # Check if there was content found for each data then append
            self.title.append(title[:len(title)] if title else '**No News Title Found**')
            self.authors.append(authors[:len(authors)] if authors else '**No Author Found**')
            self.dates.append(dates if dates else '**No Date Found**')
            self.contents.append(' '.join(all_content) if all_content else '**No Content Found**')  
                    
                
    def build_df(self):
        # Plot the data
        data = {
            'links':self.sites_to_scrape,
            'titles':self.title,
            'authors':self.authors,
            'date':self.dates,
            'contents':self.contents,
            #'content_tokens':self.tokens
        }
        self.df = pd.DataFrame(data)

    def return_copy(self):
        return self.df.copy()
                
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
