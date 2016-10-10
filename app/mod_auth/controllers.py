# <<<<<<< HEAD
import sqlalchemy
# =======
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, \
    current_app
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from app.models import User, Data_Base, engine
from firebase import firebase
import hashlib
import uuid
import re
# >>>>>>> 4f7d50700a62ff3b23bb68480d66863f85e5bc03
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for
from  sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
# <<<<<<< HEAD
from app.mod_auth.forms import LoginForm, TreasurerForm, RegistrationForm
from app.models import User, Data_Base, engine
from app.mod_dashboard import controller
# =======
from app.mod_auth.forms import LoginForm
# >>>>>>> 4f7d50700a62ff3b23bb68480d66863f85e5bc03

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
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
    firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)
    firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

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

        # todo: assign the user an auth token and pass to a session
        authentication = firebase.FirebaseAuthentication(secret=firebase_secret, email=email)
        firebase.authentication = authentication
        print(authentication.extra)
        # {'admin': False, 'debug': False, 'email': email, 'id': idx, 'provider': 'password'}
        user = authentication.get_user()

        # get firebase auth token for the current user and assign to a session to manage user login
        print user.firebase_auth_token
        # Database Directive
        firebase_conn.put(url=firebase_users_node, name=username, data={
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

