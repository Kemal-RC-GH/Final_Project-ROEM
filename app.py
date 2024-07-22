from flask import Flask

app = Flask(__name__)
app.secret_key = "1234@$"

from routes import register_routes  # Import the function to register routes

register_routes(app)  # Register routes with the Flask app

if __name__ == "__main__":
    app.run(debug=True)
