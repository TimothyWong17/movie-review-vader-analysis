from bs4 import BeautifulSoup
import requests
import datetime

class RottenTomatoesScrapper:
    def __init__(self):
        self.rt_top_movies_url = 'https://www.rottentomatoes.com/browse/movies_in_theaters/sort:top_box_office'
        self.rt_reviews_url = 'https://www.rottentomatoes.com'
        self.data = {}
        
    def getTopMovies(self):
        r = requests.get(self.rt_top_movies_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        movies_list = soup.find("div", {"class": "discovery-tiles__wrap"})
        movies = movies_list.find_all("div", {"class": "flex-container"})        
        for movie in movies:
            movie_title = movie.find("span", {"class": "p--small"}).text.strip()
            
            print(f"Scraping data for movie: {movie_title}")
        
            movie_release_date = movie.find("span", {"class": "smaller"}).text.split("Opened")[1].strip()
            movie_release_date = datetime.datetime.strptime(movie_release_date, '%b %d, %Y')
        
            movie_img = movie.find("rt-img", {"class": "posterImage"})['src']
        
            movie_reviews_page = f"{self.rt_reviews_url}{movie.find("a")['href']}/reviews?type=verified_audience"
            self.data[movie_title] = {
                'movie_release_date': movie_release_date,
                'movie_img': movie_img,
                'movie_reviews_page': movie_reviews_page
            }
            
        
        return self.data
     
    def getMovieReviews(self):
        for k,v in self.data.items():
            print(f"Getting movie reviews for: {k}")
            r = requests.get(v['movie_reviews_page'])
            soup = BeautifulSoup(r.text, 'html.parser')
            movie_reviews = []
            m_reviews = soup.find_all("p", {"class": "audience-reviews__review"})
            for mr in m_reviews:
                movie_reviews.append(mr.text.strip())
                
            self.data[k]['movie_reviews'] = movie_reviews
        
        return self.data
    
    