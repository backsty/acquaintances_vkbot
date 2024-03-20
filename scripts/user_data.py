import random


class UserResultData:

    def __init__(self):
        self.users = {}
        self.current_user = {}
        self.last_fav_num = {}
        self.last_block_num = {}

    def add_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = []

    def add_data(self, user_id, data):
        if user_id in self.users:
            self.users[user_id].append(data)
        else:
            self.users[user_id].append(data)

    def get_data(self, user_id):
        if user_id not in self.users:
            return ''
        if len(self.users[user_id]) == 0:
            return ''
        return self.users[user_id].pop(0)

    # Удаление данных для конкретного пользователя
    def erase_data(self, user_id):
        self.users[user_id] = []

    def deleting_specific_users_data(self, user_id):
        random.shuffle(self.users[user_id])

    def make_list_user_distinct(self, user_id):
        self.users[user_id] = list(set(self.users[user_id]))

    def get_last_fav_num(self, user_id):
        if user_id not in self.last_fav_num:
            self.last_fav_num[user_id] = 0
        return self.last_fav_num[user_id]

    def get_last_block_num(self, user_id):
        if user_id not in self.last_block_num:
            self.last_block_num[user_id] = 0
        return self.last_block_num[user_id]




