"""
VK - БОТ
"""
from random import randrange

import configparser

import vk_api
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import requests
from urllib.parse import urlencode

from VKinder_db import Matches, User, Favorite, create_bd, Blacklisted

config = configparser.ConfigParser()
config.read("settings.ini")

vk = vk_api.VkApi(token=config["VKinder"]["app_token"])
longpoll = VkLongPoll(vk)

vk_api.keyboard.VkKeyboard()

start_review_keyboard = VkKeyboard()
start_review_keyboard.add_button('Начать просмотр', color=VkKeyboardColor.PRIMARY)

chose_gender_keyboard = VkKeyboard(one_time=True)
chose_gender_keyboard.add_button('Парни', color=VkKeyboardColor.PRIMARY)
chose_gender_keyboard.add_button('Девушки', color=VkKeyboardColor.NEGATIVE)

send_match_keyboard = VkKeyboard(one_time=True)
send_match_keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
send_match_keyboard.add_button('Дальше', color=VkKeyboardColor.PRIMARY)
send_match_keyboard.add_line()
send_match_keyboard.add_button('Поставить лайк', color=VkKeyboardColor.NEGATIVE)
send_match_keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
send_match_keyboard.add_line()
send_match_keyboard.add_button('Показать избранное', color=VkKeyboardColor.SECONDARY)
send_match_keyboard.add_button('Добавить в чёрный список', color=VkKeyboardColor.SECONDARY)
send_match_keyboard.add_line()
send_match_keyboard.add_button('Начать новый поиск', color=VkKeyboardColor.SECONDARY)

send_favourite_keyboard = VkKeyboard(one_time=True)
send_favourite_keyboard.add_button("Назад", color=VkKeyboardColor.PRIMARY)
send_favourite_keyboard.add_button("Дальше", color=VkKeyboardColor.PRIMARY)
send_favourite_keyboard.add_line()
send_favourite_keyboard.add_button("Вернуться к поиску", color=VkKeyboardColor.SECONDARY)
send_favourite_keyboard.add_line()
send_favourite_keyboard.add_button("Удалить из избранного", color=VkKeyboardColor.SECONDARY)


# TODO: реализовать удаление из избранного


