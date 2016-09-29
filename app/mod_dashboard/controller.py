
from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for, app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine,ChamaGroup
from datetime import  datetime



# Create session and connect to DB
engine = create_engine('sqlite:///app.db')
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()



# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')




@mod_dashboard.route('/dashboard/')
def dashboard():
    #query chama by id
    #todo: add logic for querying chama total amount as per the users login(chama logged in)
    chamas = db_session.query(ChamaGroup).filter_by(id=2)
    #time the data was queried
    date = datetime.now()
    print(chamas)

    # for chama in chamas:
    #     print chama.name
    #     print  chama.total_amount

    return render_template('user_dashboard/dashboard.html',chamas=chamas, date=date)



@mod_dashboard.route('/dashboard/')
def statement():
    #query chama for past
    statement =db_session.query(statement).filter_by(id = chama_group.id)






