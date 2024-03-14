import requests

class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

access_token = ''
user_id = ''

# пробовал потестить - выдает общие данные: {'response': [{'id': 1111111, 'first_name': 'Айтуган', 'last_name': 'Ибрагимов', 'can_access_closed': True, 'is_closed': False}]}

vk = VK(access_token, user_id)
print(vk.users_info())

