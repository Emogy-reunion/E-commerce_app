'''
This model contains routes that work on the order
'''
from flask import Blueprint
from model import db, Users, Sneakers, Cart, CartItems, Order, OrderItems
from form import CheckoutForm
from flask_login import login_required, current_user


order = Blueprint('order', __name__)

@order.route('place_order', methods=['GET', 'POST'])
@login_required
def place_holder():
    '''
    if the request is GET, it renders the checkout page
    If the request id POST it places the order and initiates payment process
    '''

    total_amount = response.json.get('total_amount')
    user_id = current_user.id
    form = CheckoutForm()

    cart = Cart.query.options(joinedload(Cart.items).joinedload

