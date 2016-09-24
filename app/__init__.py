# import flask and template errors
from flask import Flask, render_template


# import a module or component using its Blueprint handler variable
from app.mod_auth.controllers import mod_auth as auth_module

# Define the WSGI application object
app = Flask(__name__)

# configurations
app.config.from_object('config')

# define the database object which is imported by modules and controllers
#db = SQLAlchemy(app)


# Error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Register blueprint(s) ALL blueprints will be registered here
app.register_blueprint(auth_module)

# Build the database
# This will create the database file using SQLAlchemy
# db.create_all()
