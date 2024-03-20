from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from scripts.vk_bot import VKBot
from scripts.user_data import UserResultData

import configparser
from DB.manage_db import ManageDB


def get_token(file_name: str = '../config.ini'):
    config = ConfigParser()
    config.read(file_name)

    group_token = config['ScriptsVK']['group_token']
    personal_token = config['ScriptsVK']['personal_token']
    name_db = config['DataBase']['name_db']
    user_db = config['DataBase']['user_db']
    password_db = config['DataBase']['password_db']

    return group_token, personal_token, name_db, user_db, password_db


def start_VKBot(token_1, token_2):
    vk = vk_api.VkApi(token=token_1)
    longpoll = VkLongPoll(vk)

    def write_message(user_id, message, keyboard=None, attachment=None):
        pass


if __name__ == '__main__':
    group_token, personal_token, name_db, user_db, password_db = get_token()
    DB = ManageDB(name_db=name_db, user_db=user_db, password_db=password_db)
    start_VKBot(group_token, personal_token)