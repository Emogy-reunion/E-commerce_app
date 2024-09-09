'''
Handles property deletion: profiles, uploads
'''
from flask import Blueprint, jsonify
from model import db, Users, Sneakers
from utils.role import role_required
from flask_login import login_required


clear = Blueprint('clear', __name__)

@clear.route('/delete_post/<int:sneaker_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_post(sneaker_id):
    '''
    deletes a post from the database and it's related objects
    '''
    sneaker = db.session.get(Sneakers, sneaker_id)
    
    if sneaker is None:
        return jsonify({'error': 'Product not found!'})

    try:
        db.session.delete(sneaker)
        return jsonify({'success': 'Successfully deleted!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occured. Please try deleting again!'})

