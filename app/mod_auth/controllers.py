from app.models import Data_Base, engine
import hashlib
from sqlalchemy.orm import sessionmaker
from requests import HTTPError
from app.mod_auth import FirebaseAuth
import re
import datetime

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


class Auth(FirebaseAuth):
    """
    Class that handles the authentication variables with Firebase
    firebase_auth gets the configuration dictionary that will be used for authenticating the user
    firebase_db_url contains the database url to Firebase
    firebase_conn connects to the database
    firebase_database connects to the database url, enabling access to the database nodes
    """
    __headers = {'print': "pretty"}

    def __init__(self, email, password, phone_no=None):
        """
        :param email: email the user enters in the form
        :param password: password entered by the user
        """
        super(Auth, self).__init__()
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.username = re.split('@', self.email)[0]

    def register_user(self, full_name):
        # Hash that Password
        sha1 = hashlib.sha1()
        sha1.update(self.password)
        password = sha1.hexdigest()

        # create a user with email and password, check if the user email already exists
        try:
            auth = self.firebase_auth
            user = auth.create_user_with_email_and_password(self.email, password)
            auth.send_email_verification(user['idToken'])

            self.database_directive(self.username, full_name)
            return True
        except HTTPError:
            # if the email already exists, return false to display an error in the view
            return False

    def register_chama(self, chama_name, chama_members, bank_name, bank_account):
        chama_name_node_key = chama_name.lower()
        date = datetime.date.today().strftime("%B-%d-%Y")
        # check the database for a similar chama name
        if self.firebase_database.child(chama_name_node_key).get().key() is None:
            self.firebase_app.put(url=self.firebase_chama_node, name=chama_name_node_key, data={
                "accountNumber": bank_account,
                "bankName": bank_name,
                "dateCreated": date,
                "members": chama_members,
                "name": chama_name,
                "nextMeetingTime": "",
                "totalAmount": 0,
                "venue": "",
                "milestoneDate": "",
                "roles": {
                    "chairperson": self.username,
                }
            }, headers=self.__headers)
            return True
        else:
            return False

    def login_user(self):
        try:
            self.firebase_auth.sign_in_with_email_and_password(self.email, self.password)
            return True
        except HTTPError:
            return False

    def reset_password(self, email):
        self.firebase_auth.send_password_reset_email(email=email)

    def database_directive(self, username, full_name):

        first_name, last_name = full_name.split(" ")[0], full_name.split(" ")[1]

        self.firebase_app.put(url='/users', name=username, data={
            'firstName': first_name,
            'lastName': last_name,
            'email': self.email,
            'userName': username,
            'phoneNumber': int(self.phone_no)
        }, headers=self.__headers)
