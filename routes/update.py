'''
This module creates routes to update profile info and uploads
'''
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from model import Users, db, Sneakers, Orders
from form import UpdateUpload, UpdateOrderStatus
from flask_login import login_required
from utils.role import role_required


edit = Blueprint('edit', __name__)

@edit.route('/update_product/<int:product_id>', methods=['GET', 'PATCH'])
@login_required
@role_required('admin')
def update_product(product_id):
    '''
    this route allows admin's to edit uploads
    '''
    sneaker = db.session.get(Sneakers, product_id)

    if sneaker is None:
        return jsonify({"error": "Sneaker not found"})

    form = UpdateUpload()

    if request.method == 'PATCH':

        form = UpdateUpload(request.form)
        if form.validate_on_submit():
            '''
            checks if the form fields are valid
            '''
            name = form.name.data.lower()
            price = float(form.price.data)
            description = form.description.data
            brand = form.brand.data.lower()
            gender = form.gender.data

            try:

                # update fields if they are different
                if name and name != sneaker.name:
                    sneaker.name = name

                if price and price != sneaker.price:
                    sneaker.price = price

                if description and description != sneaker.description:
                    sneaker.description = description

                if brand and brand != sneaker.brand:
                    sneaker.brand = brand

                if gender and gender != sneaker.gender:
                    sneaker.gender = gender

                db.session.commit()
                return jsonify({'success': 'Successfully updated!'})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured. Try again!'})
        else:
            return jsonify({'errors': form.errors})
    return render_template('update_upload.html', form=form, sneaker=sneaker)

@edit.route('/update_order_status/<int:order_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def update_order_status(order_id):
    """
    This route allows the admin to update the order status.
    It renders a page with a SelectField for the order status, which the admin can update.
    """
    order = db.session.get(Orders, order_id)

    if order is None:
        flash("Order not found.", "danger")
        return redirect(url_for('order.admin_orders_view'))

    form = UpdateOrderStatus()

    if form.validate_on_submit():
        try:
            order.status = form.status.data
            db.session.commit()
            flash("Order status updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            flash("Failed to update order status.", "danger")
        return redirect(url_for('order.admin_orders_view'))

    return render_template('update_orders.html', order=order, form=form)
