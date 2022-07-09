from turtle import distance
from flask import Flask, render_template, request
import os
import pickle
import json
import requests

app = Flask(__name__)

# environment variables
key = os.environ.get('API_KEY')

# model = pickle.load(open('recommend.pkl', 'rb'))
db = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def getPoster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{id}?api_key={apiKey}&language=en-US".format(
        id = movie_id, apiKey = key)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie_name):
    index = db[db['title'] == movie_name].index[0]
    recommended_movie_names = []
    recommended_movie_posters = []
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        recommended_movie_names.append(db.iloc[i[0]].title)
        recommended_movie_posters.append(getPoster(db.iloc[i[0]].movie_id))
    return recommended_movie_names, recommended_movie_posters


@app.route("/", methods=['GET', 'POST'])
def home():
    movies = []
    posters = []
    if request.method == 'POST':
        movieName = request.form.get('movieName')
        if(movieName):
            movies, posters = recommend(movieName)
        # print(movieName)
    return render_template('index.html', movies=movies, db=db, posters=posters)

if __name__ == "__main__":
    app.run(debug=True)
