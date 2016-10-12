# Define the application directory
import os
import pyrebase
import json

# Statement for enabling the development environment
DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}


class Service:
    # store the json file in a variable
    __json_service = open("ChamaYetu-service.json", "r")
    # enter the file, load it into a variable and close the file
    with __json_service as data_file:
        chamayetu_service = json.load(data_file)

    def __init__(self):
        pass

    _private_key_pkcs8_pem = chamayetu_service["private_key"]
    service_account_email = chamayetu_service["client_email"]


FIREBASE_DB_CONN = "https://chamayetu-ddca4.firebaseio.com/"
FIREBASE_USERS_NODE = '/users'
FIREBASE_CHAMA_NODE = '/chamas'
FIREBASE_STATEMENTS_NODE = '/statements'
FIREBASE_MEMBERS_NODE = '/members'
FIREBASE_WEB_KEY = "AIzaSyAfNGG37gtrI09dy1nkpLt6ppX_NSgzM70"
FIREBASE_SUGGESTEDPROJ_NODE = "/suggestProject"

config = {
    "apiKey": FIREBASE_WEB_KEY,
    "authDomain": "chamayetu-ddca4.firebaseapp.com",
    "databaseURL": FIREBASE_DB_CONN,
    "storageBucket": "chamayetu-ddca4.appspot.com",
    "messagingSenderId": "128820725100",
    "serviceAccountEmail": Service
}

FIREBASE_CONFIG = pyrebase.initialize_app(config)

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
