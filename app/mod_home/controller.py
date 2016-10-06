from flask import Blueprint, request, render_template,\
    g, flash, session, redirect, url_for, current_app

from firebase import firebase
import hashlib
import uuid
from app.mod_dashboard import controller

# Define the blueprint: 'auth', set its url prefix: app.url/
mod_home = Blueprint('home', __name__, url_prefix='/')


@mod_home.route('/', methods=["POST", "GET"])
@mod_home.route('index/', methods=["POST", "GET"])
def index():
    """
    Creates a connection to the firebase database to add a user
    get password and username from the sign up form
    hash the password for security reasons
    :return: redirect to dashboard
    """
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

        # redirect to dashboard
        return redirect(url_for('dashboard.dashboard'))

    return render_template("home_page/index.html")


# contact us page
@mod_home.route('contact')
def contact():
    return render_template("home_page/contact.html")


# about us page
@mod_home.route('about')
def about():
    return render_template("home_page/about.html")
