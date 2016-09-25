from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/
mod_home = Blueprint('home', __name__, url_prefix='/')


@mod_home.route('/')
def index():
    """
    :return: Render template for home page
    """
    return render_template("home_page/index.html")

