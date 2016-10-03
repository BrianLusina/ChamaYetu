import sqlalchemy
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for
from  sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from app.mod_auth.forms import LoginForm, TreasurerForm, RegistrationForm
from app.models import User, Data_Base, engine
from app.mod_dashboard import controller

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
    Create an object of the LoginForm that takes form fields as a parameter
    validate the form on submission, check if the user is true(exists) and if the passwords match
    if true assign the user a session and store their id in a session dictionary
    redirect them to their dashboard
    else, flash a message informing them of wrong credentials
    :return: render the login template
    """
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()

        if user and check_password_hash(pwhash=user.password, password=form.password.data):
            session['user_id'] = user.id

            # welcome the user because they are awesome
            flash(message="Welcome %s" % user.name)
            return redirect_dash(user.id)
        flash(message="Wrong email or password", category='error-message')
    return render_template("auth/login.html", form=form)


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
        return redirect('templates/home_page/index')
    return render_template("auth/register.html", form=form)

