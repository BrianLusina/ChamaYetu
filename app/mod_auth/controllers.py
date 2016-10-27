from app.models import Data_Base, engine
import hashlib
from sqlalchemy.orm import sessionmaker
from requests import HTTPError
from app.mod_auth import FirebaseAuth

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

    def __init__(self, email, password, phone_no=None):
        """
        :param email: email the user enters in the form
        :param password: password entered by the user
        """
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.auth = FirebaseAuth.fire_nodes()["fire_auth"]
        self.conn = FirebaseAuth.fire_conn()

    def register_user_handler(self, full_name, username):
        """
        Handles user sign up. The Try...catch block creates a new user with email and password
        Checks if the user already exists in the database and returns true if they do not.
        The user is then created in the database and their credentials are passed to the database
        :param username: auto-generated username
        :param full_name: full name of the user
        :return: :rtype boolean depending on success of the user signing up
        """

        # Hash that Password
        sha1 = hashlib.sha1()
        sha1.update(self.password)
        password = sha1.hexdigest()

        # create a user with email and password, check if the user email already exists
        try:
            user = self.auth.create_user_with_email_and_password(self.email, password)
            self.auth.send_email_verification(user['idToken'])

            self.database_directive(username, full_name)
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

    def login_handler(self):
        """
        :return: Whether the user exists in the auth configurations or whether they are new users
        :rtype Bool
        """
        try:
            self.auth.sign_in_with_email_and_password(self.email, self.password)
            return True
        except HTTPError:
            return False

    @staticmethod
    def reset_password(email):
        """
        Reset user password on request
        :param email: User email to reset password
        :return:
        """
        # send password reset email
        FirebaseAuth.fire_nodes()["fire_auth"].send_password_reset_email(email=email)
        pass

    def database_directive(self, username, full_name):
        """
        Adds the user to the database with the following params
        :param username: the username generated from the user email
        :param full_name: full name of the user
        :return: no return type here
        """

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

        self.conn.put(url='/users', name=username, data={
            'firstName': first_name,
            'lastName': last_name,
            'email': self.email,
            'userName': username,
            'phoneNumber': self.phone_no
        }, headers={'print': 'pretty'})
