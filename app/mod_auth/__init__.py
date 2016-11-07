from flask import current_app
from firebase import firebase
from abc import ABCMeta, abstractmethod


class FirebaseAuth(object):
    """
    Class to handle connection to Firebase configuration variables
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
        self.firebase_chama_node = current_app.config.get('FIREBASE_CHAMA_NODE')
        self.firebase_auth = current_app.config.get('FIREBASE_CONFIG').auth()
        self.firebase_db_url = current_app.config.get('FIREBASE_DB_CONN')
        self.firebase_app = firebase.FirebaseApplication(self.firebase_db_url, None)
        self.firebase_database = current_app.config.get('FIREBASE_CONFIG').database()
        self.firebase_web_key = current_app.config.get("FIREBASE_WEB_KEY")
        self.firebase_secret = current_app.config.get("FIREBASE_WEB_KEY")

    @abstractmethod
    def register_user(self, full_name):
        """
        Handles user sign up. The Try...catch block creates a new user with email and password
        Checks if the user already exists in the database and returns true if they do not.
        The user is then created in the database and their credentials are passed to the database
        :param full_name: full name of the user
        :return: :rtype boolean depending on success of the user signing up
        """
        pass

    @abstractmethod
    def register_chama(self, chama_name, chama_members, bank_name, bank_account):
        """
        Registers a new chama to the database at the Chama Node
        :param chama_name: name of the chama to be registered
        :param chama_members: number of members to be registered with the chama
        :param bank_name: the bank name of the registering chama
        :param bank_account: the bank account of the chama
        :return: :rtype bool, whether the write operation is completed
        """
        pass

    @abstractmethod
    def login_user(self):
        """
        :return: Whether the user exists in the auth configurations or whether they are new users
        :rtype Bool
        """
        pass

    @abstractmethod
    def reset_password(self, email):
        """
        Reset user password on request
        :param email: User email to reset password
        :return:
        """
        pass

    @abstractmethod
    def database_directive(self, username, full_name):
        """
        Adds the user to the database with the following params
        :param username: the username generated from the user email
        :param full_name: full name of the user
        :return: no return type here
        """
        pass
