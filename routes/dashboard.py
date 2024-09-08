'''
renders the dashboards according to user authentication and authorization
'''
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from utils.role import role_required


dash = Blueprint('dash', __name__)

@dash.route('/')
def index():
    '''
    Renders logged out users dashboard
    '''
    return render_template('index.html')

@dash.route('/guest_dashboard')
@login_required
def guest_dashboard():
    '''
    Renders the logged in users dashboard
    if user has admin privileges, they are redirected to the admin dash
    '''
    if current_user.role == 'admin':
        '''
        checks if the current user has admin privileges
        if true they are redirected to an admin's dashboard
        '''
        return redirect(url_for('dash.admin_dashboard'))
    return render_template('guest.html')

@dash.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    '''
    Renders the admin dashboard
    '''
    return render_template('admin.html')

