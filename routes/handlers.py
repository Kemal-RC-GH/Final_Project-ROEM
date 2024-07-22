from flask import render_template, request, session, redirect, flash, get_flashed_messages
from utility.functions import (
    is_valid_password,
    login_validation,
    get_events,
    is_event_available,
    save_event,
    update_event,
    delete_event_from_file
)
from utility.users import users_instance
from datetime import datetime

def index():
    username = session.get("username")
    if username:
        return redirect("/login")
    return render_template("index.html")

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "" or password == "":
            flash("Please fill all fields!")
            return render_template("register.html", flash_message=get_flashed_messages())

        if not is_valid_password(password):
            flash("Password does not meet the criteria!")
            return render_template("login.html", flash_message=get_flashed_messages())

        if login_validation(username, password):
            return redirect("/dashboard")
        flash("Invalid username or password!")

    return render_template("login.html", flash_message=get_flashed_messages())

def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if username == "" or password == "" or confirm_password == "":
            flash("Please fill all fields!")
            return render_template("register.html", flash_message=get_flashed_messages())

        if password != confirm_password:
            flash("Passwords do not match!")
            return render_template("register.html", flash_message=get_flashed_messages())

        if not is_valid_password(password):
            flash("Password must be at least 8 characters long and contain at least one special character!")
            return render_template("register.html", flash_message=get_flashed_messages())

        users = users_instance.USERS
        if username in users:
            flash("Username already exists!")
            return render_template("register.html", flash_message=get_flashed_messages())

        users[username] = password
        users_instance.save_users(users)
        session["username"] = username
        return redirect("/dashboard")

    return render_template("register.html", flash_message=get_flashed_messages())

def logout():
    session.pop("username", None)
    return redirect("/")

def dashboard():
    if "username" not in session:
        return redirect("/login")

    events = get_events(session["username"])
    # Remove the username prefix from event titles
    cleaned_events = []
    for event in events:
        # Assuming the username prefix is always followed by a '-'
        title_without_username = event["title"].split("-", 1)[-1]
        cleaned_event = event.copy()  # Make a copy of the event dictionary
        cleaned_event["title"] = title_without_username  # Update the title
        cleaned_events.append(cleaned_event)
    
    events_available = len(cleaned_events) > 0
    return render_template("dashboard.html", events=cleaned_events, events_available=events_available, username=session["username"])


def create_event():
    try:
        session_username = session["username"]
    except KeyError:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        date_str = request.form["date"].strip()
        username = session_username + "-"
        event_id = str(datetime.now().timestamp()).split(".")[0]

        if title == "" or description == "" or date_str == "":
            flash("Please fill all fields!")
            return render_template("create_event.html", flash_message=get_flashed_messages())

        if not is_event_available(session_username, date_str):
            flash("Event already exists for this date!")
            return render_template("create_event.html", event_id=event_id, flash_message=get_flashed_messages())

        new_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}
        save_event(new_event)
        return redirect("/dashboard")

    return render_template("create_event.html")


def edit_event(event_id):
    try:
        session_username = session["username"]
    except KeyError:
        return redirect("/login")

    if request.method == "GET":
        events = get_events(session_username)
        event = next((e for e in events if e["id"] == event_id), None)
        if event:
            event["title"] = event["title"].replace(session_username + "-", "")
            return render_template("edit_event.html", event=event)
        else:
            flash("Event not found!")
            return redirect("/dashboard")

    elif request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        date_str = request.form["date"].strip()
        username = session_username + "-"

        if title == "" or description == "" or date_str == "":
            flash("Please fill all fields!")
            event = {"id": event_id, "title": title, "description": description, "date": date_str}
            return render_template("edit_event.html", event=event, flash_message=get_flashed_messages())

        if not is_event_available(session_username, date_str, event_id):
            flash("Event already exists for this date!")
            event = {"id": event_id, "title": title, "description": description, "date": date_str}
            return render_template("edit_event.html", event=event, flash_message=get_flashed_messages())

        updated_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}
        update_event(updated_event)
        return redirect("/dashboard")

    flash("Method not allowed")
    return redirect("/dashboard")

def delete_event(event_id):
    if "username" not in session:
        return redirect("/login")

    if request.method == "GET":
        event = next((e for e in get_events(session["username"]) if e["id"] == event_id), None)
        if event:
            return render_template("delete_event.html", event=event, flash_message=get_flashed_messages())
        else:
            flash("Event not found!")
            return redirect("/dashboard")

    elif request.method == "POST":
        delete_event_from_file(event_id)
        return redirect("/dashboard")
