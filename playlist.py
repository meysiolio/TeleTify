import json
#import sys
import requests

with open('telegram-sample.json', 'r', encoding="utf8") as json_file:
    msg_list_json = json.load(json_file)

search_pattern = ''

for i in range(0,len(msg_list_json['messages'])):
    if msg_list_json['messages'][i].media_type:
        if 'title' in msg_list_json['messages'][i]:
            search_pattern = search_pattern + msg_list_json['messages'][i]['title']   
        if 'performer' in msg_list_json['messages'][i]:
            search_pattern = search_pattern + ' ' + msg_list_json['messages'][i]['performer']
        if search_pattern:
            edited_pattern=search_pattern.replace(" ","+")
            url = f"https://api.spotify.com/v1/search?q={edited_pattern}&type=track"
            print(url)
            header = {'Authorization': 'Bearer BQAuskvuytPwQUKy5VTs6w3690Nl7R4-nbmIXBiOdqR9ozybdm_g-MSh03ff37unWOvzMkDKouacnWhDIVSuFabhI1J18r8M6dTUq4sYMeB7tfLX_QE'}
            res = requests.get(url, headers=header)
            a=res.json()
            print(a)
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