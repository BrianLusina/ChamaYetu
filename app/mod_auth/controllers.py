<<<<<<< HEAD
import sqlalchemy
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, \
    current_app
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
=======
from flask import request, g, session, current_app
>>>>>>> 986b9db887e8b98b9af5382d93577025f1103386
from app.models import User, Data_Base, engine
import hashlib
import uuid
import re
<<<<<<< HEAD
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for
from  sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from app.mod_auth.forms import LoginForm, TreasurerForm, RegistrationForm
from app.models import User, Data_Base, engine
from app.mod_dashboard import controller
from app.mod_auth.forms import LoginForm
=======
from sqlalchemy.orm import sessionmaker
from firebase_token_generator import create_token
from firebase import firebase
from requests import HTTPError
>>>>>>> 986b9db887e8b98b9af5382d93577025f1103386

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
db_session = DBSession()


class Auth(object):
    """
    Class that handles the authentication variables with Firebase
    firebase_auth gets the configuration dictionary that will be used for authenticating the user
    firebase_db_url contains the database url to Firebase
    firebase_conn connects to the database
    firebase_database connects to the database url, enabling access to the database nodes
    """

    def __init__(self, email, password):
        """
        :param email: email the user enters in the form
        :param password: password entered by the user
        """
        self.email = email
        self.password = password

    @staticmethod
    def firebase_auth():
        return current_app.config.get('FIREBASE_CONFIG').auth()

    @staticmethod
    def firebase_db_url():
        return current_app.config.get('FIREBASE_DB_CONN')

    @staticmethod
    def firebase_conn():
        return firebase.FirebaseApplication(Auth.firebase_db_url(), None)

    @staticmethod
    def firebase_database():
        return Auth.firebase_auth().database()

    def firebase_nodes(self):
        return {
            "firebase_users_node": current_app.config.get('FIREBASE_USERS_NODE'),
            "firebase_web_key": current_app.config.get("FIREBASE_WEB_KEY")
        }

    def signup_handler(self, full_name, username):
        """
        Handles user sign up. The Try...catch block creates a new user with email and password
        Checks if the user already exists in the database and returns true if they do not.
        The user is then created in the database and their credentials are passed to the database
        :param username: auto-generated username
        :param full_name: full name of the user
        :return: :rtype boolean depending on success of the user signing up
        """

        auth = Auth.firebase_auth()

        # Generates Random UID for Database
        idx = uuid.uuid4()
        uid = str(idx)

        # Hash that Password
        sha1 = hashlib.sha1()
        sha1.update(self.password)
        password = sha1.hexdigest()

        # create a user with email and password, check if the user email already exists
        try:
            user = auth.create_user_with_email_and_password(self.email, password)
            auth.send_email_verification(user['idToken'])

            self.database_directive(uid, username, full_name)
            return True
        except HTTPError:
            # if the email already exists, return false to display an error in the view
            return False

    def login_handler(self, username):
        """
        :return: Whether the user exists in the auth configurations or whether they are new users
        :rtype Bool
        """

        firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
        firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

        auth = Auth.firebase_auth()
        try:
            auth.sign_in_with_email_and_password(self.email, self.password)

            # get connection to user's node and query specific user
            user = Auth.firebase_conn().get(firebase_users_node, username)

            # todo: assign the user an auth token and pass to a session
            authentication = firebase.FirebaseAuthentication(secret=firebase_secret, email=self.email)
            firebase.authentication = authentication
            print(authentication.extra)
            # {'admin': False, 'debug': False, 'email': email, 'id': idx, 'provider': 'password'}
            user = authentication.get_user()
            return True
        except HTTPError:
            return False

    def database_directive(self, uid, username, full_name):
        """
        Adds the user to the database with the following params
        :param uid: the user id which is auto generated
        :param username: the username generated from the user email
        :param full_name: full name of the user
        :return: no return type here
        """

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

        Auth.firebase_conn().put(url='/users', name=username, data={
            'uid': uid,
            'firstName': first_name,
            'lastName': last_name,
            'email': self.email,
            'userName': username,
            'userPassword': self.password
        }, headers={'print': 'pretty'})
<<<<<<< HEAD

        # redirect to dashboard, pass the username to the dashboard
        return redirect(url_for(endpoint='dashboard.dashboard', username=username))


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
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)

    firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
    firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

# <<<<<<< HEAD
# TODO: redirect to mod_dashboard's controller pass in user name as a url
def redirect_dash(user_id):
    return controller.mod_dashboard.route('/dashboard')


@mod_auth.route('/treasurer/', methods=["POST", "GET"])
def treasurer():
    form = TreasurerForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(Name=form.membersname.data).first()
        user = db_session.query(User).filter_by(Name=form.amountcontributed.data).first()
        user = db_session.query(User).filter_by(Name=form.amountwithdrawn.data).first()
        user = db_session.query(User).filter_by(Name=form.date.data).first()
        return redirect(url_for('home_page/treasurer.html'))

    return render_template('home_page/treasurer.html', form=form)


@mod_auth.route('/register/', methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()

        flash(message="Welcome %s" % user.name)
        return redirect('home_page/index')
    return render_template('auth/register.html',
                           form=form)

    if request.method == 'POST':
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

