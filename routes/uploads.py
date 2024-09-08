'''
This module handle uploading collections and retrieving them
'''
from flask import Blueprint
from utils.role import role_required


post = Blueprint('post', __name__)

@post.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def upload():

