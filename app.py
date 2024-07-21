from flask import Flask
import routes  # Import the routes from routes.py

app = routes.app  # Use the app instance from routes.py

if __name__ == "__main__":
    app.run(debug=True)
