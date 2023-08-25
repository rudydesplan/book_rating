import pandas as pd
import re

def preprocess_data(df):
    """
    Preprocesses the input dataframe for prediction.
    
    Args:
    - df (pd.DataFrame): Input dataframe with book details.
    
    Returns:
    - pd.DataFrame: Preprocessed dataframe.
    """
    
    # Remove duplicated ISBNs
    df = df.drop_duplicates(subset='isbn', keep='first')
       
    # Clean the authors' column to keep only the primary author
    df['authors'] = df['authors'].apply(lambda x: x.split("/")[0])
    
    # Extract publication year from publication_date
    df['publication_year'] = pd.to_datetime(df['publication_date'], errors='coerce').dt.year
    
    # Create the 'is_series' column
    df['is_series'] = df['title'].apply(lambda x: 1 if re.search(r'\(.*#\d+\)', x) else 0)
    
    # Create the 'engagement' column
    df['engagement'] = df['text_reviews_count'] / df['ratings_count']
    
    # Keeping only the top 6 languages and categorizing others as 'other'
    top_languages = df['language_code'].value_counts().nlargest(6).index.tolist()
    df['language_code'] = df['language_code'].apply(lambda x: x if x in top_languages else 'other')
    
    # One-hot encoding the language_code column
    df = pd.get_dummies(df, columns=['language_code'], drop_first=True)
    
    # Dropping unnecessary columns
    columns_to_drop = ['bookID', 'title', 'authors', 'isbn', 'isbn13', 'publication_date', 'publisher', 'work']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Filling NaN values with 0
    df = df.fillna(0)
    
    return df

