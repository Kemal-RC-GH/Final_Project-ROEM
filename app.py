from flask import Flask, render_template, request, session, redirect, flash, get_flashed_messages, json
from datetime import datetime

app = Flask(__name__)          # All required classes and functions imported. Flask file defined
app.secret_key = '1234@$'

if __name__ == '__main__':
    app.run(debug=True)
