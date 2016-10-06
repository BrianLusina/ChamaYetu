from flask import Blueprint, request, render_template, \
    g, flash, session, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker
from wtforms import validators
from app.models import User, Data_Base, engine
from firebase import firebase
from .form import SuggProject
import datetime



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


# global var
count = 0
# add milestone
@mod_dashboard.route('/milestones',methods=['GET','POST'])
def add_milestone():
#     form = AddMile()
#
#     if form.validate_on_submit():
#         global count
#         count +=
#
#         putData={'date':form.date.data,'projectname:form.title.data'}
#         firebase.put('/suggestProject' ,'project' +str(count),putData )
#         return render_template('user_dashboard/dashboard.html')

    return render_template('user_dashboard/milestone.html')

#suggest project

@mod_dashboard.route('/project',methods=['GET','POST'])
def sugg_project():
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_suggestedproj = current_app.config.get('FIREBASE_SUGGESTEDPROJ_NODE')
    firebase_con = firebase.FirebaseApplication(firebase_base_url ,None)

    form = SuggProject()

    if request.method == 'POST' and form.validate:
        # create access to count var
        global count

        # increase value of by one everytime method runs
        count += 1

        # data to be added to firebase
        putData = {'date': form.date.data , 'projectname':form.title.data}
        firebase_con.put('/suggestProject', name='projectname' + str(count),data= putData, headers={'print','pretty'})

        return render_template('user_dashboard/dashboard.html',form=form)

    else:

        return render_template('user_dashboard/project.html')