
from flask import Flask,Blueprint,render_template


# def blueprint
mod_calendar = Blueprint('calendar ',__name__,url_prefix="/")


app = Flask(__name__)

@mod_calendar.route('/calendar')
def calendar():
    return render_template("calendar/calendar.html")