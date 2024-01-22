from cleaner import clean
from scraper import scrape
import pandas as pd
import time

def main():
    # scrape dataframe 
    x = scrape('sites.csv')
    
    # clean dataframe
    y = clean(x.df)
    
    # save files
    x.save('uncleaned.csv')
    y.save('cleaned.csv')

if __name__ == '__main__':
    main()