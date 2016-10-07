# from flask import Flask,Blueprint, app, request, redirect, url_for, session, flash, g, render_template
# from flask_rauth import RauthOAuth1
#
# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from  app.models import User
#
#
#
# # Define the blueprint: 'auth', set its url prefix: app.url/auth
# mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
#
#
#
# TWITTER_CONSUMER_KEY='B0NAmdtcSvF5vDWMApymhS5Xz',
# TWITTER_CONSUMER_SECRET='DjgNIyVoJ4BuSi5df7UbAGpq1kG5wjVFrLQL2Sts5CleH3vNij',
# SECRET_KEY='just a secret key, to confound the bad guys',
# DEBUG = True
#
#
#
# # twitter end points
# twitter = RauthOAuth1(
#
#     name='twitter',
#     base_url='https://api.twitter.com/1/',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     authorize_url='https://api.twitter.com/oauth/authorize',
#     access_token_url='https://api.twitter.com/oauth/access_token'
# )
#
#
# twitter.init_app(app)
#
# # sqlalchemy setup
#
# engine = create_engine('sqlite:////app.db')
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     Base.metadata.create_all(bind=engine)
#
#
# @mod_auth.before_request
# def before_request():
#     g.user = None
#     if 'user_id' in session:
#         g.user = User.query.get(session['user_id'])
#
#
# @mod_auth.after_request
# def after_request(response):
#     db_session.remove()
#     return response
#
#
# @twitter.tokengetter
# def get_twitter_token():
#     '''
#     This is used by the API to look for the auth token and secret that are used
#     for Twitter API calls. If you don't want to store this in the database,
#     consider putting it into the session instead.
#     Since the Twitter API is OAuth 1.0a, the `tokengetter` must return a
#     2-tuple: (oauth_token, oauth_secret).
#     '''
#     user = g.user
#     if user is not None:
#         return user.oauth_token, user.oauth_secret
#
# @mod_auth.route('/login')
# def login():
#     '''
#     Calling into `authorize` will cause the OAuth 1.0a machinery to kick
#     in. If all has worked out as expected or if the user denied access to
#     his/her information, the remote application will redirect back to the callback URL
#     provided.
#     Int our case, the 'authorized/' route handles the interaction after the redirect.
#     '''
#     return twitter.authorize(callback=url_for('authorized',
#         _external=True,
#         next=request.args.get('next') or request.referrer or None))
#
#
# @mod_auth.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You were signed out')
#     return redirect(request.referrer or url_for('home/index'))
#
#
# @mod_auth.route('/authorized')
# @twitter.authorized_handler()
# def authorized(resp, oauth_token):
#     '''
#     Called after authorization. After this function finished handling,
#     the tokengetter from above is used to retrieve the 2-tuple containing the
#     oauth_token and oauth_token_secret.
#     Because reauthorization often changes any previous
#     oauth_token/oauth_token_secret values, then we must update them in the
#     database.
#     If the application redirected back after denying, the `resp` passed
#     to the function will be `None`. Unfortunately, OAuth 1.0a (the version
#     that Twitter, LinkedIn, etc use) does not specify exactly what should
#     happen when the user denies access. In the case of Twitter, a query
#     parameter `denied=(some hash)` is appended to the redirect URL.
#     '''
#     next_url = request.args.get('next') or url_for('home/index')
#
#     # check for the Twitter-specific "access_denied" indicator
#     if resp is None and 'denied' in request.args:
#         flash(u'You denied the request to sign in.')
#         return redirect(next_url)
#
#     # pull out the nicely parsed response content.
#     content = resp.content
#
#     user = User.query.filter_by(name=content['screen_name']).first()
#
#     # this if the first time signing in for this user
#     if user is None:
#         user = User(content['screen_name'])
#         db_session.add(user)
#
#     # we now update the oauth_token and oauth_token_secret
#     # this involves destructuring the 2-tuple that is passed back from the
#     #   Twitter API, so it can be easily stored in the SQL database
#     user.oauth_token = oauth_token[0]
#     user.oauth_secret = oauth_token[1]
#     db_session.commit()
#
#     session['user_id'] = user.id
#     flash('You were signed in')
#     return redirect(next_url)
#
