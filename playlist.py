import json
#import sys
import requests


CLIENT_ID = "c7534310526246c3966dbc89a94ca3e5"
CLIENT_SECRET = "6b19f6272cbc4e39b8e4944afe6975e7"

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

#Need to pass access token into header to send properly formed GET request to API server
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

with open('telegram-sample2.json', 'r', encoding="utf8") as json_file:
    msg_list_json = json.load(json_file)

# search_pattern = ''

for i in range(0,len(msg_list_json["messages"])):
    if "media_type" in msg_list_json["messages"][i]:
        if "title" in msg_list_json["messages"][i]:
            search_pattern = msg_list_json["messages"][i]["title"]   
        if "performer" in msg_list_json["messages"][i]:
            search_pattern = search_pattern + ' ' + msg_list_json["messages"][i]["performer"]
        if search_pattern:
            edited_pattern=search_pattern.replace(" ","+")
            url = f"https://api.spotify.com/v1/search?q={edited_pattern}&type=track"
            print(url)
            res = requests.get(url, headers=headers)
            # print(res)
            # print("\n\n\n")
            # print(res.text)
            # print("\n\n\n")
            # print(res.json())
            # a=json.loads(res.text)

            print(res.json()["tracks"]["items"][0]["id"])

            # with open('output.json', 'w') as out_file:
            #     json.dump(res.json(), out_file, sort_keys = True, indent = 4, ensure_ascii = False)
    else:
        print(f"message number {i} does not contain any media")
        search_pattern = ''


############## piece of codes that may be useful
    # print(f"message #{i} - Start")
    # try:
    #     search_pattern[i] = msg_list_json['messages'][i]['title']
    # except:
    #     print(f"title for message #{i} does not exist")
    # try:
    #     search_pattern2 = msg_list_json['messages'][i]['performer']
    # except:
    #     print(f"performer for message #{i} does not exist")
    # try:
    #     print(search_pattern1 + search_pattern2)
    # except:
    #     print(f"Both title and performer for message #{i} do not exist")
    # print(f"message #{i} - End")