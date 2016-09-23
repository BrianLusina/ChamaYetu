from flask import Blueprint, request, render_template, g,flash, session,redirect, url_for

# import password encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

# import module forms
from app.mod_auth.forms import LoginForm

# import module models
from app.mod_auth.models import  User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

