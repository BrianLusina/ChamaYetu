from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import flask_sqlalchemy
from flask_login import LoginManager, login_user, logout_user,\
    current_user
from controllers import OAuthSignIn
from app.mod_auth.forms import LoginForm
from app.models import User, Data_Base, engine
from mod_auth import controllers
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


#route for authentication

@app.route('/authorize/<provider>')
#route ensures user not loggedin the OAuthSignIn subclass for provider and then invokes authorize()

def oauth_authorize(provider):
	if not current_user.is_anonymous():
		return redirect(url_for('index'))

	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()



#callback route

@app oauth_callback(provider):
	if not user.is_anonymous:
		return redirect(url_for('index'))
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email = oauth.callback()

	if social_id is  None:
		flash('Authentication failed')
		return redirect(url_for('index'))

	user = User.query.filter_by(social_id=social_id).first
	if not user:
		user = User(social_id=social_id,nickname = username,email=email)
		db.session.add(user)
		db.session.commit()

	login_user(user, True)
	return redirect(url_for('index'))





if _name__ == '__main__':
	db.create_all()
	app.run(debug=True)