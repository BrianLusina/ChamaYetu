from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, \
    current_app
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from app.models import User, Data_Base, engine
from firebase import firebase
import hashlib
import uuid


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
    :return: redirect to dashboard
    """
    # form = LoginForm(request.form)
    #
    # if form.validate_on_submit():
    #     user = db_session.query(User).filter_by(email=form.email.data).first()
    #
    #     if user and check_password_hash(pwhash=user.password, password=form.password.data):
    #         session['user_id'] = user.id
    #
    #         # welcome the user because they are awesome
    #         flash(message="Welcome %s" % user.name)
    #     flash(message="Wrong email or password", category='error-message')
    # return render_template("auth/login.html", form=form)

    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)

    if request.method == 'POST':
        password = request.form['signup_password']
        email = request.form['signup-email']
        username = request.form['signup_full_name']
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
            'usern': username,
            'userp': password
        }, headers={'print': 'pretty'})

        # redirect to dashboard, pass the username to the dashboard
        return redirect(url_for(endpoint='dashboard.dashboard', username=username))


@mod_auth.route('/login', methods=["POST", "GET"])
def login():
    pass
