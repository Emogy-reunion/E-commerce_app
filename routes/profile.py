'''
this routes render and return user profiles
'''
from flask import Blueprint
from utils.role import role_required
from model import Users, db
from flask_login import current_user, login_required


profile = Blueprint('profile', __name__)


@profile.route('/admin_profile')
@login_required
@role_required('admin')
def admin_profile():
    '''
    renders the admin profile template with admin's data
    '''
    admin = db.session.get(Users, current_user.id)
    return render_template('admin_profile.html', admin=admin)

@profile.route('/guest_profile')
@login_required
def guest_profile():
    '''
    renders the guest's profile page
    '''
    guest = db.session.get(Users, current_user.id)
    return render_template('guest_profile.html', guest=guest)
