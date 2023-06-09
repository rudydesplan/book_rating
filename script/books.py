#Import Required Libraries

#from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import pandas as pd
from pyarrow import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#We can disregard :
# bookID: This is simply an identifier and should not have an impact on the rating of a book. It doesn't carry any useful semantic information.
# isbn and isbn13: These are also identifiers, meant for cataloging and distribution purposes, and won't influence a book's rating.


# PyArrow

def handle_invalid_row_pyarrow(row):
    # You can implement your own logic here to decide whether to skip or raise an error for the invalid row
    return "skip"

## Create ParseOptions with the invalid_row_handler set to the custom function
parse_options = csv.ParseOptions(invalid_row_handler=handle_invalid_row_pyarrow)
df_pyarrow_table = csv.read_csv('books.csv',parse_options=parse_options)

#Pandas

## Load the Dataset

bad_lines = []
def handle_bad_line(line):
    # Append the bad line to the list
    bad_lines.append(line)
    
df = pd.read_csv('books.csv', on_bad_lines=handle_bad_line , engine="python")

## Specify the columns to convert to lowercase
columns_to_lowercase = ['title', 'authors', 'language_code', 'publisher']

## Convert the specified columns to lowercase
df[columns_to_lowercase] = df[columns_to_lowercase].apply(lambda x: x.str.lower())


## Initial Data Exploration

### Create a DataFrame from the bad lines

#bad_lines_df = pd.DataFrame({'Bad Line': bad_lines})
#print(bad_lines_df)

## Bad_lines handling - For each BookID , connect to the API and get the correct data

### First few rows of the dataset
#print(df.head())

## Display the shape of the dataset
#print(df.shape)

## Display the data types of each column
#print(df.dtypes)

## Summary statistics of numerical columns
#print(df.describe())

# Data Cleaning and Preprocessing

# Get the numerical columns
#numerical_columns = df.select_dtypes(include='number').columns

# Count rows with negative values in numerical columns
#count_negative_rows = (df[numerical_columns] < 0).any(axis=1).sum()

# Print the count of rows with negative values
#print("Count of rows with negative values:", count_negative_rows)

## Check for missing values
#print(df.isnull().sum())

## Check for duplicate values
#print(df.duplicated().sum())

## Datetime handling
# Create a copy of the original dates
original_dates = df['publication_date'].copy()

# Attempt to convert the dates
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%m/%d/%Y', errors='coerce')

# Find the rows where the conversion failed
failed_rows = df['publication_date'].isna()

## Easy solution - For each failed row, attempt to adjust the day and convert again
for idx in original_dates[failed_rows].index:
    # Split the date into month, day, and year
    month, day, year = original_dates.loc[idx].split('/')
    
    # If the day is 31, change it to 30
    if day == '31':
        day = '30'
    
    # Attempt to convert the adjusted date
    try:
        df.loc[idx, 'publication_date'] = pd.to_datetime(f'{month}/{day}/{year}', format='%m/%d/%Y')
    except ValueError:
        # If there's still an error, you could either leave it as NaT, or handle it in some other way
        pass
    
## Other solution - connect to the API and get the publication date for the specific BookID

#Title length
df['title_length'] = df['title'].apply(len)

# Find the maximum number of authors for any book
max_authors = df['num_authors'].max()

# For each number up to max_authors, create a new column and populate it with the author names
for i in range(max_authors):
    df[f'author_{i+1}'] = df['authors'].apply(lambda x: x.split('/')[i] if len(x.split('/')) > i else None)

## Investigate the relationship between the average rating and the authors' names.
# Generate summary statistics for each author
for i in range(1, max_authors + 1):
    author_stats = df.groupby(f'author_{i}')['average_rating'].describe()
    print(author_stats)
    
# Visualize the average ratings for each author
for i in range(1, max_authors + 1):
    plt.figure(figsize=(10,5))
    sns.boxplot(x=f'author_{i}', y='average_rating', data=df)
    plt.title(f'Average Ratings by Author {i}')
    plt.xticks(rotation=90)
    plt.show()

# Count the different unique values in the language_code column
language_counts = df['language_code'].value_counts()

# Display the counts
#print(language_counts)

# Filter rows with specific language codes
valid_language_codes = ['eng', 'en-us', 'en-gb', 'en-ca']
df = df[df['language_code'].isin(valid_language_codes)]

#We can disregard the colum language_code as all the books are in english:
# Delete the language_code column
df = df.drop('language_code', axis=1)


###Data Visualization
##Histogram of the book ratings:
#plt.hist(df['average_rating'], bins=10)
#plt.xlabel('Average Rating')
#plt.ylabel('Count')
#plt.title('Distribution of Book Ratings')
#plt.show()

