'''
This module creates routes to update profile info and uploads
'''
from flask import Blueprint
from model import Users, db
from form import UpdateUpload


edit = Blueprint('edit', __name__)

@edit.route('/update_product/<int:product_id>', methods=['GET', 'PUT'])
@login_required
@role_required('admin')
def update_product(product_id):
    '''
    this route allows admin's to edit uploads
    '''
    sneaker = db.session.get(Sneakers, product_id)
    form = UpdateUpload()
