'''
This model contains routes that work on the order
routes to place order, render the templates
'''
from flask import Blueprint, render_template, jsonify, request
from utils.role import role_required
from model import db, Users, Sneakers, Cart, CartItems, Orders, OrderItems, Images
from form import CheckoutForm
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from utils.pay import get_access_token, generate_password, initiate_stk_push


order = Blueprint('order', __name__)

@order.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    '''
    if the request is GET, it renders the checkout page
    If the request id POST it places the order and initiates payment process
    '''
    user_id = current_user.id

    form = CheckoutForm()

    cart = Cart.query.options(
    joinedload(Cart.items).joinedload(CartItems.item).joinedload(Sneakers.images),
    joinedload(Cart.user)
    ).filter_by(user_id=user_id).first()

    if not cart or not cart.items:
        '''
        ensures the cart exists and is not empty
        '''
        return jsonify({'error': 'The cart is empty!'})

    if request.method == 'GET':
        subtotal = request.args.get('total_amount', type=float)
        shipping_fee = float(150)
        total = subtotal + shipping_fee
        return render_template('checkout.html', cart=cart, subtotal=subtotal, total=total, form=form)
    else:

        form = CheckoutForm(request.form)

        if form.validate_on_submit():
            '''
            ensures that the form data is valid
            '''
            phone_number = form.phone_number.data
            shipping_address = form.shipping_address.data.lower()
            total_value = float(request.form.get('total_value'))

            try:
                # create the order
                order = Orders(
                        user_id=user_id,
                        total_amount=total_value,
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
                    db.session.add(order_item)
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured!'})
            
            db.session.commit()

            my_cart = Cart.query.filter_by(user_id=user_id).first()

            # handle payments for successfully place orders
            print(phone_number)
            response = initiate_stk_push(amount=total_value, phone_number=phone_number) 
            print(response)

            if response.get('status') == 'success':
                try:
                    CartItems.query.filter_by(cart_id=my_cart.id).delete()
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': 'An unexpected error occured!'})
                return jsonify({'success': 'Payment initiated successfully.'})
            else:
                return jsonify({'error': 'Payment initiation failed.'})
        else:
            return jsonify({'errors': form.errors})

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
            joinedload(Orders.ordered_items).
            joinedload(OrderItems.ordered_item), joinedload(Orders.user)
            ).filter_by(user_id=user_id).order_by(Orders.id.desc()).all()

    if not orders:
        return render_template('orders.html', orders=None)
    else:
        return render_template('orders.html', orders=orders)

@order.route('/admin_orders_view')
@login_required
@role_required('admin')
def admin_orders_view():
    '''
    This method retrieves all orders in the database
    If there are no orders, it returns None
    '''
    orders = Orders.query.options(
            joinedload(Orders.ordered_items).
            joinedload(OrderItems.ordered_item), joinedload(Orders.user)
            ).order_by(Orders.id.desc()).all()

    if not orders:
        return render_template('admin_orders.html', orders=None)
    else:
        return render_template('admin_orders.html', orders=orders)

@order.route('/callback', methods=['POST'])
def callback():
    # Safaricom sends the confirmation details in JSON format
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request, JSON data missing"}), 400

    try:
        # Extracting the transaction details from the callback payload
        result_code = data['Body']['stkCallback']['ResultCode']
        result_desc = data['Body']['stkCallback']['ResultDesc']
        mpesa_receipt = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        phone_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']

        # Check if the transaction was successful
        if result_code == 0:
            order = Orders.query.filter_by(phone_number=phone_number).first()
            if order:
                order.status = 'Paid'
                db.session.commit()
                return jsonify({"message": "Order payment status updated to Paid"}), 200
            else:
                return jsonify({"error": "Order not found for this phone number"}), 404
        else:
            return jsonify({"message": f"Transaction failed: {result_desc}"}), 400

    except KeyError as e:
        return jsonify({"error": f"Missing expected field {str(e)} in the callback"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
