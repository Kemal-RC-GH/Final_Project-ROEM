### Project Requirements

✅ It is available on GitHub.

✅ It uses the Flask web framework.

✅ It uses at least one module from the Python Standard Library other than the random module. Please provide the name of the module you are using in your app.

      Module names: Datetime, JSON
      
✅ It contains at least one class written by you that has both properties and methods. It uses __init__() to let the class initialize the object's attributes (note that __init__() doesn't count as a method).

This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.

    File name for the class definition: utility.py > class Users 
    
    Line number(s) for the class definition: from line 3 to line 19
    
    Name of two properties: self.users_file_path = users_file_path, self.USERS = self.load_users(), 
    
    Name of two methods: USERS or load_users, save_users.....
    
    File name and line numbers where the methods are used: routes.py > USERS (line 46), save_users(line 52)....
    
✅ It makes use of JavaScript in the front end and uses the localStorage of the web browser.

✅ It uses modern JavaScript (for example, let and const rather than var).

✅ It makes use of the reading and writing to the same file feature. from JSON file for admin users and from events.txt for events.

✅ It contains conditional statements. Please provide below the file name and the line number(s) of at least one example of a conditional statement in your code.

        File name: local_Storag.js
        
        Line number(s): 4 and 12
      
✅ It contains loops. Please provide below the file name and the line number(s) of at least one example of a loop in your code.

        File name: utility.py

        Line number(s): 40, 59, 66  ....

✅ It lets the user enter a value in a text box at some point. login and register. This value is received and processed by your back end Python code.

✅ It doesn't generate any error message even if the user enters a wrong input.

✅ It has styles using CSS.

✅ The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use              print() or console.log() for any information the app user should see. Instead, all user feedback needs to be visible in the browser.

✅ All exercises have been completed as per the requirements and pushed to the respective GitHub repository.



### Refugee Organizations Events Managing Website (ROEM)

This is a Flask application that allows admin users of refugee organizations in Cairo Egypt to create, manage, and view their events. It utilizes plain HTML, CSS, and JavaScript for the frontend functionality.

# Features:

✅ User login and authentication

✅ Create new events

✅ Edit existing events

✅ View upcoming events

✅ Delete events

✅ Responsive design using CSS

# Requirements:

✅ Python 3

✅ Flask framework

        pip install Flask


# Installation:

✅ Clone this repository.

✅ Run the application:

        flask --app app.py --run
        flask --app app.py --debug run

# Project Structure:

✅ app.py: Main Flask application file containing routes and logic.

✅ templates: Folder containing HTML templates for different pages (e.g., login, dashboard, etc.).

✅ static: Folder containing static assets:

✅ style.css: Stylesheet for the website's appearance.

✅ scripts (min_date.js, local_storage.js and welcome_admin.js): Custom JavaScript code for interactivity.

# Additional Notes:

    🔻 This is a basic website and can be extended with additional features like event categories, reminders, or invitations.
        
    🔻 The code currently stores events in a plain text file (events.txt). You can consider using a database for real-world applications.
        
    🔻 The provided JavaScript files might be optional and can be used for basic functionalities like date validation or UI enhancements.

# Getting Started:

    🔻 Run the flask:  flask --app app.py --debug run

    🔻 Visit http://127.0.0.1:5000/ in your web browser.
    
    🔻 Register and Login using the default credentials (if you haven't modified them).
    
    🔻 Explore the functionalities to create, edit, and manage your events.

# I hope you find this event organizer website helpful! ©️

