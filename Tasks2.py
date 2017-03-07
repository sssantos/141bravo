
# coding: utf-8

# In[1]:

import Tasks0 
top100songs = Tasks0.top100songs


# In[4]:

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

def getLyrics(song, newUrl = ''):
    artist = song['Artist']
    title = song['Title']
    #Remove punctuation and change to lower case.
    artist = processString(artist, "Artist")
    title = processString(title," Title")
    lyric_url = "http://www.songlyrics.com/"+artist+"/"+title+"-lyrics/"
    if newUrl != '':
        lyric_url = newUrl
#    print(lyric_url)
    soup = BeautifulSoup((requests.get(lyric_url)).text, "html.parser")
    tmp = soup.find_all('p', {"id": "songLyricsDiv"})
    lyrics = tmp[0].get_text()
    if bool(re.search(pattern= "(We do not have)|(we have no)", string = lyrics)):
        lyrics = ""
        lyric_url = ""
    return({'Url':lyric_url, 'Lyric': lyrics})


# In[5]:

getLyrics(top100songs.loc[80])
top100songs.loc[80]


# In[6]:

result = [getLyrics(row) for idx, row in top100songs.iterrows()]
result = pd.DataFrame(result)


# In[7]:

#Locate songs that couldn't be found using function
missing =result[result['Url'] == ""].index
top100songs.loc[missing]


# In[8]:

notFoundUrls = ["http://www.songlyrics.com/elton-john-billy-joel/candle-in-the-wind-lyrics/", "http://www.songlyrics.com/percy-faith/theme-from-a-summer-place-lyrics/","http://www.songlyrics.com/jewel-feat-kelly-clarkson/foolish-games-lyrics/", ""]


# In[9]:

result.loc[53,'Lyric':'Url'] = getLyrics(top100songs.loc[53], newUrl = notFoundUrls[0])
result.loc[80,'Lyric':'Url'] = getLyrics(top100songs.loc[80], newUrl = notFoundUrls[1])
result.loc[83,'Lyric':'Url'] = getLyrics(top100songs.loc[83], newUrl = notFoundUrls[2])


# In[10]:

song = top100songs.loc[60]
artist = song['Artist']
title = song['Title']
lyric_url = "http://www.metrolyrics.com/say-say-say-lyrics-paul-mccartney.html"
artist = processString(artist, "Artist")
title = processString(title," Title")
soup = BeautifulSoup((requests.get(lyric_url)).text, "html.parser")
tmp = soup.find_all('div', {"id": "lyrics-body-text"})
lyrics = tmp[0].get_text()
result.loc[60,'Lyric': 'Url'] = {'Lyric': lyrics, 'Url': lyric_url}


# In[12]:

result

