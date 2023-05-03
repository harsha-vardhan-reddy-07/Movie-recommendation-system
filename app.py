import requests
import streamlit as st
import pickle
import pandas as pd
import gdown


# Here, the similarities.pkl file is 180MB and is not supported by github. So, we uploaded it into gdrive and download it from there using gdown library!!
#url for our file!!
url = 'https://drive.google.com/uc?id=1Oo4TIyZkYRwEg1bt6Jqyy9PSsUVz8fTu'
output = 'similarity.pkl'

gdown.download(url, output, quiet=False)
#loading pkl file
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)


    
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open(urllib3.request.urlopen('https://drive.google.com/file/d/1Oo4TIyZkYRwEg1bt6Jqyy9PSsUVz8fTu/view?usp=share_link', 'rb')))


# Function to fetch posters

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9c73aef5d4060891f00a40559857da11&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']


# recommendation function

def recommend(movie_title):
    movie_index = movies[movies.title == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.title('Havar Recommender System')

selected_movie_name = st.selectbox(
    'Search/Select your favourite movie!',
    movies['title'].values)

if st.button('Recommend Similar Movies'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


