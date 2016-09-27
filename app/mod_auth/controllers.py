from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for,current_app
from rauth import OAuth1Service
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from app.mod_auth.forms import LoginForm
from app.models import User, Data_Base, engine
from app.mod_dashboard import controller


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




#twitter authentication

#base clss for authentication
class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials= current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']


    def authorize(self):
        pass

    def callback(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback',provider = self.provider_name, _external= True)


    @classmethod

    #gets available authentication providers and adds them toa a dict
    def get_provider(self, provider_name):
        if self.provider is None:
            self.providers = {}

            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class TwitterSignin(OAuthSignIn):
    def __init__(self):
        super(TwitterSignin, self).__init__('twitter')
        self.service = OAyth1Service(
        name = 'twitter'
        consumer_key = self.consumer_id,
        consumer_secret = self.consumer_secret,
        request_token_url='https://api.twitter.com/oauth/request_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        access_token_url='https://api.twitter.com/oauth/access_token',
        base_url='https://api.twitter.com/1.1/'
            )

