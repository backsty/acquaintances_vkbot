"""
sex: 1 - девушки, sex: 2 - парни

"""
import json
import requests
from urllib.parse import urlencode
from pprint import pprint

vk_url = 'https://oauth.vk.com/authorize'
params = {
    'client_id': 51794519,
    "redirect_uri": 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'friends, audio, groups, photos',
    'response_type': 'token'
}
oath_url = f'{vk_url}?{urlencode(params)}'
print(oath_url)
response = requests.get(f'{vk_url}?{urlencode(params)}')

token = (
    'vk1.a.dGoqDbHTwM6XIgj6qa1YKiytzDJfxbDdJfeS6FIq90D7j8gaXlh5jaBwQ3YcTskyD146EMJohPa2powp5V3bqopUZsXKmQu4fG38WyoPFzV9'
    'OTQlob5s3iB-uXzJ4MNXZiGVlYbThE2v3JOSkrmk-X5O8lF8Y-fzkLaJ0-ZGnFjITGwwtgRNVSsfcgXCBtvZ2hfkF6ZYx0_CdfA1Ncq8qA'
)

search_params = {  # Решить проблему с выдачей 1000 человек.
    'access_token': token,
    'count': 1000,
    'offset': 0,
    'v': '5.199',
    'sex': 1,
    'city': 1,
    'fields': 'is_friend',
    'age_from': 30,
    'age_to': 30,
    'has_photo': 1
}
get_token = ('vk1.a.a1Z0lP2MH'
             '-s3wOkXEnsGUFK1P_Wq5r4eJMXQ6kiLLtRanBnZwoaQGXqewA5NsQ48jYzPiC1o26gS0qR9POKSLxJlTnOl_NMgiIhG9w4_d'
             'qBvK_ZMjLJZfipuv5UvnOEe0ihX_WmGPXJzeg5PfdvQRQs9xTtf1BWXTswS_AlEJUXABX4ELNF6zgW57qnzZ5Pma_85ZmT-nyIGCYmI6NXQFg')
get_params = {
    'access_token': token,
    'v': '5.199',
    'owner_id': 32707600,
    'offset': 400,
    'extended': 1,
    'photo_sizes': 1,
    'type': 'z',
    'count': 200
}
# search_response = requests.get(f'https://api.vk.com/method/users.search', params=search_params)
# pprint(search_response.json())
search_response = requests.get(f'https://api.vk.com/method/photos.getAll', params=get_params)
pprint(search_response.json())
with open(f'result.json', 'w') as jf:
    json.dump(search_response.json(), jf, indent=2)

for item in search_response.json().get('response').get('items'):
    print(item.get('likes').get('count'))


def get_photos(user_token, owner_id):
    photo_request_params = {
        'access_token': user_token,
        'v': '5.199',
        'owner_id': owner_id,
        'extended': 1,
        'photo_sizes': 1
    }
    photo_response = requests.get(f'https://api.vk.com/method/photos.get', params=photo_request_params)
    photo_result = photo_response.json().get()
