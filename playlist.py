import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

global CLIENT_ID
global CLIENT_SECRET
global redirect_uri

CLIENT_ID = "c7534310526246c3966dbc89a94ca3e5"
CLIENT_SECRET = "6b19f6272cbc4e39b8e4944afe6975e7"
playlist_id = "2QWKUjBiNjnki6OJxyeYi1"
redirect_uri = "http://localhost:8888/callback"


def authorize_account():

    # # Set your Spotify API credentials
    # SPOTIPY_CLIENT_ID = 'your_client_id'
    # SPOTIPY_CLIENT_SECRET = 'your_client_secret'
    # SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'  # This should match your app's redirect URI

    # Initialize the SpotifyOAuth object
    sp_oauth = SpotifyOAuth(
        CLIENT_ID, 
        CLIENT_SECRET, 
        redirect_uri, 
        scope='playlist-modify-public'  # Add any required scopes here
    )

    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()

    print("Please navigate to this URL and authorize the app:")
    print(auth_url)

    # After authorization, the user will be redirected to the redirect URI with a code
    code = input("Enter the code from the redirect URI: ")

    # Exchange the code for an access token
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']

    # Initialize the Spotipy object with the access token
    sp = spotipy.Spotify(auth=access_token)

    # Now you can use the Spotipy object to make authorized API requests
    user_info = sp.me()
    print("Logged in as:", user_info['display_name'])

    return sp


def renew_bearer_token():

    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    #Convert response to JSON
    auth_response_data = auth_response.json()

    #Save the access token
    access_token = auth_response_data['access_token']
    # print(access_token) - each a new access token would be generated

    #Need to pass access token into header to send properly formed GET request to API server
    # headers = {
    #     'Authorization': 'Bearer {token}'.format(token=access_token)
    # }

    return access_token

access_token = renew_bearer_token()

headers1 = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

# headers2 = {
#         'Authorization': 'Bearer {token}'.format(token=access_token),
#         'Content-Type': 'application/json'
#     }

with open('telegram-sample2.json', 'r', encoding="utf8") as json_file:
    msg_list_json = json.load(json_file)

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope="playlist-modify-public"))

sp = authorize_account()

for i in range(0,len(msg_list_json["messages"])):
    if "media_type" in msg_list_json["messages"][i]:
        if "title" in msg_list_json["messages"][i]:
            search_pattern = msg_list_json["messages"][i]["title"]   
        if "performer" in msg_list_json["messages"][i]:
            search_pattern = search_pattern + ' ' + msg_list_json["messages"][i]["performer"]
        if search_pattern:
            edited_pattern=search_pattern.replace(" ","+")
            getUrl = f"https://api.spotify.com/v1/search?q={edited_pattern}&type=track"
            print(getUrl)
            res = requests.get(getUrl, headers=headers1)

            song_id = (res.json()["tracks"]["items"][0]["id"])
            song_uri = [f"spotify:track:{song_id}"]
            print(song_uri)

            sp.playlist_add_items(playlist_id, song_uri)

            # postUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris=spotify%3Atrack%3A{song_uri}"
            # addRes = requests.post(postUrl, headers=headers2, data=trackData)
            # print(addRes.json())
            # with open('output.json', 'w') as out_file:
            #     json.dump(res.json(), out_file, sort_keys = True, indent = 4, ensure_ascii = False)
    else:
        print(f"message number {i} does not contain any media")
        search_pattern = ''

    print("\n\n\n\nAll songs are added")