def write_msg(user_id: int, message, keyboard=None, attachment=None):
    vk.method('message'
              's.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                         'keyboard': keyboard, 'attachment': attachment})


def add_user(vk_id, token, city):
    DSN = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(DSN)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_user = User(vk_id=vk_id, token=token, city=city, step=0, f_step=0)
    session.add(new_user)
    session.commit()
    session.close()


def get_user_info(user_id: int):
    user_info = vk.method('users.get', {
        'user_id': user_id, 'fields': 'first_name, last_name, bdate, domain, has_photo, city'
    })
    return user_info[0]


def bot_listening():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "Начать":
                    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                    engine = create_engine(bd_address)

                    session = sessionmaker(bind=engine)
                    session = session()
                    create_bd(engine)
                    if session.query(User).filter(User.vk_id == int(event.user_id)).first() is None:
                        user_token = get_correct_user_token(event.user_id)
                        user_info = get_user_info(event.user_id)
                        add_user(event.user_id, user_token, int(user_info.get("city").get("id")))

                    search_people(event.user_id)

                elif request == "Дальше" or request == "Начать просмотр":
                    send_match(event.user_id, True)

                elif request == "Назад":
                    send_match(event.user_id, False)

                elif request == "Добавить в избранное":
                    add_favorite(event.user_id)
                    write_msg(event.user_id, "Пользователь добавлен в избранное",
                              send_match_keyboard.get_keyboard())

                elif request == "Показать избранное":
                    parce_favorite(event.user_id)

                elif request == "Начать новый поиск":
                    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                    engine = create_engine(bd_address)
                    session = sessionmaker(bind=engine)
                    session = session()
                    user = session.query(User).where(User.vk_id == int(event.user_id)).first()
                    matches = session.query(Matches).filter(Matches.user_id == int(event.user_id)).all()
                    user.step = 0
                    for match in matches:
                        session.delete(match)
                    session.commit()
                    search_people(event.user_id)

                elif request == "Добавить в чёрный список":
                    add_to_blocklist(event.user_id)

                else:
                    write_msg(event.user_id, "Не понял вашего ответа. Пожалуйста, воспользуйтесь клавиатурой.",
                              start_review_keyboard.get_keyboard())


def chose_gender(user_id):
    write_msg(user_id, "Выбери интересующий тебя пол.", chose_gender_keyboard.get_keyboard())
    for cg_event in longpoll.listen():
        if cg_event.type == VkEventType.MESSAGE_NEW:

            if cg_event.to_me:
                cg_request = cg_event.text
                sex = 0
                if cg_request == "Девушки":
                    sex = 1

                elif cg_request == "Парни":
                    sex = 2

                else:
                    write_msg(cg_event.user_id, "Не понял вашего ответа. Пожалуйста, воспользуйтесь клавиатурой.",
                              chose_gender_keyboard.get_keyboard())

                return sex


def chose_lower_age(user_id):
    write_msg(user_id, "Введи нижнюю планку возраста:", start_review_keyboard.get_empty_keyboard())
    for ca_event in longpoll.listen():
        if ca_event.type == VkEventType.MESSAGE_NEW:

            if ca_event.to_me:
                ca_request = ca_event.text
                lower_age = 0
                if check_age(ca_request):
                    lower_age = int(ca_request)

                else:
                    write_msg(ca_event.user_id, "Введи корректную нижнюю планку возраста")
                    chose_lower_age(user_id)
                return lower_age


def chose_upper_age(user_id):
    write_msg(user_id, "Введи верхнюю планку возраста:", start_review_keyboard.get_empty_keyboard())
    for ca_event in longpoll.listen():
        if ca_event.type == VkEventType.MESSAGE_NEW:
            upper_age = 0
            if ca_event.to_me:
                ca_request = ca_event.text

                if check_age(ca_request):
                    upper_age = int(ca_request)
                else:
                    write_msg(ca_event.user_id, "Введите корректную верхнюю планку возраста")
                    chose_upper_age(user_id)

                return upper_age


def check_age(response):
    if response.isdigit():
        if 18 <= int(response) <= 80:
            return True
        else:
            return False
    else:
        return False


def get_correct_user_token(user_id):
    vk_url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': 51794519,
        "redirect_uri": 'https://oauth.vk.com/blank.html',
        'display': 'page',
        'scope': 'friends, audio, groups, photos',
        'response_type': 'token'
    }
    oath_url = f'{vk_url}?{urlencode(params)}'
    write_msg(user_id, f'Для продолжения необходимо пройти по ссылке {oath_url}. Скопируй ссылку из адресной '
                       f'строки и отправь её боту.')
    for gcut_event in longpoll.listen():
        if gcut_event.type == VkEventType.MESSAGE_NEW:
            if gcut_event.to_me:
                request = gcut_event.text
                if request[request.find('vk1.a'): request.find('&amp;expires_in')] == "":
                    write_msg(user_id, 'Ссылка не корректна. Пожалуйста, попробуйте ещё раз.')
                    get_correct_user_token(user_id)
                else:

                    return request[request.find('vk1.a'): request.find('&amp;expires_in')]


def search_request(user_token: str, sex: int, city_id: int, lower_age: int, higher_age: int):
    if lower_age > higher_age:
        lower_age, higher_age = higher_age, lower_age
    search_params = {  # TODO Решить проблему с выдачей 1000 человек c помощью даты рождения(достаточно месяца и года,
        # TODO но нужна проверка через сайт вк)
        'access_token': user_token,
        'count': 1000,
        'offset': 0,
        'v': '5.199',
        'sex': sex,
        'city': city_id,
        'fields': 'is_friend, can_send_friend_request,can_write_private_message, domain, relation',
        'status': 6,  # в активном поиске
        'age_from': lower_age,
        'age_to': higher_age,
        'has_photo': 1,
    }
    search_response = requests.get(f'https://api.vk.com/method/users.search', params=search_params)
    return search_response.json()


def add_people_to_bd(search_result, user_id):
    for idx, people in enumerate(search_result.get('response').get('items')):
        if people.get("is_closed") is False or people.get("can_access_closed"):
            if people.get("is_friend") == 0:
                bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                engine = create_engine(bd_address)

                session = sessionmaker(bind=engine)
                session = session()
                match = Matches(
                    name=people.get("first_name"),
                    surname=people.get("last_name"),
                    vk_id=people.get('id'),
                    user_id=user_id,
                    step=idx + 1
                )
                session.add(match)
                session.commit()
                session.close()
    return send_match(user_id, True)


