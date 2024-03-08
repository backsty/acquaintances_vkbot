import os
from configparser import ConfigParser
from datetime import datetime, timedelta
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from DB.create_db import Users, Blocklist, Photos, Likes, Favourites, Matches, Search_Weights, create_tables


config = ConfigParser()
config.read('config.ini')


def get_token_id():
    name_db = config['DataBase']['name_db']
    user_db = config['DataBase']['user_db']
    password_db = config['DataBase']['password_db']
    DSN = config['DataBase']['DSN']
    return name_db, user_db, password_db, DSN


class ManageDB:

    def __init__(self):
        pass

    def add_users(self):
        pass

# тут написать логику для теста Базы Данных


if __name__ == "__main__":
    name_db_, user_db_, password_db_, DSN_ = get_token_id()