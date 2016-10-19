from flask import Blueprint, request, render_template, \
    g, flash, session, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker
from app.models import User, Data_Base, engine
from firebase import firebase

from .form import SuggProject , AddMile

from pprint import pprint



# Create session and connect to DB
Data_Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define the blueprint: 'dashboard', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/<username>')
def dashboard(username):
    """
    :param username: the user name of the logged in user that will be appended to the url
    Fetch the data from the chamas node
    :return: return the dashboard template
    """
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_conn = firebase.FirebaseApplication(firebase_base_url, None)
    firebase_chama_node = current_app.config.get('FIREBASE_CHAMA_NODE')
    firebase_statements_node = current_app.config.get('FIREBASE_STATEMENTS_NODE')
    firebase_members_node = current_app.config.get('FIREBASE_MEMBERS_NODE')
    firebase_users_node = current_app.config.get('FIREBASE_USERS_NODE')




    # welcome our amazing user
    flash("Welcome back " + username)

    # query the user's chama (boda in this case)
    user_chamas = firebase_conn.get(firebase_users_node+"/"+username+"/chamaGroups/boda", None)

    # connect to that chama to get specific details
    chama_details = firebase_conn.get(firebase_chama_node+"/boda", None)
    chama_statement = firebase_conn.get(firebase_statements_node+"/boda", None)
    pprint(chama_details)

    return render_template('user_dashboard/dashboard.html', username=username,
                           chama_details=chama_details, chama_statement=chama_statement, scheme='https')


# global var
count = 0
# add milestone
@mod_dashboard.route('/milestones',methods=['GET','POST'])
def add_milestone():
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_suggestedproj = current_app.config.get('FIREBASE_MILESTONE_NODE')
    firebase_con = firebase.FirebaseApplication(firebase_base_url, None)

    form = AddMile()

    if request.method == 'POST':
        global count
        count +=1

        putData={'mileDate':form.date.data,'mileName':form.title.data}
        firebase_con.put('/milestones/boda', name='mile'+ str(count),data=putData )

        return render_template('user_dashboard/dashboard.html')

    return render_template('user_dashboard/milestone.html')

#suggest project

@mod_dashboard.route('/project',methods=['GET','POST'])
def sugg_project():
    firebase_base_url = current_app.config.get('FIREBASE_DB_CONN')
    firebase_suggestedproj = current_app.config.get('FIREBASE_PROJ_NODE')
    firebase_con = firebase.FirebaseApplication(firebase_base_url ,None)

    form = SuggProject()

    if request.method == 'POST':
        # create access to count var
        global count

        # increase value of by one everytime method runs
        count +=1

        # data to be added to firebase

        Data = {'projDate': form.date.data ,'projName':form.title.data}
        # projData = {'projectname':form.title.data}
        firebase_con.put('/projects/boda', name='proj'+ str(count),data=Data )

        return render_template('user_dashboard/dashboard.html',form=form)

    else:

        return render_template('user_dashboard/project.html')

@mod_dashboard.route('/calendar')
def calendar():
    return render_template("user_dashboard/calendar.html")