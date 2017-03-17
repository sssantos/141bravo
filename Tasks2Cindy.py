
# coding: utf-8

# In[1]:

# Extract song info from html
import requests
from bs4 import BeautifulSoup
billboard_url = "http://www.billboard.com/articles/list/2155531/the-hot-100-all-time-top-songs"
soup = BeautifulSoup((requests.get(billboard_url)).text, "html.parser")
songs = [song.text for song in soup.find_all("h3", {"class": "list-data__title"})]

# Extra title, artist, and year info
import re
# We consider only the first year for a song if more than one: the 100th song's case
titles  = [str(re.sub(r"\xe2\x80\xa6", r"...", re.sub("\"", "", re.match(r"\"[\"\']?.+\"[\"\']?", song).group(0)))) for song in songs]
artists = [str(re.sub("^\"|\r|(- )|(.*\".*\" )","", re.search("\" .*\r", song).group(0)).lstrip()) for song in songs]
years   = [int(re.sub("\)|\(|,", "", re.search("(\(\d{4}\))|(\(\d{4},)", song).group(0))) for song in songs]

import pandas as pd 
top100songs = pd.DataFrame({'Title': titles, 'Artist': artists, 'Year': years})


# In[2]:

import requests
#import requests_cache
#requests_cache.install_cache("cache")
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
    lyrics = tmp[0].get_text().encode("ascii","ignore")
    if bool(re.search(pattern= "(We do not have)|(we have no)", string = lyrics)):
        lyrics = ""
        lyric_url = ""
    return({'Url':lyric_url, 'Lyric': lyrics})


# In[3]:

getLyrics(top100songs.loc[80])
top100songs.loc[80]


# In[4]:

result = [getLyrics(row) for idx, row in top100songs.iterrows()]
result = pd.DataFrame(result)


# In[5]:

#Locate songs that couldn't be found using function
missing =result[result['Url'] == ""].index
top100songs.loc[missing]


# In[6]:

notFoundUrls = ["http://www.songlyrics.com/elton-john-billy-joel/candle-in-the-wind-lyrics/", "http://www.songlyrics.com/percy-faith/theme-from-a-summer-place-lyrics/","http://www.songlyrics.com/jewel-feat-kelly-clarkson/foolish-games-lyrics/", ""]


# In[7]:

result.loc[53,'Lyric':'Url'] = getLyrics(top100songs.loc[53], newUrl = notFoundUrls[0])
result.loc[80,'Lyric':'Url'] = getLyrics(top100songs.loc[80], newUrl = notFoundUrls[1])
result.loc[83,'Lyric':'Url'] = getLyrics(top100songs.loc[83], newUrl = notFoundUrls[2])


# In[8]:

song = top100songs.loc[60]
artist = song['Artist']
title = song['Title']
lyric_url = "http://www.metrolyrics.com/say-say-say-lyrics-paul-mccartney.html"
artist = processString(artist, "Artist")
title = processString(title," Title")
soup = BeautifulSoup((requests.get(lyric_url)).text, "html.parser")
tmp = soup.find_all('div', {"id": "lyrics-body-text"})
lyrics = tmp[0].get_text().encode("ascii","ignore")
result.loc[60,'Lyric': 'Url'] = {'Lyric': lyrics, 'Url': lyric_url}


# In[9]:

result = pd.concat([top100songs.reset_index(drop=True), result], axis = 1)
result.loc[53,'Title'] = "Candle in the Wind 1997"
result.loc[83, 'Title'] = "Foolish Games"


# <h3>Spotify API</h3>

# In[10]:

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


# In[11]:

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


# In[12]:

def spotify_audio_features(trackid, token, verbose = False):
    url = "https://api.spotify.com/v1/audio-features/"+trackid
    headers = {"Authorization":"Bearer" + ' ' + str(token)}
    response = requests.get(url, headers = headers)
    response.raise_for_status() # check for errors
    if verbose:
        print response.url

    return response.json() # parse JSON


# In[13]:

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


# In[14]:

idSearch = list()
for index, row in result.iterrows():
    search_result = spotify_search(row['Title'] + ' ' + row['Artist'], "track")
    info = getSpotifyID(search_result, token)
    idSearch.append(getSpotifyID(search_result, token))
    print info
    


# In[15]:

final_data = pd.concat([result.reset_index(drop=True), pd.DataFrame(idSearch)], axis = 1)
final_data


# <p>
# <h1>Cindy's Analysis Time!! :D</h1>

# In[16]:

from matplotlib import pyplot as plt
plt.style.use('ggplot')
import numpy as np


# In[17]:

main_df = final_data
#main_df = pd.concat([top100songs,result], axis = 1)
main_df["Rank"] = range(100, 0, -1)
main_df.head()


# In[33]:

quant = main_df.iloc[:,7:]
del quant["spotifyID"]
del quant["Rank"]
quant["Score"] = range(1, 101)


