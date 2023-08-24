## Scrapping songs from Telegram and add them to a playlist on Spotify
Let's have some fun using [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) library!

## Goal
This piece of code digests an extracted JSON file of messages of a Telegram chat group (can be adjusted to use any other messanger), list audio songs in these messages and then will add these songs to a specified playlist of a specified Spotify account.

## How to use
To use this code, you need to have **Python3** and also these modules installed:

`
import json  
import requests  
import spotipy
`

Then use Spotify developers tools and create an application, to specify these values and replace them in the code:

`
CLIENT_ID = "SPOTIPY_CLIENT_ID"
CLIENT_SECRET = "SPOTIPY_CLIENT_SECRET"
redirect_uri = "SPOTIPY_REDIRECT_URI"
`

You also need your playlist ID and put it in the code:
`
playlist_id = "SPOTIFY_playlist_id"
`

You can consult with [Spotify Web API documentaion](https://developer.spotify.com/documentation/web-api) to get help obtaining these values.

The next step is to extract JSON file of archived messages of your Telegram group. You can easily do that using Telegram desktop application. The name for the file used in the code is *telegram-channel-messages.json*. You can use whatever name you like, just make sure to adjust the code accordingly. 

