import requests
import vk_api

from scripts.keyboard import Button
from scripts.vk_bot_functions import safe_get_from_dict, safe_get_from_list, build_url, culc_age, get_common_params, get_user_data
from scripts.user_data import UserResultData
from DB.create_db import Users, Photos, Search_Weights


class VKBot:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, user_id, access_token, dbOdject, results):
        self.token = access_token
        self.user_id = user_id
        self.user_data = get_user_data(self.base_url, self.token, str(user_id))
        self.dbOdject = dbOdject
        self.results = results

    def get_common_groups(self, target_user_id):
        url = build_url(self.base_url, 'groups.getMutual')
        params = get_common_params(self.token)
        params.update({
            'source_uid': self.user_id['id'],  # ID текущего пользователя
            'target_uid': target_user_id,  # ID пользователя, с которым ищем общие группы
        })
        try:
            response = requests.json()["response"]
        except KeyError:
            return []
        return response

    def get_common_friends(self, target_user_id):
        url = build_url(self.base_url, 'friends.getMutual')
        params = get_common_params(self.token)
        params.update({
            'source_uid': self.user_id['id'],  # ID текущего пользователя
            'target_uid': target_user_id,  # ID пользователя, с которым ищем общих друзей
        })
        try:
            response = requests.json()["response"]
        except KeyError:
            return []
        return response

    def get_user_photos(self, user_id):
        url = build_url(self.base_url, 'photos.get')
        params = get_common_params(self.token)
        params.update({
            'owner_id': user_id,
            'album_id': 'profile',
            'rev': 1,
            'count': 3
        })
        response = requests.get(url, params=params)
        try:
            response = requests.json()["response"]
            items = response["items"]
        except KeyError:
            return []
        photos = [item['sizes'][-1][url] for item in items]
        return photos

    def dating_search(self, user_data: dict):
        url = build_url(self.base_url, 'users.search?')
        params = get_common_params(self.token)
        if user_data['sex'] == 0:
            sex = 0
        elif user_data['sex'] == 1:
            sex = 2
        else:
            sex = 1

        age = safe_get_from_dict(user_data, 'age')
        age = int(age) if age != '' else 0

        if age == 0:
            min_age, max_age = 18, 40
        else:
            min_age, max_age = max(18, age - 3), max(18, age + 3)

        city = safe_get_from_dict(safe_get_from_dict(user_data, 'city'), 'id')
        if city == '' or sex == 0 or age == 0:
            return "Для поиска необходимо указать все данные - (город, пол, возраст)"

        for age_from in range(min_age, max_age + 1):
            for offset in range(0, 1000, 20):
                params.update({
                    'city': city,
                    'sex': sex,
                    'age_from': min_age,
                    'age_to': max_age,
                    "fields": "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation",
                    'count': 20,
                    'offset': offset
                })
                response = requests.get(url, params=params)
                try:
                    response = response.json()["response"]
                    count, items = response["count"], response["items"]
                except KeyError:
                    return f"Не удалось найти собеседника"
                self.results.add_user(self.user_id['id'])
        for _, item in enumerate(items):
            if safe_get_from_dict(item, 'bdate') == '':
                age = 0
            else:
                age = culc_age(safe_get_from_dict(item, 'bdate'))
            photos = self.get_user_photos(item['id'])
            user_dict = {
                'vk_profile_id': str(item['id']),
                'name': safe_get_from_dict(item, 'first_name'),
                'surname': safe_get_from_dict(item, 'last_name'),
                'age': age,
                'sex': item['sex'],
                'city': safe_get_from_dict(safe_get_from_dict(item, 'city'), 'title'),
                'photo_a_1': photos[0] if len(photos) > 0 else '',
                'photo_a_2': photos[1] if len(photos) > 1 else '',
                'photo_a_3': photos[2] if len(photos) > 2 else '',
                'photo_fr_1': photos[0] if len(photos) > 0 else '',
                'photo_fr_2': photos[1] if len(photos) > 1 else '',
                'photo_fr_3': photos[2] if len(photos) > 2 else '',
                'interests': safe_get_from_dict(item, 'interests'),
                'books': safe_get_from_dict(item, 'books'),
                'movies': safe_get_from_dict(item, 'movies'),
                'music': safe_get_from_dict(item, 'music')
            }
            result = self.dbOdject.add_user(user_dict)
            if result == 1:
                print(f"Не удалось добавить пользователя {user_dict['vk_profile_id']} в базу данных. Возраст: {user_dict['age']}")
            elif result == 0:
                print(f"Пользователь {user_dict['vk_profile_id']} добавлен в базу данных. Возраст: {user_dict['age']}")
            else:
                print(f"Произошла ошибка при добавлении пользователя {user_dict['vk_profile_id']} в базу данных. Возраст: {user_dict['age']}")

            # common_groups = self.get_common_groups(item['id'])
            # common_friends = self.get_common_friends(item['id'])
            # search_weights = Search_Weights(
            #     user_id=item['id'],
            #     music_interest_weight=safe_get_from_dict(item, 'music'),
            #     book_interest_weight=safe_get_from_dict(item, 'books'),
            #     common_groups=common_groups,
            #     common_friends=common_friends
            # )
            # self.dbObject.add_search_weights_db(search_weights)

        self.results.make_list_distinct(self.user_data['id'])
        self.results.randomize_data(self.user_data['id'])
        return f"Найдены записи о {_} пользователях для знакомства. Для просмотра нажмите кнопку 'Следующий в поиске'"



