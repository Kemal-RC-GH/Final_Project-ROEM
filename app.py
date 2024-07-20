from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
from datetime import datetime

app = Flask(__name__)           # All required classes and functions imported. Flask file defined
app.secret_key = "1234@$"       # secret added for the sake of syntax


class Users:
    
    def __init__(self, users_file_path):
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

def login_validation(username, password):
    users = users_instance.USERS
    if users.get(username) == password:
        session["username"] = username
        return True          # if both username and password are correct return true
    return False
                    
def get_events(username):
    events = []                 #initialize empty event

    try:
        file = open("events.txt" , "r")
        for line in file:
            event_parts = line.strip().split(",")
            if len(event_parts) == 4:
                event_id, title, description, date = event_parts 
                if username == title.split("-")[0]: 
                    events.append({"id": event_id, "title": title, "description" : description, "date": date})            # title of the event and its username split
        file.close()
    except FileNotFoundError:                   # if file is currupt or have problems
        print("event.txt file not found!")
    return events                               # we get the event now

def save_event(event):
    file = open("events.txt", "a")
    file.write(event["id"] + "," + event["title"] + "," + event["description"] + "," + event["date"] + "\n")
    file.close()                            # events created should be saved in the events.txt file

def is_event_available(username, date_str, event_id=None):
    events = get_events(username)
    for event in events:                                                # event id should also be checked to allow editting 
        if event["date"] == date_str and (event_id is None or event["id"] != event_id):
            return False
    return True                                                     # Here we check the availability of the event on the same date to avoid duplication

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
    events = get_events(session["username"])
    for i, e in enumerate(events):
        if e["id"] == event_id:
            del events[i]
            break
    
    file = open("events.txt", "w")
    for e in events:
        file.write("{},{},{},{}\n".format(e["id"], e["title"], e["description"], e["date"]))
    file.close()


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
        users = users_instance.USERS
        user_password = users.get(username)
        if user_password and user_password == password:     # Here we check availabilty of user password and then we compare it to stored password
            session["username"] = username
            return redirect("/dashboard")
        flash("Invalid username or password!")
    return render_template("login.html", flash_message=get_flashed_messages())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:                    # password confiramation
            flash("Passwords do not match!")
            return render_template("register.html", flash_message=get_flashed_messages())

        users = users_instance.USERS          
        username_exists = False
        for key in users.keys():                # Here we are going to check if the username exists
            if key == username:
                username_exists = True
                break

        if username_exists:          # Here if username exists, it will flash a message otherwise will register
            flash("Username already exists!")
            return render_template("register.html", flash_message=get_flashed_messages())
      
        users[username] = password   # build the new dictionary
        users_instance.save_users(users)            # save it to the json file using save_user function
        session["username"] = username # update session for direct login and flash the below message
        flash("Registration successful! Please log in.")
        return redirect("/dashboard")
    
    return render_template("register.html", flash_message=get_flashed_messages())

@app.route("/dashboard", methods=["GET"])
def dashboard():
    username_in_session = False         #here we need to chheck if the user is in session
    for key in session.keys():
        if key == "username":
            username_in_session = True
            break

    if username_in_session:                     # As the user is in session, we need to load the respective users events
        events = get_events(session["username"])
        return render_template("dashboard.html", events=events, username=session["username"])
    return redirect("/login")

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    try:
        session_username = session["username"]           # check wether the username is in session
    except KeyError:
        return redirect("/login")

    if request.method == "POST":                        # post the form for the user
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        date_str = request.form["date"].strip()
        username = session_username + "-"
        event_id = str(datetime.now().timestamp()).split(".")[0]   # generate unique event ids and this the python module used

        if title == "" or description == "" or date_str == "":
            flash("Please fill all fields!")                        # if user tried to create event without providing required infos
            return render_template("create_event.html", flash_message=get_flashed_messages())

        if is_event_available(session_username, date_str, event_id) == False:
            flash("Event already exists for this date!")                            # call event availability function to aviod duplication
            return render_template("create_event.html", event_id=event_id, flash_message=get_flashed_messages())   

        new_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}
        save_event(new_event)                                       # save new event using save_event function to the text file
        return redirect("/dashboard")
    
    return render_template("create_event.html")

@app.route("/edit_event/<string:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    try:
        session_username = session["username"]                  # check wether the username is in session
    except KeyError:                                    
        return redirect("/login")

    if request.method == "GET":                                     # get the updates from the user
        events = get_events(session_username)
        event = next((e for e in events if e["id"] == event_id), None)  # loops in the events list and finds the event to compare it with the event id
        if event:
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
            flash("Please fill all fields!")                                # if user tried to create event without providing required infos
            return render_template("edit_event.html", event_id=event_id, flash_message=get_flashed_messages())

        if is_event_available(session_username, date_str, event_id) == False:
            flash("Event already exists for this date!")
            return render_template("edit_event.html", event_id=event_id, flash_message=get_flashed_messages())

        updated_event = {"id": event_id, "title": username + title, "description": description, "date": date_str}
        update_event(updated_event)                                         # save edited event using update_event function to the text file
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
            return redirect("/dashboard", flash_message=get_flashed_messages())

    elif request.method == "POST":
        success = delete_event_from_file(event_id)  # Call the function to delete from file
        if not success:
            flash("Error deleting event!")
            return redirect("/dashboard")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)                       #  here session is stopped and redirected to the index page
    return redirect("/")

                          
if __name__ == "__main__":      #part of the flask format
    app.run(debug=True)
