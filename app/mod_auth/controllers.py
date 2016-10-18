from flask import request, g, session, current_app
from app.models import User, Data_Base, engine
import hashlib
import uuid
import re
from sqlalchemy.orm import sessionmaker
from firebase_token_generator import create_token
from firebase import firebase
from requests import HTTPError

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


class Auth(object):
    """
    Class that handles the authentication variables with Firebase
    firebase_auth gets the configuration dictionary that will be used for authenticating the user
    firebase_db_url contains the database url to Firebase
    firebase_conn connects to the database
    firebase_database connects to the database url, enabling access to the database nodes
    """

    def __init__(self, email,password):
        """
        :param email: email the user enters in the form
        :param password: password entered by the user
        """
        self.email = email
        self.password = password

    @staticmethod
    def firebase_auth():
        return current_app.config.get('FIREBASE_CONFIG').auth()

    @staticmethod
    def firebase_db_url():
        return current_app.config.get('FIREBASE_DB_CONN')

    @staticmethod
    def firebase_conn():
        return firebase.FirebaseApplication(Auth.firebase_db_url(), None)

    @staticmethod
    def firebase_database():
        return Auth.firebase_auth().database()

    def firebase_nodes(self):
        return {
            "firebase_users_node": current_app.config.get('FIREBASE_USERS_NODE'),
            "firebase_web_key": current_app.config.get("FIREBASE_WEB_KEY")
        }

    def register_user_handler(self, full_name, username):
        """
        Handles user sign up. The Try...catch block creates a new user with email and password
        Checks if the user already exists in the database and returns true if they do not.
        The user is then created in the database and their credentials are passed to the database
        :param username: auto-generated username
        :param full_name: full name of the user
        :return: :rtype boolean depending on success of the user signing up
        """

        auth = Auth.firebase_auth()

        # Generates Random UID for Database
        idx = uuid.uuid4()
        uid = str(idx)

        # Hash that Password
        sha1 = hashlib.sha1()
        sha1.update(self.password)
        password = sha1.hexdigest()

        # create a user with email and password, check if the user email already exists
        try:
            user = auth.create_user_with_email_and_password(self.email, password)
            auth.send_email_verification(user['idToken'])

            self.database_directive(uid, username, full_name)
            return True
        except HTTPError:
            # if the email already exists, return false to display an error in the view
            return False

    @staticmethod
    def register_chama_handler(chama_name, chama_members, bank_name, bank_account):
        """
        :param chama_name: name of the chama to be registered
        :param chama_members: number of members to be registered with the chama
        :param bank_name: the bank name of the registering chama
        :param bank_account: the bank account of the chama
        :return: :rtype bool, whether the write operation is completed
        """

        pass

    def login_handler(self, username):
        """
        :return: Whether the user exists in the auth configurations or whether they are new users
        :rtype Bool
        """

        firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
        firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

        auth = Auth.firebase_auth()
        try:
            auth.sign_in_with_email_and_password(self.email, self.password)

            # get connection to user's node and query specific user
            user = Auth.firebase_conn().get(firebase_users_node, username)

            # todo: assign the user an auth token and pass to a session
            authentication = firebase.FirebaseAuthentication(secret=firebase_secret, email=self.email)
            firebase.authentication = authentication
            print(authentication.extra)
            # {'admin': False, 'debug': False, 'email': email, 'id': idx, 'provider': 'password'}
            user = authentication.get_user()
            return True
        except HTTPError:
            return False

    def database_directive(self, uid, username, full_name):
        """
        Adds the user to the database with the following params
        :param uid: the user id which is auto generated
        :param username: the username generated from the user email
        :param full_name: full name of the user
        :return: no return type here
        """

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

        Auth.firebase_conn().put(url='/users', name=username, data={
            'uid': uid,
            'firstName': first_name,
            'lastName': last_name,
            'email': self.email,
            'userName': username,
            'phoneNumber': self.phone_no,
            'userPassword': self.password
        }, headers={'print': 'pretty'})
