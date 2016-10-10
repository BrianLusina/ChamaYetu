from flask import Flask, render_template, request, redirect

# import a module or component using its Blueprint handler variable
from app.mod_auth.views import mod_auth as auth_module
from app.mod_dashboard.controller import mod_dashboard as dashboard_module
from app.mod_home.controller import mod_home as home_module

# Define the WSGI application object
app = Flask(__name__)

# configurations
app.config.from_object('config')


# Error handler for page not found
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@app.errorhandler(403)
def error_500(error):
    return render_template("500.html"), 500


# Register blueprint(s) ALL blueprints will be registered here
app.register_blueprint(home_module)
app.register_blueprint(auth_module)
app.register_blueprint(dashboard_module)
