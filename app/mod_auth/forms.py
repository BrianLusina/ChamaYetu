from flask_wtf import RecaptchaField, Form
from wtforms import StringField, PasswordField, BooleanField, DecimalField, DateTimeField, SubmitField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Regexp, Length

# Define Login form
from app.models import User


class LoginForm(Form):
    email = StringField("Email Address", [Email(), DataRequired(message="Forgot your email address?")])
    password = PasswordField("Password", [DataRequired(message="Must provide a password")])


class TreasurerForm(Form):
    membersname = StringField("MembersName")
    amountcontributed = DecimalField("Amount Deposited")
    amountwithdrawn = DecimalField("Amount Withdrawn")
    date = DateTimeField("Date And Time")
    submit = SubmitField("Send to Chama")


def validate_username(field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already in use.')


def validate_email(field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    Chama = StringField('Chama Name', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Chamanames must have only letters, '
                                              'numbers, dots or underscores')])
    phonenumber = IntegerField('Password', validators=[
        DataRequired()])
    role = SelectField("select a field", choices=[('Member'), ('Chairman'), ('Treasurer' ), ('Secretary')])
    submit = SubmitField('Register')
