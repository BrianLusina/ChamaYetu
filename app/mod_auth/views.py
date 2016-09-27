from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import flask_sqlalchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from controllers import OAuthSignIn

app = Flask(_name__)
app.config['SECRET_KEY'] = 'unjdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
	
	'twitter':{
	'id':' B0NAmdtcSvF5vDWMApymhS5Xz'
	'secret': 'DjgNIyVoJ4BuSi5df7UbAGpq1kG5wjVFrLQL2Sts5CleH3vNij'
	
	}
}