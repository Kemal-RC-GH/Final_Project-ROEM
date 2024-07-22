from flask import session, json

class Users:
    def __init__(self, users_file_path):    # properties of the class defined
        self.users_file_path = users_file_path
        self.USERS = self.load_users()

    def load_users(self):   # admin users loaded from json file
        file = open(self.users_file_path, "r")
        users = json.load(file)
        file.close()
        return users

    def save_users(self, users):
        file = open(self.users_file_path, "w")
        json.dump(users, file)
        file.close()

users_instance = Users("users.json") # Initialize Users instance