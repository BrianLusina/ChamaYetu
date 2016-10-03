from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from app.mod_auth.forms import LoginForm
from app.models import User, Data_Base, engine
from app.mod_dashboard import controller

# imports
import logging
from flask import Blueprint, url_for, request, current_app, session
from flask_login import login_user, current_user
from flask_security.utils import do_flash
from flask_babel import gettext as _
from flask_oauth import OAuthException

from werkzeug.exceptions import abort
from werkzeug.local import LocalProxy
from werkzeug.utils import redirect



# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

logger = logging.getLogger("flask_social_blueprint")

# set the routes and accepted methods
@mod_auth.route('/login/', methods=["POST", "GET"])
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






# social





class SocialBlueprint(Blueprint):
    def __init__(self, name, import_name, connection_adapter=None, providers=None, login_redirect_url='/', *args, **kwargs):
        super(SocialBlueprint, self).__init__(name, import_name, *args, **kwargs)
        self.connection_adapter = connection_adapter
        self.providers = providers or {}

	self.login_redirect_url = login_redirect_url

    def get_provider(self, provider_name):
        provider = self.providers[provider_name]
        if not provider:
            abort(404)
        return provider

    def authenticate(self, provider):
        """
        Starts OAuth authorization flow, will redirect to 3rd party site.
        """
        callback_url = url_for(".callback", provider=provider, _external=True)
        provider = self.get_provider(provider)
        session['next'] = request.args.get('next') or ''
        return provider.authorize(callback_url)

    def callback(self, provider):
        """
        Handles 3rd party callback and processes it's data
        """
        provider = self.get_provider(provider)
        try:
            return provider.authorized_handler(self.login)(provider=provider)
        except OAuthException as ex:
            logging.error("Data: %s", ex.data)
            raise

    def login(self, raw_data, provider):

        logger.debug("raw_data: %s" % raw_data)
        if not raw_data:
            do_flash(_("OAuth authorization failed"), "danger")
            abort(400)
        profile = provider.get_profile(raw_data)
        connection = self.connection_adapter.by_profile(profile)
        if not connection:
            return self.no_connection(profile, provider)
        return self.login_connection(connection, profile, provider)

    def no_connection(self, profile, provider):
        try:
            connection = self.create_connection(profile, provider)
        except Exception as ex:
            logging.warn(ex, exc_info=True)
            do_flash(_("Could not register: {}").format(getattr(ex, "message", ex)), "warning")
            return self.login_failed_redirect(profile, provider)

        return self.login_connection(connection, profile, provider)

    def login_connection(self, connection, profile, provider):
        user = connection.get_user()
        assert user, "Connection did not returned a User instance"
        login_user(user)
        return self.login_redirect(profile, provider)

    def login_redirect(self, profile, provider):
        next_ = session.pop('next', '')
        return redirect(next_ or self.login_redirect_url)

    def login_failed_redirect(self, profile, provider):
        return redirect("/")

    def create_connection(self, profile, provider):
        return self.connection_adapter.from_profile(current_user, profile)

    @classmethod
    def create_bp(cls, name, connection_adapter, providers, login_redirect_url, *args, **kwargs):
        bp = cls(name, __name__, connection_adapter, providers, login_redirect_url, *args, **kwargs)
        bp.route('/login/<provider>', endpoint="login")(bp.authenticate)
        bp.route('/callback/<provider>', endpoint="callback")(bp.callback)
        return bp

    @classmethod
    def setup_providers(cls, config):
        providers = {}
        for provider, provider_config in config.items():
            module_path, class_name = provider.rsplit('.', 1)
            from importlib import import_module
            module = import_module(module_path)
            provider = getattr(module, class_name)(**provider_config)
            providers[provider.name] = provider
        return providers

    @classmethod
    def init_bp(cls, app, connection_adapter, *args, **kwargs):
        config = app.config.get("SOCIAL_BLUEPRINT")
        providers = cls.setup_providers(config)
	login_redirect_url = app.config.get("SECURITY_POST_LOGIN_VIEW")
        if login_redirect_url is None:
            login_redirect_url = '/'
        bp = cls.create_bp('social', connection_adapter, providers, login_redirect_url, *args, **kwargs)
        app.register_blueprint(bp)


bp = LocalProxy(lambda: current_app.blueprints[request.blueprint])


# TODO: redirect to mod_dashboard's controller pass in user name as a url
def redirect_dash(user_id):
    return controller.mod_dashboard.route('auth/dashboard')