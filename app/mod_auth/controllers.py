from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, \
    current_app
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from app.models import User, Data_Base, engine
from firebase import firebase
import hashlib
import uuid
import re


# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

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
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)

    if request.method == 'POST':
        # get the full name from the form and split to get the username
        full_name = request.form['signup_full_name']
        email = request.form['signup-email']
        username = re.split('@', email)[0]

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]
        password = request.form['signup_password']

        # Generates Random UID for Database
        idx = uuid.uuid4()
        uid = str(idx)
        # Hash that Passsword
        sha1 = hashlib.sha1()
        sha1.update(password)
        password = sha1.hexdigest()

        # Database Directive
        firebase_conn.put(url='/users', name=username, data={
            'uid': uid,
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'userName': username,
            'userPassword': password
        }, headers={'print': 'pretty'})

        # redirect to dashboard, pass the username to the dashboard
        return redirect(url_for(endpoint='dashboard.dashboard', username=username))


@mod_auth.route('/login', methods=["POST", "GET"])
def login():
    pass
