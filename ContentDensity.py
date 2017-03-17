
# coding: utf-8

# In[1]:

import Tasks2
import NGRAMS
final_data = Tasks2.final_data


# In[2]:

# NATURAL LANGUAGE PROCESSING
import nltk
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

# COUNTER CLASS
from collections import Counter

# SCIKIT LEARN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsRegressor

# VISUALISATION
from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import random

# ELSE
from itertools import izip


# In[3]:

# stemmer = PorterStemmer().stem
# tokenize = nltk.word_tokenize

# def stem(tokens,stemmer = PorterStemmer().stem):
#     return [stemmer(w.lower()) for w in tokens] 

# def lemmatize(text):
#     """
#     Extract simple lemmas based on tokenization and stemming
#     Input: string
#     Output: list of strings (lemmata)
#     """
#     return stem(tokenize(text))


# In[4]:

from NGRAMS import corpus_raw_split, corpus_raw, song_words_list


# In[5]:

lexical_tags = ["ADJ", "ADV", "NOUN", "VERB"]


# In[6]:

tagged_songs = [nltk.pos_tag(song_words, "universal") for song_words in song_words_list]


# In[7]:

lexical_density_list = [float(len([word[0] for word in song if word[1] in lexical_tags]))/float(len(song)) for song in tagged_songs]


# In[8]:

seconds_list = [float(length/float(1000)) for length in final_data["songLength"]]
words_per_song = [float(len(song)) for song in song_words_list]
lyrical_density_list = [words/second for words, second in zip(words_per_song, seconds_list)]


# In[9]:

#content_density_list = [x + y for x, y in zip(lyrical_density_list, lexical_density_list)]
# Except not really. Content density will be represented by graphing lexical vs lyrical density
# Or maybe we could also 3d plots, with lex, lyr, and time?


# In[10]:

lexical_words_in_songs = [[word[0] for word in song if word[1] in lexical_tags] for song in tagged_songs]


# In[11]:

lexical_words_in_songs_no_stopwords = [[word for word in song if not word in STOPWORDS] for song in lexical_words_in_songs]


# In[ ]:



