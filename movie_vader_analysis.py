from db import DB
import re
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class MovieSentimentAnalysis:
    def __init__(self, movie_title):
        self.db_conn = DB('db/db_movie_reviews')
        self.movie_title = movie_title
        
    def data_preprocessing(self):
        data = self.db_conn.get_table_data('movie_reviews')
        movie_reviews = data[data['movie_title'] == self.movie_title][['movie_reviews']]
        return movie_reviews


    def run_model(self):
        data = self.data_preprocessing()
        sid = SentimentIntensityAnalyzer()
        
        data['scores'] = data['movie_reviews'].apply(lambda review: sid.polarity_scores(review))
        data['compound']  = data['scores'].apply(lambda score_dict: score_dict['compound'])
        data['comp_score'] = data['compound'].apply(lambda c: 'pos' if c >=0 else 'neg')

        return data
        