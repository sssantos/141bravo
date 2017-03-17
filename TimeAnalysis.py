
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import Tasks2Cindy


# In[2]:

final_data = Tasks2Cindy.final_data


# In[3]:

songs100 = Tasks2Cindy.top100songs


# In[4]:

songs100.loc[19]


# In[5]:

art_list = songs100["Artist"].unique().tolist()
temp =[artist.split("&") for artist in art_list]
temp = reduce(lambda x, y: x + y, temp, [])
unique_artists = reduce(lambda x, y: x + y, [artist.split("feat.") for artist in temp], [])
unique_artists = [artist.strip() for artist in unique_artists]


# In[6]:

temp = reduce(lambda x, y: x + y, [artist.split("&") for artist in songs100["Artist"]], [])
temp = reduce(lambda x, y: x + y, [artist.split("feat.") for artist in temp], [])
temp = [artist.strip() for artist in temp]
all_artists = reduce(lambda x, y: x + y, [artist.split(" and ") for artist in temp], [])

double_artists = pd.Series(all_artists).value_counts().head(13)
double_artists


# In[25]:

# look for the years associated with each artist
# for each artist in doublehits, scan through the artists columnto search 
#if their name is there, and then return the corresponding Year(s), Score, and Rank


#pd.DataFrame([songs100.loc[i] for i, j in enumerate(songs100["Artist"]) if j in " ".join(double_artists.index)])

doubleA_entries = []

for artist in double_artists.index:
    for ind, value in enumerate(songs100["Artist"]):
        if artist in value:
            doubleA_entries.append(songs100.loc[ind])

#pd.DataFrame(doubleA_entries)


# A question to look into is to see what the range is for each artist, to see where was the beginning and end of their top stardom? Which artists have lived in the spotlight for the longest?

# In[8]:

def decade_indicator(year):
    yearRange = range(195, 202)
    for yr in yearRange:
        if str(yr) in str(year):
            return str(yr) + "0's"
        
decade_indicator(1954)


# In[9]:

main_df = Tasks2Cindy.main_df
main_df["Decade"] = [decade_indicator(year) for year in main_df["Year"]]


# In[16]:

# VISUALISATION
from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')
#import wordcloud
#from wordcloud import WordCloud, STOPWORDS
plt.style.use('ggplot')
import random
import nltk
import ContentDensity


# In[22]:

# lexical density divided by decade, boxplot
lexical_with_stop = ContentDensity.lexical_words_in_songs
#song_bigram = ContentDensity.song_bigram
#song_trigram = ContentDensity.song_trigram


# In[24]:

lex_df = main_df
lex_df["Lexical"] = lexical_with_stop


# In[45]:

main_df.head()


# In[38]:

lexical_no_stop = lexical_words_in_songs_no_top
lex_df = main_df
lex_df["Lexical"] = lexical_no_stop

def word_cloud_time(df, beginYear, endYear):
    # get range of entries
    temp = df[df["Year"] >= beginYear]
    lex_list = temp[temp["Year"] <= 1969]["Lexical"]
    
    #lex_list = df[(df["Year"] >= beginYear) and (df["Year"] <= endYear)]
    # get the lexical
    entries = reduce(lambda x, y: x + y, lex_list, [])
    long_string = " ".join(entries)
    
    #print long_string
    
     GENERATE WORD CLOUD
    wc.generate(long_string)

    # COLORING
    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(50, 0%%, %d%%)" % random.randint(10, 50)

    # PLOTTING
    plt.figure(figsize=(20,10))
    plt.imshow(wc.recolor(color_func = grey_color_func, random_state=3))
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
    
word_cloud_time(lex_df, 1950, 1959)    
word_cloud_time(lex_df, 1960, 1969)
word_cloud_time(lex_df, 1970, 1979)
word_cloud_time(lex_df, 1980, 1989)
word_cloud_time(lex_df, 1990, 1999)
word_cloud_time(lex_df, 2000, 2009)
word_cloud_time(lex_df, 2010, 2019)


# In[44]:

lexical_density_list = ContentDensity.lexical_density_list

main_df["Lexical Density"] = lexical_density_list

main_df.boxplot("Lexical Density", "Decade")
plt.ylabel("Lexical Density")
plt.title("Lexical Densities By Decade")
plt.suptitle("")

plt.show()


# In[ ]:

from NGRAMS import song_bigram, song_trigram

main_df = pd.concat([main_df,song_bigram, song_trigram], axis = 1)

# tack on song_bigrams and song_trigrams to main_df


# In[ ]:

# trigram per decade
decades = [df[df["Year"] >= (1900 + i*10) and df["Year"] < (1900 + (i+1)*10)]  for i in range(5, 12)]


# In[ ]:

# maybe create a trigram per decade
# timeless - phrases that appear through all time periods
# unique - what's unique to one time period


# In[ ]:

# bar plot of bigrams/trigrams

