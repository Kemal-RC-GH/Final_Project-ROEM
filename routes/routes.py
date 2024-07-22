from .handlers import (
    index,
    login,
    register,
    logout,
    dashboard,
    create_event,
    edit_event,
    delete_event
)

def register_routes(app):
    app.add_url_rule("/", view_func=index, methods=["GET"])
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=register, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout, methods=["GET"])
    app.add_url_rule("/dashboard", view_func=dashboard, methods=["GET"])
    app.add_url_rule("/create_event", view_func=create_event, methods=["GET", "POST"])
    app.add_url_rule("/edit_event/<string:event_id>", view_func=edit_event, methods=["GET", "POST"])
    app.add_url_rule("/delete_event/<string:event_id>", view_func=delete_event, methods=["GET", "POST"])
