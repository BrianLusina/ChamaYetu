from flask import Blueprint, request, render_template, g, flash, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/dashboard/')
def dashboard():
    return render_template('user_dashboard/dashboard.html')
