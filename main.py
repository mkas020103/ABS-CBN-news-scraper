'''
January 23, 2024 7pm
'''

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

if __name__ == '__main__':
    main()