import pandas as pd
import os
import re
import sqlite3
from rotten_tomatoes_scrapper import RottenTomatoesScrapper
from datetime import date

def extract():
    rtScrapper = RottenTomatoesScrapper()
    rtScrapper.getTopMovies()
    data = rtScrapper.getMovieReviews()
    df = pd.DataFrame.from_dict(data=data, orient='index')
    df = df.reset_index()
    df = df.rename(columns={'index': 'movie_title'})
    return df

def transform(data):
    print("Transforming data")
    data = data.explode('movie_reviews')
    return data


def load_to_sqlite(data):
    conn = sqlite3.connect('db/db_movie_reviews')
    print("Writing to DB")
    data.to_sql('movie_reviews', con=conn, if_exists='replace')
    conn.commit()
    conn.close()

def main():
    df = extract()
    df_transformed = transform(df)
    load_to_sqlite(df_transformed)
    
    
if __name__ == "__main__":
    main()