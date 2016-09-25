from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine

# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/dashboard/')
def dashboard():
    return render_template('user_dashboard/dashboard.html')
