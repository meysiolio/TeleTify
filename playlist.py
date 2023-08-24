import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

global CLIENT_ID
global CLIENT_SECRET
global redirect_uri

CLIENT_ID = "SPOTIPY_CLIENT_ID"
CLIENT_SECRET = "SPOTIPY_CLIENT_SECRET"
playlist_id = "SPOTIFY_playlist_id"
redirect_uri = "SPOTIPY_REDIRECT_URI"


def authorize_account():

    # Initialize the SpotifyOAuth object
    sp_oauth = SpotifyOAuth(
        CLIENT_ID, 
        CLIENT_SECRET, 
        redirect_uri, 
        scope='playlist-modify-private'  # Add any required scopes here
    )
    
    # Get the authorization URL
    if not sp_oauth.validate_token(sp_oauth.get_cached_token()):
        print("----- Generating a new token -----")
        code = sp_oauth.get_auth_response()
        access_token = sp_oauth.get_access_token(code, as_dict=False)

        #### manual process using user prompt ####
        # auth_url = sp_oauth.get_authorize_url()
        # print("Please navigate to this URL and authorize the app:")
        # print(auth_url)
        # # After authorization, the user will be redirected to the redirect URI with a code
        # # code = input("Enter the code from the redirect URI: ")
        # # Exchange the code for an access token
        # token_info = sp_oauth.get_access_token(code)
        # access_token = token_info['access_token']

    else:
        print("----- Using cashed token -----")
        access_token = sp_oauth.get_cached_token()['access_token']

    return access_token

access_token = authorize_account()

# Initialize the Spotipy object with the access token
sp = spotipy.Spotify(auth=access_token)

# Now you can use the Spotipy object to make authorized API requests
user_info = sp.me()
print("Logged in as:", user_info['display_name'])

headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token),
        'Content-Type': 'application/json'
    }

with open('telegram-channel-messages.json', 'r', encoding="utf8") as json_file:
    msg_list_json = json.load(json_file)

for i in range(0,len(msg_list_json["messages"])):
    if "media_type" in msg_list_json["messages"][i]:
        if "title" in msg_list_json["messages"][i]:
            search_pattern = msg_list_json["messages"][i]["title"]   
        if "performer" in msg_list_json["messages"][i]:
            search_pattern = search_pattern + ' ' + msg_list_json["messages"][i]["performer"]
        if search_pattern:
            print(f"For message number {i}: ")
            print(f"Searching for {search_pattern}")
            edited_pattern=search_pattern.replace(" ","+")
            getUrl = f"https://api.spotify.com/v1/search?q={edited_pattern}&type=track"
            res = requests.get(getUrl, headers=headers)

            song_id = (res.json()["tracks"]["items"][0]["id"])
            song_uri = f"spotify:track:{song_id}"

            postUrl = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
            # print(postUrl)
            trackData = {
                            "uris": [
                                song_uri
                            ],
                            "position": 0
                        }
            addRes = requests.post(postUrl, headers=headers, data=json.dumps(trackData))
            print(addRes.json(), end="\n")
            if addRes.json()['snapshot_id']:
                print(f"{search_pattern} was added to the playlist\n\n")

    else:
        print(f"message number {i} does not contain any media\n\n")

print("\n\nAll songs are added")