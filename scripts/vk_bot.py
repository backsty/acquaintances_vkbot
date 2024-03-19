import requests
class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id,
                  'fields': 'sex, bdate, city'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    # https://dev.vk.com/ru/method/users.search - выбираем нужные данные по fields
    def search_users(self, age_from, age_to, sex, city):
        url = 'https://api.vk.com/method/users.search'
        params = {'count': 15,  # Количество пользователей для отображения до 1000 можно указать
                  'age_from': age_from,
                  'age_to': age_to,
                  'sex': sex,
                  'city': city,
                  'fields': 'sex, bdate, city, blacklisted, blacklisted_by_me, about, activities, books, music, movies, games'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

access_token = '' # Токен
user_id = '' # Id пользователя
vk = VK(access_token, user_id)

vk_info = vk.users_info()
user_age = 2024 - int(vk_info['response'][0]['bdate'][-4:])  # Вычисляем возраст пользователя

age_from = user_age - 5 #ищем от age_from лет
age_to = user_age + 5 #до age_to лет
sex = [2 if vk_info['response'][0]['sex'] == 1 else 1]  # 1 - женский, 2 - мужской, выбираем противоположный
city = vk_info['response'][0]['city']['id']  # ID города пользоватетеля, можно город поменять если ищем по другому городу или расширить

# Выводим информацию о пользователе
print(vk.users_info()) # для просмотра данных json
print(f"Имя: {vk_info['response'][0]['first_name']}")
print(f"Фамилия: {vk_info['response'][0]['last_name']}")
print(f"Возраст: {user_age}")
print(f"Пол: {'Мужской' if vk_info['response'][0]['sex'] == 2 else 'Женский'}")
print(f"Город: {vk_info['response'][0]['city']['title']}\n")

# Получаем список пользователей, которые соответствуют заданным критериям
search_result = vk.search_users(age_from, age_to, sex, city)

# Выводим информацию найденных пользователей
print('Выводим информацию найденных пользователей:')
for user in search_result['response']['items']:
    print(user) # для просмотра данных json
    print(f"ID: {user['id']}")
    print(f"Имя: {user['first_name']}")
    print(f"Фамилия: {user['last_name']}")
    print(f"Дата рождения: {user['bdate']}")
    print(f"Пол: {'Мужской' if user['sex'] == 2 else 'Женский' if user['sex'] == 1 else 'Не указан'}")
    print(f"Город: {user['city']['title']}") if 'city' in user else print("Город не указан")
    print()
