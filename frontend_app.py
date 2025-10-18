



import pickle
import streamlit as st
import pandas as pd
import requests
import os
os.environ["PORT"] = os.environ.get("PORT", "10000")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x:x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Load DataFrame from pickle file
with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

# Ensure movies is a DataFrame
if isinstance(movies_dict, dict):
    movies = pd.DataFrame(movies_dict)
else:
    movies = movies_dict


# Load similarity matrix
file_url = "https://www.dropbox.com/scl/fi/hqv9hqvtk3f5fofa7ojbl/similarity.pkl?rlkey=cgf4fpqdotzev1qb8qqtakjwk&st=zt22lp8q&dl=1"
file_path = "similarity.pkl"

if not os.path.exists(file_path):
    response = requests.get(file_url)
    with open(file_path, "wb") as f:
        f.write(response.content)

# Then load similarity.pkl as usual
similarity = pickle.load(open(file_path, "rb"))


# Prepare list of movies for selectbox
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])






