import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

# reading data
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# merging both datasets
movies = movies.merge(credits , on="title")

# subsetting data on usefull features
movies = movies[["genres" , "movie_id" , "title" , "overview", "keywords" , "cast" , "crew"]]

# droping na values 
movies.dropna(inplace=True)

# converting dictionary into list 
import ast
def convert(dic):
  li = []
  for i in ast.literal_eval(dic):
    li.append(i["name"])
  return li

# applying function 
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)

# converting to list and fetching 1st 3 values
def convert_3(dic):
  li = []
  count = 0
  for i in ast.literal_eval(dic):
    if count!=3:
      li.append(i["name"])
      count+=1
  return li

# Fetching first three cast values 
movies["cast"] = movies["cast"].apply(convert_3)

# fetching values where job==director
def fetch_director(dic):
  li = []
  for i in ast.literal_eval(dic):
    if i["job"]=="Director":
      li.append(i["name"])
      break
  return li

#applying function on crew
movies["crew"] = movies["crew"].apply(fetch_director)

# converting overview column to a list 
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# removing spaces and converting again into the string
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" " , "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" " , "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" " , "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" " , "") for i in x])

# creating new feature "tags" by concatinating all the lists
movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]

# creating new_df by subsetting dataframe
new_df = movies[["movie_id" , "title" , "tags"]]

# converting tags into string
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x))

# converting tags to lower cases
new_df["tags"] = new_df["tags"].apply(lambda x: x.lower())

# performing vectorization using sklearn 
cv = CountVectorizer(max_features=5000 , stop_words="english") # it will also remove stop words
# vectors = cv.fit_transform(new_df["tags"]).toarray()
# performing stemming on data
ps = PorterStemmer()

# defing helper function that will split the text and apply stemming and return string
def stem(text):
  l = []
  for i in text.split():
    l.append(ps.stem(i)) # stemming
  return " ".join(l) # converting back to string

# applying function
new_df["tags"] = new_df["tags"].apply(stem)

# applying vectorization 
vectors = cv.fit_transform(new_df["tags"]).toarray()

# calculating similarities using cosine distance
similarity = cosine_similarity(vectors)

# defining recommender system function
def recommend(movie):
  movie_index = new_df[new_df["title"]==movie].index[0] # fetching index of movie provided by user
  distance = similarity[movie_index] # extracting distances of that movie using index number
  movies_list = sorted(list(enumerate(distance)), reverse=True , key=lambda x: x[1])[1:6]
  # print movies indexes
  recommended_movies = []  # List to store recommended movie titles
  for i in movies_list:
    recommended_movies.append(new_df.iloc[i[0]].title)
    
  return recommended_movies


