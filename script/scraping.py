import json
import pandas as pd

filename = "goodreads_books.json"
output_filename = "goodreads_books.csv"

# Define the column names
column_names = ['title', 'num_pages', 'authors', 'publisher', 'publication_date', 'publication_year', 'publication_month', 'publication_day', 'country_code', 'language_code', 'average_rating', 'text_reviews_count', 'ratings_count']

# Open the CSV file in write mode
with open(output_filename, 'w') as csv_file:
    # Create a CSV writer object
    df = pd.DataFrame(columns = column_names)
    df.to_csv(csv_file, index=False)

# Open the CSV file in append mode
with open(output_filename, 'a', encoding='utf-8') as csv_file:
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            book = json.loads(line)
            isbn = int(book['isbn']) if book['isbn'].isdigit() else None
            isbn13 = int(book['isbn13']) if book['isbn13'].isdigit() else None
            title = book['title']
            num_pages = int(book['num_pages']) if book['num_pages'].isdigit() else None
            # Extract only the author_id values and join them into a single string
            authors = ",".join([author['author_id'] for author in book['authors']])
            publisher = book['publisher']
            publication_date = f"{book['publication_year']}/{book['publication_month']}/{book['publication_day']}"
            publication_year = int(book['publication_year']) if book['publication_year'].isdigit() else None
            publication_month = int(book['publication_month']) if book['publication_month'].isdigit() else None
            publication_day = int(book['publication_day']) if book['publication_day'].isdigit() else None
            country_code = book['country_code']
            language_code = book['language_code']
            average_rating = float(book['average_rating']) if book['average_rating'].replace('.', '', 1).isdigit() else None
            text_reviews_count = int(book['text_reviews_count']) if book['text_reviews_count'].isdigit() else None
            ratings_count = int(book['ratings_count']) if book['ratings_count'].isdigit() else None

            # Count the number of authors
            authors_count = authors.count(",") + 1

            # Write the data to the CSV file
            df = pd.DataFrame([[title, num_pages, authors, publisher, publication_date, publication_year, publication_month, publication_day, country_code, language_code, average_rating, text_reviews_count, ratings_count, authors_count]], columns=column_names + ['authors_count'])
            df.to_csv(csv_file, header=False, index=False, encoding='utf-8')
