from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine,ChamaGroup


# Create session and connect to DB
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()



# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

#establish connection to db


@mod_dashboard.route('/dashboard/')
def dashboard():
    chama = db_session.query(ChamaGroup).all()


    return render_template('user_dashboard/dashboard.html',chama=chama)







