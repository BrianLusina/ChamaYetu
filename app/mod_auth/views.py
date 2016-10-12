from flask import Blueprint, request, render_template, flash, redirect, url_for
from .controllers import login_handler, Auth
import re

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# set the routes and accepted methods
@mod_auth.route('/signin/', methods=["POST", "GET"])
def sign_in():
    """
    Creates a connection to the firebase database to add a user
    get password and username from the sign up form
    hash the password for security reasons
    Get the form data and store in variables for processing.
    check if the username/email already exists, if so, alert the user
    :return: redirect to dashboard
    """

    if request.method == 'POST':
        # get the full name from the form and split to get the username
        full_name = request.form['signup_full_name']
        email = request.form['signup-email']
        password = request.form['signup_password']
        username = re.split('@', email)[0]

        # initialize the Auth class with the email and password
        auth = Auth(email=email, password=password)

        if auth.signup_handler(full_name=full_name, username=username):
            # redirect to dashboard, pass the username to the dashboard
            return redirect(url_for(endpoint='dashboard.dashboard', username=username, scheme='https'))
        else:
            # Display error
            flash("This email already exists")

    return render_template('home/index.html')


@mod_auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Creates a connection to the firebase database to add a user
    get password and username from the sign up form
    hash the password for security reasons
    Get the form data and store in variables for processing.
    check if the username/email already exists, if so, alert the user
    :return: redirect to dashboard
    """
    if request.method == 'POST':
        # get the full name from the form and split to get the username
        email = request.form['login_email']
        password = request.form['login_password']
        username = re.split('@', email)[0]

        if login_handler(login_email=email, password=password):
            return redirect(url_for(endpoint='dashboard.dashboard', username=username))

        # redirect to dashboard, pass the username to the dashboard
        return redirect(url_for(endpoint='dashboard.dashboard', username=email))
