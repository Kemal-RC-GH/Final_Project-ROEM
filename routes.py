from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
from datetime import datetime
from utility import users_instance, get_events, is_event_available, save_event, update_event, delete_event_from_file, is_valid_password, login_validation

app = Flask(__name__)           # All required classes and functions imported. Flask file defined
app.secret_key = "1234@$"       # secret added for the sake of syntax

@app.route("/", methods=["GET"])
def index():
    username = session.get("username")
    if username:
        return redirect("/login")
    return render_template("index.html")        # route defined for admin login 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "" or password == "":
            flash("Please fill all fields!")          # if user tried to login without providing required info
            return render_template("register.html", flash_message=get_flashed_messages())

        if not is_valid_password(password):
            flash("Password does not meet the criteria!")
            return render_template("login.html", flash_message=get_flashed_messages())

        if login_validation(username, password):     # Here we check availability of user password and then we compare it to stored password
            return redirect("/dashboard")
        flash("Invalid username or password!")
    
    return render_template("login.html", flash_message=get_flashed_messages())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]


        if username == "" or password == "" or confirm_password == "":
            flash("Please fill all fields!")          # if user tried to register without providing required info
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

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        return redirect("/login")

    events = get_events(session["username"])
    events_available = len(events) > 0
    return render_template("dashboard.html", events=events, events_available=events_available, username=session["username"])

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    try:
        session_username = session["username"]           # check whether the username is in session
    except KeyError:
        return redirect("/login")

    if request.method == "POST":                        # post the form for the user
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        date_str = request.form["date"].strip()
        username = session_username + "-"
        event_id = str(datetime.now().timestamp()).split(".")[0]   # generate unique event ids and this the python module used

        if title == "" or description == "" or date_str == "":
            flash("Please fill all fields!")          # if user tried to create event without providing required info
            return render_template("create_event.html", flash_message=get_flashed_messages())

        if not is_event_available(session_username, date_str):  # Call event availability function to avoid duplication
            flash("Event already exists for this date!")
            return render_template("create_event.html", event_id=event_id, flash_message=get_flashed_messages())

        new_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}
        save_event(new_event)        # Save new event using save_event function to the text file
        return redirect("/dashboard")
    
    return render_template("create_event.html")

@app.route("/edit_event/<string:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    try:
        session_username = session["username"]  # Check whether the username is in session
    except KeyError:
        return redirect("/login")

    if request.method == "GET":  # retrieves the events info
        events = get_events(session_username)
        event = next((e for e in events if e["id"] == event_id), None)  # Find the event by id
        if event:
            event["title"] = event["title"].replace(session_username + "-", "")  # Remove username from the title for editing
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
            flash("Please fill all fields!")  # If user tried to create event without providing required info
            event = {"id": event_id, "title": title, "description": description, "date": date_str}
            return render_template("edit_event.html", event=event, flash_message=get_flashed_messages())

        if not is_event_available(session_username, date_str, event_id):  # Pass event_id to exclude the current event
            flash("Event already exists for this date!")
            event = {"id": event_id, "title": title, "description": description, "date": date_str}
            return render_template("edit_event.html", event=event, flash_message=get_flashed_messages())

        updated_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}  # Use the updated title directly
        update_event(updated_event)  # Save edited event using update_event function to the text file
        return redirect("/dashboard")

    flash("Method not allowed")
    return redirect("/dashboard")

@app.route("/delete_event/<string:event_id>", methods=["GET", "POST"])
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
        delete_event_from_file(event_id)  # Call the function to delete from file
        return redirect("/dashboard")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)  # Here session is stopped and redirected to the index page
    return redirect("/")

if __name__ == "__main__":  # Part of the flask format
    app.run(debug=True)
