from flask_wtf import RecaptchaField, Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


# Define Login form
class LoginForm(Form):
    email = StringField("Email Address", [Email(), DataRequired(message="Forgot your email address?")])
    password = PasswordField("Password", [DataRequired(message="Must provide a password")])

