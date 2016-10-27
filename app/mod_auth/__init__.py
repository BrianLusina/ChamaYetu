from flask import current_app
from firebase import firebase


class FirebaseAuth(object):
    """
    Class to handle connection to Firebase configuration variables
    """

    def __init__(self):
        pass

    @staticmethod
    def fire_auth():
        return current_app.config.get('FIREBASE_CONFIG').auth()

    @staticmethod
    def fire_db_url():
        return current_app.config.get('FIREBASE_DB_CONN')

    @staticmethod
    def fire_conn():
        return firebase.FirebaseApplication(FirebaseAuth.fire_db_url(), None)

    @staticmethod
    def fire_database():
        return FirebaseAuth.fire_auth().database()

    @staticmethod
    def fire_nodes():
        return {
            "firebase_users_node": current_app.config.get('FIREBASE_USERS_NODE'),
            "firebase_web_key": current_app.config.get("FIREBASE_WEB_KEY"),
            "firebase_secret": current_app.config.get("FIREBASE_WEB_KEY")
        }
