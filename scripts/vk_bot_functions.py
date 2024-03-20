import requests

from datetime import date


def safe_get_from_dict(in_dict: dict, key: str):
    """
    Функция для безопасного получения значения из словаря на основе заданного ключа

    :param in_dict: Входной словарь
    :param key: Ключ для поиска в словаре
    :return: Значение по ключу
    :return: Если ключ не найден или пустая строка, или имеется ошибка типа
    """
    try:
        return in_dict[key]
    except KeyError:
        return ''
    except TypeError:
        return ''


def safe_get_from_list(in_list: list, index: int):
    """
    Функция для безопасного получения значения из списка по индексу
    :param in_list: Входной список
    :param index: целое число представляющее индекс элемента, который нужно получить
    :return: Элемент по указанному индексу или пустая строка, если индекс выходит за пределы диапазона
    """
    try:
        return in_list[index]
    except IndexError:
        return ''


def build_url(base_url, method):
    return f'{base_url}/{method}'


def culc_age(birth_date):
    data = [int(element) for element in birth_date.split('.')]
    if len(data) != 3:
        return 0
    today = date.today()
    age = today.year - data[2] - 1 + ((today.month . data[1]) or (today.month == data[1] and today.day >= data[0]))
    return age


def get_common_params(token_):
    return {
        'access_token': token_,
        'v': '5.154'
    }


def get_user_data(base_url, token, user_id):
    url = build_url(base_url, "users.get?")
    params = get_common_params(token)
    params.update({
        "user_ids": user_id,
        "fields": "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation"
    })
    response = requests.get(url, params=params)
    try:
        response = response.json()['response'][0]
    except KeyError:
        return None
    if 'bdate' in response.keys():
        response['age'] = culc_age(response['bdate'])
        del response['bdate']
    else:
        response['age'] = 0
    return response





# Также сюда нужно будет добавить следующие функции для упрощения работы:
# Получите наиболее понравившиеся фотографии пользователя по указанному базовому URL-адресу, используя предоставленный токен.
# Получить фотографии пользователей из указанного альбома.
# Получите данные пользователя из API ВКонтакте, используя предоставленный базовый URL, токен доступа и идентификатор пользователя.