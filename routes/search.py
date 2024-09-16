'''
contains routes that handle database searching
'''
from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from utils.role import role_required
from model import Sneakers, Images
from form import SearchForm
from sqlalchemy.orm import joinedload


find = Blueprint('find', __name__)

@find.route('/admin_search_template', methods=['GET'])
@login_required
@role_required('admin')
def admin_search_template():
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

    sneakers = query.options(joinedload(Sneakers.images)).all()

    results = []
    
    for sneaker in sneakers:
        '''
        loop through the sneakers to extract individual properties
        '''
        results.append({
            'id': sneaker.id,
            'name': sneaker.name,
            'price': sneaker.price,
            'filename': sneaker.images[0].filename
            })
    if results:
        return jsonify({'data': results})
    else:
        return jsonify({'message': 'No collection available!'})

@find.route('/member_search_template')
@login_required
def member_search_template():
    '''
    render the authenticated users search form
    '''
    form = SearchForm()
    return render_template('member_search.html', form=form)

@find.route('/member_search')
@login_required
def member_search():
    '''
    allows users to filter products based on certain conditions
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

    sneakers = query.options(joinedload(Sneakers.images)).all()

    results = []

    for sneaker in sneakers:
        '''
        loop through the sneakers to extract individual properties
        '''
        results.append({
            'id': sneaker.id,
            'name': sneaker.name,
            'price': sneaker.price,
            'filename': sneaker.images[0].filename
            })
        
    if results:
        return jsonify({'data': results})
    else:
        return jsonify({'message': 'No collection available!'})

@find.route('/guest_search_template')
def guest_search_template():
    '''
    render the authenticated users search form
    '''
    form = SearchForm()
    return render_template('guest_search.html', form=form)

@find.route('/guest_search')
def guest_search():
    '''
    allows users to filter products based on certain conditions
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

    sneakers = query.options(joinedload(Sneakers.images)).all()

    results = []

    for sneaker in sneakers:
        '''
        loop through the sneakers to extract individual properties
        '''
        results.append({
            'id': sneaker.id,
            'name': sneaker.name,
            'price': sneaker.price,
            'filename': sneaker.images[0].filename
            })

    if results:
        return jsonify({'data': results})
    else:
        return jsonify({'message': 'No collection available!'})
