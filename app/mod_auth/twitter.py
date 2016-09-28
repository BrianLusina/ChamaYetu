from app.mod_auth import oauth
from flask import redirect, session, request
from  flask_oauth import OAuth




# class TwitterSignin(oauth.OAuthSignIn):
#     def __init__(self):
#         super(TwitterSignin, self).__init__('twitter')
#         self.service = OAuth1Service(
#             name='twitter',
#             consumer_key=self.consumer_id,
#             consumer_secret=self.consumer_secret,
#             request_token_url='https://api.twitter.com/oauth/request_token',
#             authorize_url='https://api.twitter.com/oauth/authorize',
#             access_token_url='https://api.twitter.com/oauth/access_token',
#             base_url='https://api.twitter.com/1.1/'
#         )

