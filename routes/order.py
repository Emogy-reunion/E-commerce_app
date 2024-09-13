'''
This model contains routes that work on the order
'''
from flask import Blueprint, render_template, jsonify
from utils.role import role_required
from model import db, Users, Sneakers, Cart, CartItems, Orders, OrderItems
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

    cart = Cart.query.options(
            joinedload(Cart.items).
            joinedload(Cart.cart_user).
            joinedload(CartItems.item).
            joinedload(Sneaker.images)
            ).filter_by(user_id=user_id).first()

    if not cart or not cart.items:
        '''
        ensures the cart exists and is not empty
        '''
        return jsonify({'error': 'The cart is empty!'})

    if request.method == 'GET':
        return render_template('checkout.html', cart=cart, total_amount=total_amount, form=form)
    else:

        form = CheckoutForm(request.form)

        if form.validate_on_submit():
            '''
            ensures that the form data is valid
            '''
            phone_number = form.phone_number.data
            shipping_address = form.shipping_address.data

            try:
                # create the order
                order = Order(
                        user_id=user_id,
                        total_amount=total_amount,
                        status='not_paid',
                        shipping_address=shipping_address,
                        phone_number=phone_number
                        )
                db.session.add(order)
                db.session.commit()

                for item in cart.items:
                    '''
                    iterate over the items in the cart, add each of them to the orderItems table
                    '''
                    order_item = OrderItems(
                            quantity=item.quantity,
                            size=item.size,
                            subtotal=item.subtotal,
                            order_id=order.id,
                            sneaker_id=item.sneaker_id
                            )
                    db.session.add()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured!'})
        else:
            return jsonify({'errors': form.errors})
        
        # handle payments for successfully place orders

@order.route('/view_orders')
@login_required
def view_orders():
    '''
    This method retrieves and returns the user's orders.
    If there are no orders, it returns None.
    '''
    user_id = current_user.id

    # retrieve the user's orders
    orders = Orders.query.options(
            joinedload(Orders.user).
            joinedload(Orders.ordered_items).
            joinedload(OrderedItems.ordered_item)
            ).filter_by(user_id=user_id).all()

    if not orders:
        return render_template('orders.html', orders=None)
    else:
        return render_template('orders.html', orders=orders)

@order.route('admin_orders_view')
@login_required
@role_required('admin')
def admin_orders_view():
    '''
    This method retrieves all orders in the database
    If there are no orders, it returns None
    '''
    orders = Orders.query.options(
            joinedload(Orders.user).
            joinedload(Orders.ordered_items).
            joinedload(OrderedItems.ordered_item)
            ).all()

    if not orders:
        return render_template('orders.html', orders=None)
    else:
        return render_template('orders.html', orders=orders)
