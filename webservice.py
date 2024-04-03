from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from Movierecommender_system import MyModel, new_df, similarity, movies

movie_recommender = MyModel(new_df, similarity)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/recommend/{movie}')
def recommend(movie: str):
    recommended_movies = movie_recommender.recommend(movie)
    return {"recommended_movies": recommended_movies}

@app.get('/movies')
def getmovies():
    all_movies = new_df["title"].tolist()
    return {"movies": all_movies}

@app.get('/search/{movie}')
def searched(movie: str):
    movie_details = movies[movies["title"].str.contains(movie)]
    return movie_details.to_dict(orient="records")
