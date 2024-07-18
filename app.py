from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
from datetime import datetime

app = Flask(__name__)           # All required classes and functions imported. Flask file defined
app.secret_key = '1234@$'       # secret added for the sake of syntax

def load_users():
    file = open("user.json" , "r")
    users = json.load(file)
    file.clsoe()
    return users

USERS = load_users()            # admin users loaded from json file

def login_validation(username, password):
    if USERS.get(username) == password:
        session["username"] = username
        return True
    return False                # if both username and password are correct return true

def get_events(username):
    events = []                 #initialize empty event
    
    try:
        file = open("events.txt" , "r")
        for line in file:
            event_parts = line.strip().split(",")
            if len(event_parts) == 4:
                event_id, title, description, date = event_parts 
                if username == title.split("_")[0]: 
                    events.append({"id": event_id, "title": title, "description" : description, "date": date})            # title of the event and its username split
        file.close()
    except FileNotFoundError:                   # if file is currupt or have problems
        print("event.txt file not found!")
    return events                               # we get the event now
                          
if __name__ == '__main__':      #part of the flask format
    app.run(debug=True)
