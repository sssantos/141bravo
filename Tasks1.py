
# coding: utf-8

# In[1]:

import Tasks0 
top100songs = Tasks0.top100songs


# In[146]:

top100songs.loc[53]


# In[166]:

import requests
import requests_cache
requests_cache.install_cache("cache")
from bs4 import BeautifulSoup
import re
import string
import pandas as pd
test = top100songs.loc[9] 
def processString(s, type):
    s = re.sub("['?:!.,;&/]+", " ", s).lower().strip()
    if(type != "Artist"):
        s = re.sub("-", "",s)
    s = re.sub("\s+", "-", s)
    return(s)

def getLyrics(song):
    artist = song['Artist']
    title = song['Title']
    #Remove punctuation and change to lower case.
    artist = processString(artist, "Artist")
    title = processString(title," Title")
    lyric_url = "http://www.songlyrics.com/"+artist+"/"+title+"-lyrics/"
#    print(lyric_url)
    soup = BeautifulSoup((requests.get(lyric_url)).text, "html.parser")
    tmp = soup.find_all('p', {"id": "songLyricsDiv"})
    lyrics = tmp[0].get_text()
    if 'Sorry, we have no' in lyrics:
        lyrics = ""
    return({'Url':lyric_url, 'Lyric': lyrics})


# In[167]:

result = [getLyrics(row) for idx, row in top100songs.iterrows()]


# In[168]:

#Couldn't Find
# Elton John - Candle in the wind 1997 something about the way you look tonight Lyrics
# paul-mccartney-and-michael-jackson/say-say-say-lyrics/
# jewel/you-were-meant-for-me-foolish-games-lyrics/
pd.DataFrame(result)

