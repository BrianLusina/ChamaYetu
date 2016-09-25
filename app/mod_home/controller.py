from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/
mod_home = Blueprint('home', __name__, url_prefix='/')


@mod_home.route('/')
@mod_home.route('index/')
def index():
    """
    :return: Render template for home page
    """
    return render_template("home_page/index.html")


# contact us page
@mod_home.route('contact/')
def contact():
    return render_template("home_page/contact.html")


# about us page
@mod_home.route('about/')
def about():
    return render_template("home_page/about.html")
