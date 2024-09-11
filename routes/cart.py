from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from model import Sneakers, db, Images, Cart, CartItems
from form import QuantityForm


cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    '''
    this route adds an item to cart
    '''
    user_id = current_user.id

    # fetch the product from the database
    product = db.session.get(Sneakers, product_id)

    if not product:
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
    cart_item = CartItems.query.filter_by(product_id=product_id).first()

    if cart_item:
        '''
        if the product exists increase it's quantity
        '''
        try:
            cart_item.quantity += 1
            cart_item.subtotal = product.price * cart_item.quantity
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
                    product_id=product_id,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=1,
                    subtotal=product.price
                    )
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'success': 'Successfully added to cart'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Item not added to cart. Try again!'})

