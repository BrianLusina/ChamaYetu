from flask import Blueprint
from flask import  request, redirect, url_for, session, g, flash, \
    render_template,app
from flask_oauth import OAuth

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import mod_auth

mod_auth = Blueprint('twitter', __name__, url_prefix='/auth')


oauth = OAuth()

twitter = oauth.remote_app('twitter',

                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url = 'https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key = 'B0NAmdtcSvF5vDWMApymhS5Xz',
                           consumer_secret='DjgNIyVoJ4BuSi5df7UbAGpq1kG5wjVFrLQL2Sts5CleH3vNij')




@twitter.tokengetter
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('auth/login'))

    access_token = access_token[0]

    return  render_template('idex.html')

@mod_auth.route('/login')
def login():
    return  twitter.authorized_handler(callback= url_for('twitter.oauth_authorized'
                                                         # next = request.args.get('next') or request.referrer or None
                                                         ))

@mod_auth.route('/oath-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')

    if resp is None:
        flash('request denied!!')
        return  redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']

    )

    return  redirect(url_for('index'))