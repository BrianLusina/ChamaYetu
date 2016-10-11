from flask import Blueprint, request, g, flash, session, redirect, url_for, \
    current_app
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine
import hashlib
import uuid
import re
from sqlalchemy.orm import sessionmaker
from firebase_token_generator import create_token
from firebase import firebase
from requests import HTTPError

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


class Auth(object):
    """
    Class that handles the authentication variables with Firebase
    :firebase_auth gets the configuration dictionary that will be used for authenticating the user
    """
    @staticmethod
    def firebase_auth():
        return current_app.config.get('FIREBASE_CONFIG').auth()


def signup_handler(email, password, full_name):
    """
    :param email: email the user enters in the form
    :param password: password entered by the user
    :param full_name: full name of the user
    :return: :rtype boolean depending on success of the user signing up
    """

    auth = Auth.firebase_auth()

    username = re.split('@', email)[0]

    # Generates Random UID for Database
    idx = uuid.uuid4()
    uid = str(idx)

    # Hash that Password
    sha1 = hashlib.sha1()
    sha1.update(password)
    password = sha1.hexdigest()

    # create a user with email and password, check if the user email already exists
    try:
        auth.create_user_with_email_and_password(email, password)
        database_directive(uid, username, full_name, email, password)
        return True
    except HTTPError:
        # if the email already exists, return false to display an error in the view
        return False


def login_handler(login_email, password):
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)

    firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
    firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

    # get the full name from the form and split to get the username
    email = request.form['login_email']
    password = request.form['login_password']
    username = re.split('@', email)[0].lower()

    # get connection to user's node and query specific user
    user = firebase_conn.get(firebase_users_node, username)
    if check_user(user):
        return redirect(url_for(endpoint='dashboard.dashboard', username=username))

    # todo: assign the user an auth token and pass to a session
    authentication = firebase.FirebaseAuthentication(secret=firebase_secret, email=email)
    firebase.authentication = authentication
    print(authentication.extra)
    # {'admin': False, 'debug': False, 'email': email, 'id': idx, 'provider': 'password'}
    user = authentication.get_user()

    # redirect to dashboard, pass the username to the dashboard
    return redirect(url_for(endpoint='dashboard.dashboard', username=email))


def register_chama():
    """
    Method to manage subse
    :return:
    """
    pass


def check_user(user):
    """
    Helper function that validates a user on login
    :param user the user to validate
    :return:
    """
    if user:
        return True


def database_directive(uid, username, full_name, email, password):
    """
    Adds the user to the database with the following params
    :param uid: the user id which is auto generated
    :param username: the username generated from the user email
    :param full_name: full name of the user
    :param email: email the user will authenticate with
    :param password: password the user will use to sign up and login
    :return: no return type here
    """

    first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN'),
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None),

    # Database Directive
    firebase_conn.post(url='/users', name=username, data={
        'uid': uid,
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'userName': username,
        'userPassword': password
    }, headers={'print': 'pretty'})
