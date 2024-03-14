import os
from configparser import ConfigParser
from datetime import datetime, timedelta
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from DB.create_db import Users, Blocklist, Photos, Likes, Favourites, Matches, Search_Weights, create_tables


config = ConfigParser()
config.read('../config.ini')


def get_token_id():
    name_db = config['DataBase']['name_db']
    user_db = config['DataBase']['user_db']
    password_db = config['DataBase']['password_db']
    return name_db, user_db, password_db


class ManageDB:

    def __init__(self, name_db: str, user_db: str, password_db: str, protocol_db: str = "postgresql",
                 host: str = "localhost", port: str = "5432") -> None:
        self.DSN = f"{protocol_db}://{user_db}:{password_db}@{host}:{port}/{name_db}"
        self.engine = sq.create_engine(self.DSN)
        create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine)()

    @staticmethod
    def db_connect_decorator(func):
        """
        Декоратор db_connect_decorator предназначен для автоматического управления соединением с базой данных в классе
        ManageDB. Он обеспечивает открытие соединения, выполнение метода класса, коммит изменений при успешном
        выполнении метода и откат изменений в случае возникновения исключения. После выполнения метода соединение с
        базой данных автоматически закрывается.

        Применение:
        1. Декоратор db_connect_decorator следует использовать для методов класса ManageDB, которые требуют соединения
        с базой данных.
        2. При вызове метода, обернутого в декоратор, он автоматически управляет открытием и закрытием соединения с
        базой данных.
        :param func:
        :return: db_connect
        """
        def db_connect(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.Session.commit()
            except Exception as e:
                print(f"Ошибка {e}")
                self.Session.rollback()
            finally:
                self.Session.remove()
        return db_connect

    @db_connect_decorator
    def get_user_by_vk_id(self, vk_profile_id: str) -> dict:
        """
        Получение словаря с данными пользователя по его vk id
        :param vk_profile_id:
        :return: dict
        """
        query = self.Session.query(Users.name, Users.surname, Users.sex, Users.age, Users.city, Users.vk_profile_id,
                                   Blocklist.is_blocked, Photos.photo_url, Likes.status_like, Favourites.photo_id)\
            .select_from(Users)\
            .join(Blocklist, Users.id == Blocklist.user_id)\
            .join(Photos, Users.id == Photos.user_id)\
            .join(Likes, Photos.id == Likes.photo_id)\
            .join(Favourites, Users.id == Favourites.user_id)\
            .filter(Users.vk_profile_id == vk_profile_id)
        result = query.first()
        if result:
            return {
                "name": result.name, "surname": result.surname,
                "sex": result.sex, "age": result.age, "city": result.city,
                "vk_profile_id": result.vk_profile_id
            }
        return {}

    @db_connect_decorator
    def if_user_in_db(self, vk_profile_id: str) -> bool:
        """
        Проверка на существование user в бд
        :param vk_profile_id:
        :return: true or false
        """
        query = self.Session.query(Users).filter(Users.vk_profile_id == vk_profile_id)
        if len(query.all()) > 0:
            return True
        else:
            return False

    @db_connect_decorator
    def add_users(self, user_info: dict) -> int:
        """
        Добавление пользователя в базу данных
        :param user_info:
            id - int
            name - str
            surname - str
            sex - str (Male or Female)
            age - int > 0
            city - str
            vk_profile_id int
        :return: Возвращает 0 если user уже есть в бд
        :return: Возвращает 1 если user меньше 18 лет
        :return: Возвращает 2 если user добавлен в бд
        """
        query = self.Session.query(Users.name, Users.surname, Blocklist.is_blocked,
                                   Photos.photo_url, Likes.status_like, Favourites.photo_id)\
            .select_from(Users)\
            .join(Blocklist, Users.id == Blocklist.user_id).join(Photos, Users.id == Photos.user_id)\
            .join(Likes, Photos.id == Likes.photo_id).ojin(Favourites, Users.id == Favourites.user_id)
        if int(user_info['age']) < 18:
            return 1
        # Проверка на существование пользователя в базе данных
        elif len(query.all()) > 0:
            return 0
        else:
            self.Session.add(
                Users(
                    id=user_info['id'],
                    name=user_info['name'],
                    surname=user_info['id'],
                    sex=user_info['sex'],
                    age=user_info['age'],
                    city=user_info['city'],
                    vk_profile_id=user_info['vk_profile_id']
                )
            )
            self.Session.commit()
            return 2

    @db_connect_decorator
    def updating_user(self, user_info: dict) -> bool:
        """
        Обновление пользователя в бд
        :param user_info:
            id - int
            name - str
            surname - str
            sex - str (Male or Female)
            age - int > 0
            city - str
            vk_profile_id int
        :return: True если user обновлён и False если нет.
        """
        pass



"""Также нужно реализовать эти функции!!!!!!!!!!!!!"""
# Добавление пользователя в бд избранных
# Удаление пользователя из избранных
# Добавление пользователя в чс
# Удаление пользователя из чс
# Получение списка избранных
# Получение чс


if __name__ == "__main__":
    name_db, user_db, password_db = get_token_id()

    DB = ManageDB(name_db, user_db, password_db)

    DB.add_users({"name": "Artem", "surname": "Pavlov", "sex": "Male", "age": 19, "vk_profile_id": 43456789})
    DB.add_users({"name": "Pavel", "surname": "Durov", "sex": "Male", "age": 18, "vk_profile_id": 40945653})
    DB.add_users({"name": "Olga", "surname": "Ivanova", "sex": "Female", "age": 25, "vk_profile_id": 19287465})

    DB.updating_user({"name": "Olga", "surname": "Voronina", "sex": "Female", "age": 23, "vk_profile_id": 19287465})
