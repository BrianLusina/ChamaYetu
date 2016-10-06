from flask import Blueprint, request, render_template, \
    g, flash, session, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/')
def dashboard():
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    return render_template('user_dashboard/dashboard.html')