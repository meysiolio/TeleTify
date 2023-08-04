import json
#import sys
import requests

with open('telegram-music-group-history.json', 'r', encoding="utf8") as json_file:
    msg_list_json = json.load(json_file)

search_pattern = ''

for i in range(1003,1007):
    if 'title' in msg_list_json['messages'][i]:
        search_pattern = search_pattern + msg_list_json['messages'][i]['title']   
    if 'performer' in msg_list_json['messages'][i]:
        search_pattern = search_pattern + ' ' + msg_list_json['messages'][i]['performer']
    if search_pattern:
        edited_pattern=search_pattern.replace(" ","+")
        url = f"https://api.spotify.com/v1/search?q={edited_pattern}&type=track"
        print(url)
        header = {'Authorization': 'Bearer BQBVgqle9Ec3DWRzKfK0bsnTIDBqCEfeXyS2q7viL5ENoZjMqATuXhNypzxDQ3EB4wbRJi4SUQqdJsXjx8JjCfP64Z_uL9dGP-Nk7KKXM0WVWWuzGhs'}
        res = requests.get(url, headers=header)
        a=res.json()
        print(a)
        search_pattern = ''


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