from flask import Flask, render_template, request, url_for
import pandas as pd
from db import DB
from movie_vader_analysis import MovieSentimentAnalysis


def getMovieTitles():
    db_conn = DB('db/db_movie_reviews')
    df = db_conn.get_table_data("movie_reviews")
    movie_titles =  list(df['movie_title'].unique())
    return movie_titles
    
    
app = Flask(__name__)

@app.route('/')
def index():
    movie_titles = getMovieTitles()
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/review',  methods=['POST'])
def review():
    movie_titles = getMovieTitles()
    movie_selected = request.form['movie_select']
    movie_sa = MovieSentimentAnalysis(movie_selected)
    data = movie_sa.run_model()
    return render_template('index.html', movie_titles=movie_titles, movie_selected=movie_selected, tables=[data.to_html(index=False, classes='data')])