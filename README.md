# ABS-CBN-news-scraper
A project was developed to scrape the contents of ABS-CBN and preprocess the content through regular expression for a school project.

## main.py
  - Main program that connects the frontend and backend

## cleaner.py
  - a program that cleans the scrape data from scraper.py by removing irrelevant words and normalizing the text data.
  - uses regular expressions to create synthetic data.
  - tokenizes the scraped data using regular expression.

## scraper.py
  - scrapes a text containing the link of a valid ABS-CBN news or a CSV file containing the links.
  - searches for a match of the title, author, content, and timestamp using regular expressions.
