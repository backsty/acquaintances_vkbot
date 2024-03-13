"""
VK - БОТ
"""
from random import randrange

import json

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import requests
from urllib.parse import urlencode

token = ('vk1.a.a1Z0lP2MH'
         '-s3wOkXEnsGUFK1P_Wq5r4eJMXQ6kiLLtRanBnZwoaQGXqewA5NsQ48jYzPiC1o26gS0qR9POKSLxJlTnOl_NMgiIhG9w4_d'
         'qBvK_ZMjLJZfipuv5UvnOEe0ihX_WmGPXJzeg5PfdvQRQs9xTtf1BWXTswS_AlEJUXABX4ELNF6zgW57qnzZ5Pma_85ZmT-nyIGCYmI6NXQFg')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

vk_api.keyboard.VkKeyboard()
initial_keyboard = VkKeyboard()
initial_keyboard.add_button('Начать поиск', color=VkKeyboardColor.PRIMARY)

chose_gender_keyboard = VkKeyboard(one_time=True)

chose_gender_keyboard.add_button('Парней', color=VkKeyboardColor.PRIMARY)
# chose_gender_keyboard.add_line()
chose_gender_keyboard.add_button('Девушек', color=VkKeyboardColor.NEGATIVE)

chose_age_keyboard = VkKeyboard(one_time=True)
chose_age_keyboard.add_button('18-25', color=VkKeyboardColor.PRIMARY)
chose_age_keyboard.add_button('26-35', color=VkKeyboardColor.PRIMARY)
chose_age_keyboard.add_line()
chose_age_keyboard.add_button('36-45', color=VkKeyboardColor.PRIMARY)
chose_age_keyboard.add_button('46-55', color=VkKeyboardColor.PRIMARY)
chose_age_keyboard.add_line()
chose_age_keyboard.add_button('56-65', color=VkKeyboardColor.PRIMARY)
chose_age_keyboard.add_button('66-75', color=VkKeyboardColor.PRIMARY)



def write_msg(user_id, message, keyboard=None):
    vk.method('message'
              's.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                         'keyboard': keyboard})


def create_user():
    pass

def first_appearance():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "Начать":
                    create_user()
                    """
                        Добавляем юзера в БД
                    """
                    write_msg(event.user_id, "Кого ищем?", chose_gender_keyboard.get_keyboard())
                    chose_gender()

                else:
                    write_msg(event.user_id, "Не понял вашего ответа. Пожалуйста, воспользуйтесь клавиатурой.",
                              initial_keyboard.get_keyboard())


def chose_gender():
    for cg_event in longpoll.listen():
        if cg_event.type == VkEventType.MESSAGE_NEW:

            if cg_event.to_me:
                cg_request = cg_event.text

                if cg_request == "Парни":
                    write_msg(cg_event.user_id, f"Какой возраст?", chose_age_keyboard.get_keyboard())
                    chose_age()

                elif cg_request == "Девушки":
                    write_msg(cg_event.user_id, f"Какой возраст", chose_age_keyboard.get_keyboard())
                    chose_age()

                else:
                    write_msg(cg_event.user_id, "Не понял вашего ответа. Пожалуйста, воспользуйтесь клавиатурой.",
                              chose_gender_keyboard.get_keyboard())


def chose_age():
    for ca_event in longpoll.listen():
        if ca_event.type == VkEventType.MESSAGE_NEW:

            if ca_event.to_me:
                ca_request = ca_event.text

                if ca_request == "Парни":

                    write_msg(ca_event.user_id, f"Вы выбрали поиск парней. Укажите нужный возраст.",
                              chose_age_keyboard.get_keyboard())

                elif ca_request == "Девушки":
                    write_msg(ca_event.user_id, f"Вы выбрали поиск девушек. Укажите нужный возраст",
                              chose_age_keyboard.get_keyboard())

                else:
                    write_msg(ca_event.user_id, "Не понял вашего ответа. Пожалуйста, воспользуйтесь клавиатурой.",
                              chose_age_keyboard.get_keyboard())


response = requests.get()
def make_link_for_token():

    vk_url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': 51794519,
        "redirect_uri": '',
        'display': 'page',
        'scope': 'photos',
        'response_type': 'token'
    }
    oath_url = f'{vk_url}?{urlencode(params)}'
    print(oath_url)
    response = requests.get(f'{vk_url}?{urlencode(params)}')