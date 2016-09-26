from flask_wtf import RecaptchaField, Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


# Define Login form
class LoginForm(Form):
    email = StringField("Email Address", [Email(), DataRequired(message="Forgot your email address?")])
    password = PasswordField("Password", [DataRequired(message="Must provide a password")])

#def register form

class RegisterForm(Form):
	email = StringField(
		'email', validators =[DataRequired(),Email(message=None), Length(min = 6 ,max=40)]

		)

	password = PasswordField('password', validators = [DataRequired[],Length(min = 6,max=25)])

	confirm = PasswordField('repeat password',validators=[DataRequired(),EqualTo('password',message='Password must match')])