## Scatter plot of average rating vs. number of pages
#plt.scatter(df['num_pages'], df['average_rating'])
#plt.xlabel('Number of Pages')
#plt.ylabel('Average Rating')
#plt.title('Average Rating vs. Number of Pages')
#plt.show()

## Bar chart of the top 10 publishers based on the number of books
#top_publishers = df['publisher'].value_counts().nlargest(10)
#plt.bar(top_publishers.index, top_publishers.values)
#plt.xlabel('Publisher')
#plt.ylabel('Number of Books')
#plt.title('Top 10 Publishers by Number of Books')
#plt.xticks(rotation=45)
#plt.show()

#Explore the relationship between the number of ratings/reviews and the average rating.

# Scatter plot of average rating vs. number of ratings
#plt.scatter(df['ratings_count'], df['average_rating'])
#plt.xlabel('Number of Ratings')
#plt.ylabel('Average Rating')
#plt.title('Average Rating vs. Number of Ratings')
#plt.show()

# Scatter plot of average rating vs. number of text reviews
#plt.scatter(df['text_reviews_count'], df['average_rating'])
#plt.xlabel('Number of Text Reviews')
#plt.ylabel('Average Rating')
#plt.title('Average Rating vs. Number of Text Reviews')
#plt.show()


#Analyze the distribution of book publication dates by year month.

# Bar chart of the count of books published each year
#year_counts = df['publication_year'].value_counts().sort_index()
#plt.bar(year_counts.index, year_counts.values)
#plt.xlabel('Year')
#plt.ylabel('Number of Books')
#plt.title('Distribution of Books by Year')
#plt.xticks(rotation=45)
#plt.show()

# Bar chart of the count of books published each month
#month_counts = df['publication_month'].value_counts().sort_index()
#plt.bar(month_counts.index, month_counts.values)
#plt.xlabel('Month')
#plt.ylabel('Number of Books')
#plt.title('Distribution of Books by Month')
#plt.xticks(rotation=45)
#plt.show()

## ## Interaction features : 

#Interaction between average_rating and num_pages: 
# Calculate interaction features
df['avg_rating_per_page'] = df['average_rating'] / df['num_pages'].replace(0, np.nan)
df['ratings_count_per_page'] = df['ratings_count'] / df['num_pages'].replace(0, np.nan)
df['reviews_count_per_page'] = df['text_reviews_count'] / df['num_pages'].replace(0, np.nan)

df['reviews_per_avg_rating'] = df['text_reviews_count'] / df['average_rating'].replace(0, np.nan)
df['ratings_per_point'] =df['ratings_count'] / df['average_rating'].replace(0, np.nan)

## Review Density: Calculate the ratio of text_reviews_count to ratings_count.
## It could indicate the level of engagement or the depth of readers' opinions, which might be correlated with the book's rating.
# Calculate the number of zeros in each column
num_zeros_ratings = (df['ratings_count'] == 0).sum()
num_zeros_reviews = (df['text_reviews_count'] == 0).sum()

# Choose the column with fewer zeros as the denominator
if num_zeros_ratings < num_zeros_reviews:
    df['review_density'] = df['text_reviews_count'] / df['ratings_count'].replace(0, np.nan)
else:
    df['review_density'] = df['ratings_count'] / df['text_reviews_count'].replace(0, np.nan)


## This might capture readers' perception of the book's quality relative to its length.

# Triangle correlation heatmap
# Calculate the correlation matrix
corr_matrix = df.corr()
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr_matrix, cmap=cmap, vmax=.3, center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})

# Show the plot
plt.show()

## Author Label Encoding remplace author by IDs

# Create a set to store unique author names
unique_authors = set()

# Split the 'authors' strings by '/' and add the authors to the set
df['authors'].str.split('/').apply(unique_authors.update)

# Create a list from the set and sort it
sorted_authors = sorted(list(unique_authors))

# Create a label encoder and fit it with the sorted authors list
le = LabelEncoder()
le.fit(sorted_authors)

# Apply the label encoder to the 'authors' column
df['author_ids'] = df['authors'].apply(lambda x: '/'.join(map(str, le.transform(x.split('/')))))

## Publisher Label Encoding remplace Publisher by IDs
# Create a LabelEncoder object
le_publisher = LabelEncoder()

# Fit the LabelEncoder object and transform the 'publisher' column
df['publisher_id'] = le_publisher.fit_transform(df['publisher'])

## Title preprocessing : Stopwords Removal
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# You need to download the stopwords package if you haven't done so yet
nltk.download('punkt')
nltk.download('stopwords')

# Get the English stopwords
stop_words = set(stopwords.words('english'))

# Define a function that will remove stopwords from a given string
def remove_stopwords(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove the stopwords
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    # Join the tokens back into a single string and return it
    return " ".join(tokens)

# Apply the function to the 'title' column
df['title'] = df['title'].apply(remove_stopwords)

