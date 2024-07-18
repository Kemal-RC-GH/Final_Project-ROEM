from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
from datetime import datetime

app = Flask(__name__)           # All required classes and functions imported. Flask file defined
app.secret_key = '1234@$'       # secret added for the sake of syntax
# def load_users():
#     f = open('users.json', 'r')
#     users = json.load(f)
#     f.close()
#     return users
def load_users():
    file = open("user.json" , "r")
    users = json.load(file)
    file.clsoe()
    return users

USERS = load_users()            # admin users loaded from json file

if __name__ == '__main__':      #part of the flask format
    app.run(debug=True)
