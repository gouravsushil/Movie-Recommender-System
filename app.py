import pandas as pd
import streamlit as st
import pickle
# import gzip
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

cv = CountVectorizer(max_features=5000,stop_words='english')

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/find/movie_id?external_source=7cddbdfad423c66f5f73f753feb8d295&language=en-US'.format(movie_id))
#     data = response.json()
#     st.text(data)
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie,similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    # recommended_movies_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetching poster from API
        # movie_id = i[0]
        # recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies


# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# with open('movies_dict.pkl', 'rb') as file:
#     movies_dict = pickle.load(file)

@st.cache_data
def load_pickle_file(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)
movies_dict = load_pickle_file('movies_dict.pkl')


movies = pd.DataFrame(movies_dict)
vectors = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)

# similarity = pickle.load(open('similarity.pkl', 'rb'))
# with gzip.open('similarity1.pkl.gz', 'rb') as f:
#     similarity = pickle.load(f)

st.title('Movie Recommender System')



# # Print the current working directory
# st.write("Current working directory:", os.getcwd())
#
# # List all files in the current working directory
# st.write("Files in the directory:", os.listdir(os.getcwd()))

option = st.selectbox(
    "Select any movie of your choice: ",
    (movies['title'].values)
)


if st.button("Recommend"):


    recommendations = recommend(option,similarity)

    for i in recommendations:
        st.write(i)



