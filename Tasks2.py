
# coding: utf-8

# In[1]:

import Tasks0 
top100songs = Tasks0.top100songs


# In[2]:

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


# In[110]:

result = [getLyrics(row) for idx, row in top100songs.iterrows()]
result = pd.DataFrame(result)


# In[111]:

#Locate songs that couldn't be found using function
missing =result[result['Url'] == ""].index
top100songs.loc[missing]


# In[112]:

notFoundUrls = ["http://www.songlyrics.com/elton-john-billy-joel/candle-in-the-wind-lyrics/", "http://www.songlyrics.com/percy-faith/theme-from-a-summer-place-lyrics/","http://www.songlyrics.com/jewel-feat-kelly-clarkson/foolish-games-lyrics/"]


# In[113]:

result.loc[53,'Lyric':'Url'] = getLyrics(top100songs.loc[53], newUrl = notFoundUrls[0])
result.loc[80,'Lyric':'Url'] = getLyrics(top100songs.loc[80], newUrl = notFoundUrls[1])
result.loc[83,'Lyric':'Url'] = getLyrics(top100songs.loc[83], newUrl = notFoundUrls[2])


# In[114]:

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


# In[115]:

result = pd.concat([top100songs.reset_index(drop=True), result], axis = 1)
result.loc[53,'Title'] = "Candle in the Wind 1997"
result.loc[83, 'Title'] = "Foolish Games"


# In[116]:

client_id = '37b4f8e242b54a67a4b8d4807b35d4aa'
client_secret = '9cb223d471b64dac9f1dc48f3b62593f'
#client_id = "Enter your client_id from spotify"
#client_secret = "Enter your client_id"

def spotify_authorize(client_id, client_secret):
    grant_type = 'client_credentials'

    #Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/

    #Request body parameter: grant_type Value: Required. Set it to client_credentials
    body_params = {'grant_type' : grant_type}

    url='https://accounts.spotify.com/api/token'

    response=requests.post(url, data=body_params, auth = (client_id, client_secret)) 
    return(response.json())

token = spotify_authorize(client_id, client_secret)['access_token']


# In[117]:

def spotify_search(term, search_type = "artist", verbose = False):
    url = "https://api.spotify.com/v1/search"
    response = requests.get(url, params = {
        "q": term,
        "type": search_type
    })
    response.raise_for_status() # check for errors
    if verbose:
        print response.url
    
    return response.json() # parse JSON


# In[123]:

def spotify_audio_features(trackid, token, verbose = False):
    url = "https://api.spotify.com/v1/audio-features/"+trackid
    headers = {"Authorization":"Bearer" + ' ' + str(token)}
    response = requests.get(url, headers = headers)
    response.raise_for_status() # check for errors
    if verbose:
        print response.url

    return response.json() # parse JSON


# In[135]:

def getSpotifyID(search, token):
    """
    Search for song title and artist combination on spotify and return id, duration, and other audio characteristcs
    """
    id = search['tracks']['items'][0]['id']
    length = search['tracks']['items'][0]['duration_ms']
    audio_features = spotify_audio_features(id, token)
    result = {'spotifyID': id, 
              'songLength': audio_features['duration_ms'],
              'acousticness': audio_features['acousticness'],
              'danceability': audio_features['danceability'],
              'energy': audio_features['energy'], 
              'instrumentalness': audio_features['instrumentalness'],
              'key': audio_features['key'],
              'liveness': audio_features['liveness'],
              'loudness': audio_features['loudness'],
              'mode': audio_features['mode'],
              'speechiness': audio_features['speechiness'],
              'tempo': audio_features['tempo'],
             'valence': audio_features['valence']}
    return result


# In[136]:

idSearch = list()
for index, row in result.iterrows():
    search_result = spotify_search(row['Title'] + ' ' + row['Artist'], "track")
    idSearch.append(getSpotifyID(search_result, token))
    


# In[140]:

final_data = pd.concat([result.reset_index(drop=True), pd.DataFrame(idSearch)], axis = 1)


# In[141]:

final_data

