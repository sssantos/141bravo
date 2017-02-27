
# coding: utf-8

# In[3]:

# Cash me ousside how bow dah
import requests
import requests_cache
requests_cache.install_cache("cache")


# In[4]:

# Extract song info from html
from bs4 import BeautifulSoup
billboard_url = "http://www.billboard.com/articles/list/2155531/the-hot-100-all-time-top-songs"
soup = BeautifulSoup((requests.get(billboard_url)).text, "html.parser")
songs = [song.text for song in soup.find_all("h3", {"class": "list-data__title"})]


# In[5]:

# Extra title, artist, and year info
import re
# We consider only the first year for a song if more than one: the 100th song's case
titles  = [str(re.sub(r"\xe2\x80\xa6", r"...", re.sub("\"", "", re.match(r"\"[\"\']?.+\"[\"\']?", song).group(0)))) for song in songs]
artists = [str(re.sub("^\"|\r|(- )|(.*\".*\" )","", re.search("\" .*\r", song).group(0)).lstrip()) for song in songs]
years   = [int(re.sub("\)|\(|,", "", re.search("(\(\d{4}\))|(\(\d{4},)", song).group(0))) for song in songs]


# In[11]:

import pandas as pd 
top100songs = pd.DataFrame({'Title': titles, 'Artist': artists, 'Year': years})

