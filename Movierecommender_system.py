#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd


# In[2]:


# credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')


# In[3]:


movies.head(1)


# In[4]:


credits.head(1)


# In[5]:


movies = movies.merge(credits, on="title")


# In[6]:


# genres, id, keyword, title, overview, cast, crew

movies = movies[['genres', 'movie_id', 'keywords', 'title', 'overview', 'cast', 'crew']]


# In[7]:


movies.head(1)


# In[8]:


movies.dropna(inplace = True)


# In[9]:


movies.isnull().sum()


# In[10]:


movies.genres.iloc[0]


# In[11]:


import ast

def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name']);
    return l;


# In[12]:


movies.genres = movies.genres.apply(convert)


# In[13]:


movies.keywords = movies.keywords.apply(convert)


# In[14]:


import ast

def convert3(obj):
    l = []
    count = 0
    for i in ast.literal_eval(obj):
        if count<=3:
            l.append(i['name'])
            count+=1
        else:
            break
    return l


# In[15]:


movies.cast = movies.cast.apply(convert3)


# In[16]:


movies.head()


# In[17]:


import ast

def getname(obj):
    l = [];
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name']);
    return l;


# In[18]:


movies.crew = movies.crew.apply(getname)


# In[19]:


movies.overview = movies.overview.apply(lambda x:x.split())


# In[20]:


movies['genres'] = movies['genres'].apply(lambda x:[i.replace(' ', '') for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(' ', '') for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(' ', '') for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(' ', '') for i in x])


# In[21]:


movies['tags'] = movies['genres'] +movies['keywords'] +movies['crew'] +movies['cast'] + movies['overview']


# In[22]:


new_df = movies[['movie_id', 'title', 'tags']]


# In[23]:


new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))


# In[24]:


new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

# In[27]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words = 'english')


# In[28]:


vectors = cv.fit_transform(new_df['tags']).toarray();


# In[30]:


import nltk

from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


# In[31]:


def stem(text):
    l = []
    for i in text.split():
        l.append(ps.stem(i))
    return " ".join(l)


# In[32]:


new_df.tags = new_df.tags.apply(stem)


# In[34]:


from sklearn.metrics.pairwise import cosine_similarity


# In[35]:


similarity = cosine_similarity(vectors);


# In[38]:


def recommend(movie):
    index = new_df[new_df.title == movie].index[0]
    distances = similarity[index];
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


# In[40]:


class MyModel:
    def __init__(self, df, similarity_matrix):
        self.df = df
        self.similarity_matrix = similarity_matrix
    
    def recommend(self, movie):
            index = self.df[self.df.title == movie].index[0]
            distances = self.similarity_matrix[index];
            movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
            recommended_movies = [self.df.iloc[i[0]].title for i in movies_list]
            return recommended_movies
        


# In[41]:


movie_recommender = MyModel(new_df, similarity)


# # In[43]:


# import pickle

# with open("movie_recommender.pkl" ,"wb") as f:
#     pickle.dump(movie_recommender, f)

