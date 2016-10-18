from flask import Blueprint, request, render_template, flash, redirect, url_for
from .controllers import Auth
import re

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# set the routes and accepted methods
@mod_auth.route('/register/', methods=["POST", "GET"])
def register_user():
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
        phone_no = request.form['signup-phone']
        username = re.split('@', email)[0]

        # initialize the Auth class with the email and password
        auth = Auth(email=email, phone_no=phone_no, password=password)

        if auth.register_user_handler(full_name=full_name, username=username):
            # proceed to register chama, pass the user name for the user dashboard
            return redirect(url_for(endpoint='auth.register_chama', username=username, scheme='https'))
        else:
            # Display error
            flash("This email already exists")
            return render_template('home/index.html')

    return render_template('home/index.html')


@mod_auth.route('/register-chama/<username>', methods=['POST', "GET"])
def register_chama():
    if request.method == "POST":
        chama_name = request.form['chama_name']
        chama_members = request.form['chama-members']
        chama_bank = request.form['bank-name']
        chama_bank_ac = request.form['bank-account-no']

        # pass the form data to the register chama handler in controller
        Auth.register_chama_handler(chama_name=chama_name, chama_members=chama_members, bank_name=chama_bank,
                                    bank_account=chama_bank_ac)

        # redirect to dashboard, pass the username to the dashboard
        return redirect(url_for(endpoint='dashboard.dashboard', username="username", scheme='https'))

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

        auth = Auth(email=email, password=password)

        if auth.login_handler(username=username):
            return redirect(url_for(endpoint='dashboard.dashboard', username=username))
        else:
            flash("Wrong Password or email")

    return render_template('home/index.html')
