from flask_wtf import Form
from datetime import datetime
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class AddMile(Form):


    pass
class SuggProject(Form):

    date = StringField('date', default=datetime.now())
    title = StringField('title', validators=[DataRequired()])