if __name__ == '__main__':
    

#     def users_info(self):
#         url = 'https://api.vk.com/method/users.get'
#         params = {'user_ids': self.id,
#                   'fields': 'sex, bdate, city'}
#         response = requests.get(url, params={**self.params, **params})
#         return response.json()
#
#     # https://dev.vk.com/ru/method/users.search - выбираем нужные данные по fields
#     def search_users(self, age_from, age_to, sex, city):
#         url = 'https://api.vk.com/method/users.search'
#         params = {'count': 15,  # Количество пользователей для отображения до 1000 можно указать
#                   'age_from': age_from,
#                   'age_to': age_to,
#                   'sex': sex,
#                   'city': city,
#                   'fields': 'sex, bdate, city, blacklisted, blacklisted_by_me, about, activities, books, music, movies, games'}
#         response = requests.get(url, params={**self.params, **params})
#         return response.json()
#
# access_token = '' # Токен
# user_id = '' # Id пользователя
# vk = VKBot(access_token, user_id)
#
# vk_info = vk.users_info()
# user_age = 2024 - int(vk_info['response'][0]['bdate'][-4:])  # Вычисляем возраст пользователя
#
# age_from = user_age - 5 #ищем от age_from лет
# age_to = user_age + 5 #до age_to лет
# sex = [2 if vk_info['response'][0]['sex'] == 1 else 1]  # 1 - женский, 2 - мужской, выбираем противоположный
# city = vk_info['response'][0]['city']['id']  # ID города пользоватетеля, можно город поменять если ищем по другому городу или расширить
#
# # Выводим информацию о пользователе
# print(vk.users_info()) # для просмотра данных json
# print(f"Имя: {vk_info['response'][0]['first_name']}")
# print(f"Фамилия: {vk_info['response'][0]['last_name']}")
# print(f"Возраст: {user_age}")
# print(f"Пол: {'Мужской' if vk_info['response'][0]['sex'] == 2 else 'Женский'}")
# print(f"Город: {vk_info['response'][0]['city']['title']}\n")
#
# # Получаем список пользователей, которые соответствуют заданным критериям
# search_result = vk.search_users(age_from, age_to, sex, city)
#
# # Выводим информацию найденных пользователей
# print('Выводим информацию найденных пользователей:')
# for user in search_result['response']['items']:
#     print(user) # для просмотра данных json
#     print(f"ID: {user['id']}")
#     print(f"Имя: {user['first_name']}")
#     print(f"Фамилия: {user['last_name']}")
#     print(f"Дата рождения: {user['bdate']}")
#     print(f"Пол: {'Мужской' if user['sex'] == 2 else 'Женский' if user['sex'] == 1 else 'Не указан'}")
#     print(f"Город: {user['city']['title']}") if 'city' in user else print("Город не указан")
#     print()
