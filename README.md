In order to successfully complete the course, your app will need to feature the following 
points:

•Available in Github: Yes

• It uses the Flask web framework: Yes
• It uses at least one module from the Python Standard Library other than 
the random module: Yes. datetime.now() module imported from flask

• It contains at least one class written by you that has both properties and 
methods (yes, plural!). It uses __init__() to let the class initialize the object's 
properties (note that __init__() doesn't count as a method). This includes 
instantiating the class and using the methods in your app. Methods that only print 
something in the terminal will not be considered: Yes done in line ............. of the ....... file. 

• It makes use of JavaScript in the front end and uses the localStorage of the web 
browser: Yes done in ......... file from line .... to ....

• It uses modern JavaScript (for example, let and const rather than var). Yes, all js files like ......

• It makes use of the writing to and reading from the same file feature: Yes, the events.txt file. 

• It contains both conditional statements and loops: Yes, it uses for as a loop in ........... and other parts and if and elif in .......
• It doesn't generate any error message even if the user enters a wrong input: Yes, errors are precisely handled

• It lets the user enter a value in a text box at some point. This value should be received 
and processed by your back end Python code: Yes for example create event form, takes data put it in the text file and then call it in the backend. 

• It is styled using CSS: Yes, I did a simple CSS style. 

• The code follows the code and style conventions we introduced in the course, is fully 
documented using comments and doesn't contain unused or experimental code. In 
particular, the code should not use print() or console.log() for any 
information the app user should see. Instead, all user feedback needs to be visible in 
the browser: Yes, done!



# Refugee Organizations Events Managing Website (ROEM)

This is a Flask application that allows admin users of refugee organizations in Cairo Egypt to create, manage, and view their events. It utilizes plain HTML, CSS, and JavaScript for the frontend functionality.

# Features:

User login and authentication

Create new events

Edit existing events

View upcoming events

Delete events

Responsive design using CSS

# Requirements:

Python 3

Flask framework

# Installation:

Clone this repository.

Run the application:
    python app.py

# Project Structure:

app.py: Main Flask application file containing routes and logic.

templates: Folder containing HTML templates for different pages (e.g., login, dashboard, etc.).

static: Folder containing static assets:

style.css: Stylesheet for the website's appearance.

scripts (min_date.js, local_storage.js and welcome_admin.js): Custom JavaScript code for interactivity.

# Additional Notes:

This is a basic website and can be extended with additional features like event categories, reminders, or invitations.

The code currently stores events in a plain text file (events.txt). You can consider using a database for real-world applications.

The provided JavaScript files might be optional and can be used for basic functionalities like date validation or UI enhancements.

# Getting Started:

Visit http://127.0.0.1:5000/ in your web browser.

Login using the default credentials (if you haven't modified them).

Explore the functionalities to create, edit, and manage your events.

# I hope you find this event organizer website helpful!

