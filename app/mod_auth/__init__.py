from flask import current_app
from firebase import firebase


class FirebaseAuth(object):
    """
    Class to handle connection to Firebase configuration variables
    """

    def __init__(self):
        self.firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')
        self.firebase_chama_node = current_app.config.get('FIREBASE_CHAMA_NODE')
        self.firebase_auth = current_app.config.get('FIREBASE_CONFIG').auth()
        self.firebase_db_url = current_app.config.get('FIREBASE_DB_CONN')
        self.firebase_app = firebase.FirebaseApplication(self.firebase_db_url, None)
        self.firebase_database = current_app.config.get('FIREBASE_CONFIG').database()

    def fire_credentials(self):
        return {
            "firebase_web_key": current_app.config.get("FIREBASE_WEB_KEY"),
            "firebase_secret": current_app.config.get("FIREBASE_WEB_KEY"),
        }
