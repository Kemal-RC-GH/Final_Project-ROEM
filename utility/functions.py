from flask import session
from utility.users import users_instance
import re

def login_validation(username, password):
    # Validate login credentials
    users = users_instance.USERS
    if users.get(username) == password:
        session["username"] = username
        return True
    return False

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


def get_events(username):
    events = []                 # initialize empty event list
    try:
        file = open("events.txt" , "r")
        for line in file:
            event_parts = line.strip().split(",")
            if len(event_parts) == 4:
                event_id, title, description, date = event_parts 
                if username == title.split("-")[0]: 
                    events.append({"id": event_id, "title": title, "description": description, "date": date}) 
        file.close()
    except FileNotFoundError:                   
        print("events.txt file not found!")    # if file is corrupt or has problems
    return events

def save_event(event):
    file = open("events.txt", "a")
    file.write(event["id"] + "," + event["title"] + "," + event["description"] + "," + event["date"] + "\n")
    file.close()

def is_event_available(username, date_str, event_id=None):
    events = get_events(username)
    for event in events:       # event id should also be checked to allow editing 
        if event["date"] == date_str and (event_id is None or event["id"] != event_id):
            return False
    return True    # Here we check the availability of the event on the same date to avoid duplication

def update_event(event):
    events = get_events(session["username"])
    for i, e in enumerate(events):              
        if e["id"] == event["id"]:
            events[i] = event
            break
    file = open("events.txt", "w")
    for e in events:
        line = "{},{},{},{}\n".format(e["id"], e["title"], e["description"], e["date"])
        file.write(line)
    file.close()

def delete_event_from_file(event_id):
    events = get_events(session["username"]) # here event is deleted from text file using write
    for i, e in enumerate(events):
        if e["id"] == event_id:
            del events[i]
            break
    file = open("events.txt", "w")
    for e in events:
        file.write("{},{},{},{}\n".format(e["id"], e["title"], e["description"], e["date"]))
    file.close()

