from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from bs4 import BeautifulSoup
import datetime
import pandas as pd

EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as file time
HUNDREDS_OF_NANOSECONDS = 10000000

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--headless')
options.add_argument("--log-level=3") 

options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)

def publication_date_from_epox(publication_time_epox):
    def filetime_to_dt(ft):
        us = (ft - EPOCH_AS_FILETIME) // 10  # microseconds
        return datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=us)


    timestamp_hundreds_of_nanoseconds = publication_time_epox * 10000
    publication_date = filetime_to_dt(EPOCH_AS_FILETIME + timestamp_hundreds_of_nanoseconds)

    return publication_date.strftime("%Y/%m/%d")

def scrap_data(book_id):
    try:
        url = 'https://www.goodreads.com/book/show/' + str(book_id)
        done = False
        while not done:
            driver.get(url)
            if 'First published ' in driver.page_source:
                done = True
            if not done:
                time.sleep(0.01)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        script_tag = soup.find("script", type="application/ld+json")
        json_data = script_tag.string
        data = json.loads(json_data)
        authors_ = [author['url'].split('/')[-1] for author in data['author']]
        author_numbers = [author.split('.')[0] for author in authors_]
        authors = '/'.join(author_numbers)
        aggregate_rating = data.get('aggregateRating', None)
        average_rating = aggregate_rating.get('ratingValue', None)
        ratings_count = aggregate_rating.get('ratingCount', None)
        text_reviews_count = aggregate_rating.get('reviewCount', None)

        book_data_= json.loads(soup.find(id="__NEXT_DATA__").text)
        book_ref = book_data_['props']['pageProps']['apolloState']['ROOT_QUERY'][f'getBookByLegacyId({{"legacyId":"{book_id}"}})']['__ref']
        work_ref = book_data_['props']['pageProps']['apolloState'][book_ref]['work']['__ref']

        publication_time_epox = book_data_['props']['pageProps']['apolloState'][work_ref]['details']['publicationTime']
        # Use the function for negative timestamps
        if publication_time_epox < 0:
            publication_date = publication_date_from_epox(publication_time_epox)
        else:  # it's a positive timestamp
            publication_date = datetime.datetime.fromtimestamp(publication_time_epox / 1000).strftime("%Y/%m/%d")
        num_pages = book_data_['props']['pageProps']['apolloState'][book_ref]['details'].get('numPages'),
        isbn = book_data_['props']['pageProps']['apolloState'][book_ref]['details'].get('isbn'), 
        isbn13 = book_data_['props']['pageProps']['apolloState'][book_ref]['details'].get('isbn13'),
        language_code = book_data_['props']['pageProps']['apolloState'][book_ref]['details']['language'].get('name'),

        if book_data_ is None:
            script_tag_ = soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
            json_data_ = script_tag_.string
            data_ = json.loads(json_data_)
            book_id_key = f'getBookByLegacyId({{"legacyId":"{book_id}"}})'
            book_ref = data_['props']['pageProps']['apolloState']['ROOT_QUERY'][book_id_key]['__ref']
            work_ref = data_['props']['pageProps']['apolloState'][book_ref]['work']['__ref']
            publication_time_epox = data_['props']['pageProps']['apolloState'][work_ref]['details']['publicationTime']
        
            # Use the function for negative timestamps
            if publication_time_epox < 0:
                publication_date = publication_date_from_epox(publication_time_epox)
            else:  # it's a positive timestamp
                publication_date = datetime.datetime.fromtimestamp(publication_time_epox / 1000).strftime("%Y/%m/%d")

            num_pages = data_['props']['pageProps']['apolloState'][book_ref]['details'].get('numPages')
            isbn = data_['props']['pageProps']['apolloState'][book_ref]['details'].get('isbn')
            isbn13 = data_['props']['pageProps']['apolloState'][book_ref]['details'].get('isbn13')
            language_code = data_['props']['pageProps']['apolloState'][book_ref]['details']['language'].get('name')

        return {
            'num_pages': num_pages,
            'isbn': isbn,
            'isbn13': isbn13,
            'publication_date': publication_date,
            'average_rating': average_rating,
            'ratings_count': ratings_count,
            'text_reviews_count': text_reviews_count ,
            'publication_year': datetime.datetime.strptime(publication_date, "%Y/%m/%d").year if publication_date else None,
            'publication_month': datetime.datetime.strptime(publication_date, "%Y/%m/%d").month if publication_date else None,
            'publication_day': datetime.datetime.strptime(publication_date, "%Y/%m/%d").day if publication_date else None,
            'language_code': language_code,
            'authors': authors
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # This will print the traceback
        print(f"Error occurred for book ID: {book_id}")
        print(str(e))
        return None

df = pd.read_csv('test.csv', sep='|')

for index, row in df.iterrows():
    book_data = scrap_data(row['book_id'])

df.to_csv('test_updated.csv', sep='|', index=False)