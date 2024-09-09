'''
This module creates routes to update profile info and uploads
'''
from flask import Blueprint, render_template, request, jsonify
from model import Users, db, Sneakers
from form import UpdateUpload
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