def get_photos(user_token: int, owner_id: int, offset: int = 0) -> str:
    photo_request_params = {
        'access_token': user_token,
        'v': '5.199',
        'owner_id': owner_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'offset': offset,
        'count': 200
    }
    photo_response = requests.get(f'https://api.vk.com/method/photos.get', params=photo_request_params)
    bd_string = ""
    if photo_response.json().get("response").get("count") > 200:
        all_photos = {}
        all_photos.update(
            {item.get('likes').get('count'): item.get("id") for item in photo_response.json().get(
                'response').get('items')}
        )
        while True:
            offset += 200
            photo_request_params.update({'offset': offset})
            photo_response = requests.get(f'https://api.vk.com/method/photos.get', params=photo_request_params)
            all_photos.update(
                {item.get('likes').get('count'): item.get('id') for item in photo_response.json().get(
                    'response').get('items')}
            )

            if len(photo_response.json().get("response").get("items")) < 200:
                for item in [
                    all_photos.get(sorted(all_photos)[-1]),
                    all_photos.get(sorted(all_photos)[-2]),
                    all_photos.get(sorted(all_photos)[-3])
                ]:
                    bd_string += f"photo{owner_id}_{item},"
                    return bd_string.strip(",")

    all_photos = {
        item.get('likes').get('count'): item.get("id") for item in photo_response.json().get(
            'response').get('items')}

    try:
        for item in [
            all_photos.get(sorted(all_photos)[-1]),
            all_photos.get(sorted(all_photos)[-2]),
            all_photos.get(sorted(all_photos)[-3])
        ]:
            bd_string += f"photo{owner_id}_{item},"
    except IndexError:
        for item_ in photo_response.json().get("response").get('items'):
            bd_string += f"photo{item_.get('owner_id')}_{item_.get('id')},"
    return bd_string.strip(",")


def send_match(user_id: int, forward: bool):
    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(bd_address)

    session = sessionmaker(bind=engine)
    session = session()

    user = session.query(User).where(User.vk_id == user_id).first()

    if forward:
        user.step += 1
    else:
        if user.step > 1:
            user.step -= 1
    session.commit()
    match = session.query(Matches).where(Matches.step == int(user.step)).first()
    if session.query(Blacklisted).where(Blacklisted.vk_id == int(match.vk_id)).first() is None:
        return write_msg(user_id, f'{match.name} {match.surname} http://vk.com/id{match.vk_id}',
                         send_match_keyboard.get_keyboard(),
                         f'{get_photos(user.token, match.vk_id)}')
    else:
        send_match(user_id, forward)


def add_favorite(user_id: int):
    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(bd_address)
    session = sessionmaker(bind=engine)
    session = session()

    user = session.query(User).where(User.vk_id == user_id).first()
    match = session.query(Matches).where(Matches.step == int(user.step)).first()
    favorite = session.query(Favorite).where(Favorite.user_id == user_id).order_by(desc(Favorite.f_step)).first()
    if favorite is None:
        f_step = 1
    else:
        f_step = favorite.f_step + 1

    favorite = Favorite(
        vk_id=match.vk_id,
        name=match.name,
        surname=match.surname,
        user_id=user.vk_id,
        f_step=f_step
    )
    session.add(favorite)
    session.commit()
    session.close()