# I replaced "Rank" with "Score" to remove confusion. Now variables will be positively correlated with Score.

# In[34]:

quant.head()


# In[67]:

quant.corr()#.sort_values(by="Score", ascending = False)


# In[51]:

# normalized
normalized = (quant - quant.mean())/quant.std()
normalized.describe()


# From the correlation matrix, we can see that the strongest correlators with "Rank" are speechiness, mode, and liveness. However, the correlation is very weak, indicating that many may be coincidental.

# In[64]:

print " + ".join(list(quant)[0:10])


# In[65]:

import statsmodels.formula.api as sm

result = sm.ols(formula="Score ~ energy + instrumentalness + key + liveness + loudness + mode + songLength + speechiness + tempo + valence", data=quant).fit()
result.params


# In[66]:

result.summary()


# We can see that the regression is not very strong from this model. We cannot come to any conclusion based on these results. This can be due to our limited sample size, especially since the simple is not identical. Each song is unique and a bit hit during a time period. They must each have their own characteristics and cannot be judged based off other top hits. 
# <p>If we had a larger data set with good and bad songs (a nice variety), preferably from the same time period, then there may be different results.

# In[52]:

plt.hist(main_df["Year"], bins = 30)
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.title("Number of Songs on Top 100 List by Year")
plt.show()


# In[22]:

from matplotlib import pyplot as plt
plt.style.use('ggplot')

plt.hist(main_df["Year"], bins = 20)
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.title("Number of Songs on Top 100 List by Year")
plt.show()


# In[25]:

max(main_df["Year"]), min(main_df["Year"])


# From the histogram, we can see there were quite a lot of top hits right when the first official 'blended' billboard began in 1958. After there, it is not until the late 1970's that music really picks up again. The all-time peak is in that time frame (late 1970s to early 1980s).
# <p>After that, there is a dip with normal amounts of top hits until the late 1990s, with another spike. This spike is soon followed by a big dip, which picks up again in the in the later half of the 2000s.
# <p>We can see that the 2010's are starting strong with lots of top hits coming out.

# <i>Some questions to think about:
# * Could the peak in the 2010s be attributed to the fact that music was much more easily distributed at that time? Is this Billboard chart a good measure of popularity?
# * Are we able to pinpoint major trends and music phases?
# * Are the frequencies also in line with the song's absolute performance on the chart?
# * Why were there not that many hits in the early 2000s? Was this just a simple music low, was it due to external factors, or was it simply because one song hit the charts for a long time?
# * What were the songs and rankings from the late 1970s-early 1980s?
# 
# <i>Note: The first question is simply to add a bit of skepticism and will not be explored in this project.</i>

# In[39]:

peak_70_80 = main_df[(main_df["Year"] > 1975) & (main_df["Year"] < 1984)].sort_values(by="Rank")
peak_70_80.head()


# In[41]:

plt.hist(peak_70_80["Rank"], bins = 10)
plt.xlabel("Rank")
plt.ylabel("Frequency")
plt.title("Actual Rankings from the Peak Era in late 1970s-early 1980s")
plt.show()


# This answers the last question. We can see that there is not a noticeable skew in the data. This could mean that yes, there were a lot of all-time popular songs during these eras, and these songs performed typically like how the rest of the distribution, with roughly even numbers throughout. We <b>cannot</b> say that 
# * <i>Hypothesis 1:</i> The songs from this era had high quantity but had very mediocre/lower ranked songs (quantity > quality), nor the opposite --
# * <i>Hypothesis 2:</i> America went through a music revolution and released a bunch of top hit singles of all time during this period.

# <h2>Frequencies and Popularities</h2>
# <p>Now I will try to create a modified plot to capture frequencies, balanced with the Billboard rank performance.

# In[44]:

freqs = main_df["Year"].value_counts()
freqs.head()


# In[56]:

rank_boost = np.arange(1, 101)
rank_boost = rank_boost * 0.10
rank_boost[95:]


# In[62]:

frq_df = pd.concat([main_df["Year"], pd.Series(rank_boost)], axis = 1)
frq_df.head()


# In[70]:

unique_years = frq_df["Year"].unique()
sum_boosts = {}

for year in frq_df["Year"].unique():
    entries = frq_df[frq_df["Year"] == year]
    sum_boosts[year] = sum(entries.iloc[:,1])

asd = pd.DataFrame(sum_boosts.items(), columns=['Year', 'Boost Value'])
asd.head()


# In[74]:

plt.plot(asd["Year"], asd["Boost Value"], '-')
plt.xlabel("Year")
plt.ylabel("Score")
plt.title("Ranking and Frequencies over the Years")
plt.show()


# <p><h2>Artists</h2>

# In[76]:

# number of unique artists
len(main_df["Artist"].unique())


# In[78]:

main_df["Artist"].value_counts().head(10)


# There are not many duplicate entries by artists on this ultimate 100 list. The maximum repeat by an artist is 2. There are only 7 repeat artists.
