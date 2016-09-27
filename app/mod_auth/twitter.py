from mod_auth import oauth

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
#authorize method for twitter 
    def authorize(self):
        request_token = self.service.get_request_token(
            params = {'oauth_callback':self.get_callback_url()})

        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

#callback method

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None,None,None

        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data = {'oauth_verifier': request_args['oauth_verifier']}

            )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None 