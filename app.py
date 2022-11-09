import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommendation System')

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity_array.pkl', 'rb'))

# Creating the dataframe
movies = pd.DataFrame(movie_dict)


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=40343d0d46b713d3a22c65f9bd8d8771'
                            f'&language=en-US')
    data = response.json()
    # st.text(data)
    # https://image.tmdb.org/t/p/original
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.loc[i[0]]['movie_id']
        recommended_movies.append(movies.loc[i[0]]['title'])
        # Fetching Poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


selected_movie_name = st.selectbox(
    "Select a Movie and we'll recommend you movies based on that!!",
    movies['title'].values)

# st.write('You selected:', option)

if st.button('Recommend'):
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