from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import flask_sqlalchemy
from flask_login import LoginManager, login_user, logout_user,\
    current_user
from controllers import OAuthSignIn
from app.mod_auth.forms import LoginForm
from app.models import User, Data_Base, engine

app = Flask(_name__)
app.config['SECRET_KEY'] = 'unjdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['OAUTH_CREDENTIALS'] = {
	
	'twitter':{
	'id':' B0NAmdtcSvF5vDWMApymhS5Xz'
	'secret': 'DjgNIyVoJ4BuSi5df7UbAGpq1kG5wjVFrLQL2Sts5CleH3vNij'

	}

}

lm = LoginManager(app)

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


#login manager check if user is logged in
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

