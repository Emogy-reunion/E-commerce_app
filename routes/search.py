'''
contains routes that handle database searching
'''
from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from routes.utils import role_required
from model import Sneakers
from form import SearchForm


find = Blueprint('find', __name__)

@find.route('/admin_template', methods=['GET'])
@login_required
@role_required('admin')
def admin_template():
    '''
    this route renders the admin search page
    '''
    form = SearchForm()
    return render_template('admin_search.html', form=form)

@find.route('/admin_search', methods=['GET'])
@login_required
@role_required('admin')
def admin_search():
    '''
    this route handles admin search and filtering
    '''
    name = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    gender = request.args.get('gender')
    brand = request.args.get('brand')
    
    # build the base query
    query = Sneakers.query

    if name:
        query = query.filter(Sneakers.name.ilike(f"%{name}%"))
    
    if min_price:
        query = query.filter(Sneakers.price >= float(min_price))

    if max_price:
        query = query.filter(Sneakers.price <= float(max_price))

    if gender:
        query = query.filter(Sneakers.gender.ilike(f"%{gender}%"))

    if brand:
        query = query.filter(Sneakers.gender.ilike(f"%{brand}%"))

    sneakers = query.all()

    results = []
    
    for sneaker in sneakers:
        '''
        loop through the sneakers to extract individual properties
        '''
        results.append({
            'name': sneaker.name,
            'price': sneaker.price,
            'description': sneaker.description,
            'gender': sneaker.gender,
            'brand': sneaker.brand,
            'filename': [image.filename for image in sneaker.images] if upload.images else None
            })

    if results:
        return jsonify({'message': 'No collection available!'})
    else:
        return jsonify({'data': results})

