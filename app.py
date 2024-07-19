from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
#from datetime import datetime

app = Flask(__name__)           # All required classes and functions imported. Flask file defined
app.secret_key = "1234@$"       # secret added for the sake of syntax

users_file_path = "users.json"
def load_users():
    file = open(users_file_path , "r")
    users = json.load(file)
    file.close()
    return users

def save_users(user):
    file = open(users_file_path, "w")
    json.dump(user, file)
    file.close()                        # registered users are saved in the users.json file    

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
        users = load_users()
        user_password = users.get(username)
        if user_password and user_password == password:
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

        if password != confirm_password:
            flash("Passwords do not match!")
            return render_template("register.html", flash_message=get_flashed_messages())

        users = load_users()          # Here we are going to check ifvthe username exists
        username_exists = False
        for key in users.keys():
            if key == username:
                username_exists = True
                break

        if username_exists:          # Here if username exists, it will flash a message otherwise will register
            flash("Username already exists!")
            return render_template("register.html", flash_message=get_flashed_messages())
      
        users[username] = password   # build the new dictionary
        save_users(users)            # save it to the json file using save_user function
        session["username"] = username # update session for direct login and flash the below message
        flash("Registration successful! Please log in.")
        return redirect("/login")
    
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

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/")

                          
if __name__ == "__main__":      #part of the flask format
    app.run(debug=True)