def parce_favorite(user_id: int):
    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(bd_address)
    session = sessionmaker(bind=engine)
    session = session()

    user = session.query(User).where(User.vk_id == int(user_id)).first()
    user.f_step += 1
    session.commit()
    favorite = session.query(Favorite).where(Favorite.f_step == int(user.f_step)).first()
    if favorite is None:
        return write_msg(user_id, "Ты никого ещё не добавил в избранное")
    write_msg(user_id,
              f"{favorite.name} {favorite.surname}\n http://vk.com/id{favorite.vk_id}",
              send_favourite_keyboard.get_keyboard(),
              get_photos(user.token, favorite.vk_id))
    for fav_event in longpoll.listen():
        if fav_event.type == VkEventType.MESSAGE_NEW:

            if fav_event.to_me:
                fa_request = fav_event.text
                if fa_request == "Продолжить поиск":
                    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                    engine = create_engine(bd_address)
                    session = sessionmaker(bind=engine)
                    session = session()

                    user = session.query(User).where(User.vk_id == int(fav_event.user_id)).first()
                    user.f_step = 0
                    session.commit()

                    return write_msg(
                        fav_event.user_id, 'Нажмите кнопку "Дальше", чтобы продолжить поиск',
                        send_match_keyboard.get_keyboard()
                    )

                elif fa_request == "Дальше":
                    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                    engine = create_engine(bd_address)
                    session = sessionmaker(bind=engine)
                    session = session()
                    user = session.query(User).where(User.vk_id == int(fav_event.user_id)).first()
                    user.f_step += 1
                    session.commit()
                    favorite = session.query(Favorite).where(Favorite.f_step == int(user.f_step)).first()
                    if favorite is None:
                        write_msg(fav_event.user_id, "Ты никого больше не добавил в избранное")
                        user.f_step -= 1
                        session.commit()
                        continue
                    write_msg(fav_event.user_id,
                              f"{favorite.name} {favorite.surname}\n http://vk.com/id{favorite.vk_id}",
                              send_favourite_keyboard.get_keyboard(),
                              get_photos(user.token, favorite.vk_id))

                elif fa_request == "Назад":
                    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
                    engine = create_engine(bd_address)
                    session = sessionmaker(bind=engine)
                    session = session()

                    user = session.query(User).where(User.vk_id == int(fav_event.user_id)).first()
                    if user.f_step > 1:
                        user.f_step -= 1

                    else:
                        write_msg(fav_event.user_id, "Достигнуто начало списка избранного")
                        continue
                    session.commit()
                    favorite = session.query(Favorite).where(Favorite.f_step == int(user.f_step)).first()
                    write_msg(fav_event.user_id,
                              f"{favorite.name} {favorite.surname}\n http://vk.com/id{favorite.vk_id}",
                              send_favourite_keyboard.get_keyboard(),
                              get_photos(user.token, favorite.vk_id))

                elif fa_request == "Вернуться к поиску":
                    return write_msg(fav_event.user_id, "Возвращаюсь к поиску. Воспользуйся клавиатурой",
                                     send_match_keyboard.get_keyboard())


def search_people(vk_id):
    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(bd_address)
    session = sessionmaker(bind=engine)
    session = session()
    user = session.query(User).where(User.vk_id == int(vk_id)).first()
    if session.query(Matches.step).where(Matches.vk_id == int(vk_id)).order_by(desc(Matches.step)).first() is None:
        empty_match_table: bool = True
    for people in search_request(
            user.token, chose_gender(vk_id), user.city, chose_lower_age(vk_id), chose_upper_age(vk_id)
    ).get('response').get('items'):
        if empty_match_table:
            empty_match_table = False
            step = 0
        else:
            step = (
                session.query(Matches.step).where(Matches.user_id == int(vk_id)).order_by(desc(Matches.step)).first()
            ).step

        if people.get("is_closed") is False or people.get("can_access_closed") and people.get("is_friend") == 0:
            match = Matches(
                name=people.get("first_name"),
                surname=people.get("last_name"),
                vk_id=people.get('id'),
                user_id=vk_id,
                step=step + 1
            )
            session.add(match)
            session.commit()
    session.close()
    return write_msg(vk_id, "Поиск завершён", start_review_keyboard.get_keyboard())


# def add_like(user_id): TODO
#     pass


def add_to_blocklist(user_id: int):
    bd_address = 'postgresql://postgres:postgres@localhost:5432/vkinderdb'
    engine = create_engine(bd_address)
    session = sessionmaker(bind=engine)
    session = session()

    user = session.query(User).where(User.vk_id == int(user_id)).first()
    match = session.query(Matches).where(Matches.step == int(user.step)).first()
    blocklist_item = Blacklisted(
        vk_id=match.vk_id,
        user_id=user_id
    )
    session.add(blocklist_item)
    session.commit()
    session.close()
    return write_msg(user_id, "Пользователь добавлен в чёрный список", send_match_keyboard.get_keyboard())


if __name__ == '__main__':
    bot_listening()
