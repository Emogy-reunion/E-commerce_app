from flask import Blueprint, jsonify, flash, url_for, render_template, redirect
from flask_login import login_required, current_user
from model import Sneakers, db, Images, Cart, CartItems
from form import QuantityForm, SizeForm


cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/add_to_cart/<int:sneaker_id>', methods=['POST'])
@login_required
def add_to_cart(sneaker_id):
    '''
    this route adds an item to cart
    '''

    # extract the shoe size from the selected sizes
    form = SizeForm(request.form)

    size = int(form.size.data)

    user_id = current_user.id

    # fetch the product from the database
    sneaker = db.session.get(Sneakers, sneaker_id)

    if not sneaker:
        '''
        if the product doesn't exist
        '''
        return jsonify({'error': 'Item not found!'})

    
    # retrieve the cart to see if it exists
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        '''
        if cart doesn't exist, create it
        '''
        try:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Item not added to cart. Try again!'})

    # check if the product already exists in the cart
    cart_item = CartItems.query.filter_by(sneaker_id=sneaker_id).first()

    if cart_item:
        '''
        if the product exists increase it's quantity
        '''
        try:
            cart_item.quantity += 1
            cart_item.subtotal = sneaker.price * cart_item.quantity
            db.session.commit()
            return jsonify({'success': 'Successfully added to cart'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Item not added to cart. Try again!'})
    else:
        '''
        if the product doesn't exist, create it
        '''
        try:
            new_item = CartItems(
                    card_id=cart.id,
                    sneaker_id=sneaker_id,
                    size=size,
                    quantity=1,
                    subtotal=sneaker.price
                    )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'success': 'Successfully added to cart'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Item not added to cart. Try again!'})

@cart_bp.route('/view_cart')
@login_required
def view_cart():
    '''
    retrieves the user cart items
    '''

    # render form to allow users to select quantity
    form = QuantityForm()

    user_id = current_user.id

    # query the cart together with its items and the relevant sneaker
    cart = Cart.query.options(joinedload(Cart.items).joinedload(CartItems.item).joinedload(Sneakers.images)).filter_by(user_id=user_id).first()

    if not cart or not cart.items:
        '''
        check if the user has a cart
            - if cart in None it means the cart is not available
        also checks if the cart has items
            - if the cart.items is empty the user has not added any items to the cart
        '''
        return render_template('cart.html', cart=None)

    # calculate the total price of items in the cart
    total_price = sum(item.subtotal for item in cart.items)
    
    return render_template('cart.html', cart=cart, form=form, total_price=total_price)

@cart_bp.route('/update_cart/<int:sneaker_id>', methods=['POST'])
@login_required
def update_cart(sneaker_id):
    '''
    updates the quantity and subtotal fields of the items table
    '''
    user_id = current_user.id

    # retrieves the quantity of an item
    form = QuantityForm(request.form)
    quantity = int(form.quantity.data)

    cart_item = CartItems.query.options(joinedload(CartItems.item)).filter_by(sneaker_id=sneaker_id).first()

    # Check if the cart item exists
    if not cart_item:
        return jsonify({'error': 'Cart item not found'})

    if quantity > 0:
        try:
            cart_item.quantity = quantity
            cart_item.subtotal = cart_item.item.price * cart_item.quantity
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Quantity not updated!'})

        # query the cart together with its items and the relevant sneaker
        cart = Cart.query.options(joinedload(Cart.items).joinedload(CartItem.item)).filter_by(user_id=user_id).first()

        # calculate the total price of items in the cart
        total_price = sum(sneaker.subtotal for sneaker in cart.items)

        return jsonify({'subtotal': cart_item.subtotal, 'total_price': total_price})
    else:
        return({'error': 'Item cannot be less than 0'})


@cart_bp.route('/remove_from_cart/<int:sneaker_id>', methods=['DELETE'])
@login_required
def remove_from_cart(sneaker_id):
    '''
    removes an item from the cart
    '''
    user_id = current_user.id

    cart_item = CartItems.query.options(joinedload(CartItems.item)).filter_by(sneaker_id=sneaker_id).first()

    # Check if the cart item exists
    if not cart_item:
        return jsonify({'error': 'Cart item not found'})

    try:
        db.session.delete(cart_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Item not removed!'})

    cart = Cart.query.options(joinedload(Cart.items).joinedload(CartItem.item)).filter_by(user_id=user_id).first()

    # If the cart is empty, return a total price of 0
    if not cart or not cart.items:
        return jsonify({'total_price': 0})

    # recalculate the total price of items in the cart
    total_price = sum(sneaker.subtotal for sneaker in cart.items)
    return jsonify({'total_price': total_price})

