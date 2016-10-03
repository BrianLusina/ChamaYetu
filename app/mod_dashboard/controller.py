from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine, ChamaGroup, Statement
from datetime import datetime

# Create session and connect to DB
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/dashboard/')
def dashboard():
    # query chama by id
    # todo: add logic for querying chama total amount as per the users login(chama logged in)
    chamas = db_session.query(ChamaGroup).filter_by(id=2)
    # time the data was queried
    date = datetime.now()
    print(chamas)

    statement = db_session.query(Statement).filter_by(chama_id='chama_group.id')
    print (statement)

    return render_template('user_dashboard/dashboard.html', chamas=chamas, date=date, statement=statement)

@mod_dashboard.route('/milestone/')
def add_milestone():
        new_mile = ChamaGroup(milestone = request.form['milestones'])

        session.add(new_mile)
        session.commit()

        return  render_template(url_for('user_dashboard/milestone.html'), new_mile=new_mile)


