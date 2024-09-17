'''
This module contains routes that handle uploads and retrieval
'''
from flask import Blueprint, jsonify, render_template, current_app, request, send_from_directory
from form import UploadForm, SizeForm
from model import db, Sneakers, Images
from utils.allowed import allowed_file
from flask_login import login_required, current_user
from utils.role import role_required
from werkzeug.utils import secure_filename
import os
from sqlalchemy.orm import joinedload

post = Blueprint('post', __name__)

@post.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def upload():

    form = UploadForm()

    if request.method == 'POST':
        form = UploadForm(request.form)

        if form.validate_on_submit():
            '''
            checks if the form fields are valid
            '''
            name = form.name.data.lower()
            price = float(form.price.data)
            description = form.description.data
            brand = form.brand.data.lower()
            gender = form.gender.data

            if "files" not in request.files:
                '''
                check if the request has a file part
                If no file part it means user didn't select file
                '''
                return jsonify({'error': 'Please make sure you select files for upload!'})

            files = request.files.getlist('files')

            if not files:
                return jsonify({'error': 'You did not select any files!'})

            try:
                sneaker = Sneakers(name=name, price=price, description=description,
                                   user_id=current_user.id, brand=brand, gender=gender)
                db.session.add(sneaker)
                db.session.commit()

                uploads = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)

                        # save the file to the folder
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                        # save the filename to the database
                        image = Images(filename=filename, sneaker_id=sneaker.id)
                        db.session.add(image)
                        uploads.append(filename)
                    else:
                        db.session.rollback()
                        return jsonify({"error": 'File extension not allowed!'})

                db.session.commit()
                if uploads:
                    return jsonify({'success': 'Uploaded successfully!'})
                else:
                    return jsonify({'error': "Failed to upload"})

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": 'An unexpected error occured. Please try again!'})
        else:
            return jsonify({"errors": form.errors})

    return render_template('upload.html', form=form)

@post.route('/uploads', methods=['GET'])
@login_required
@role_required('admin')
def uploads():
    '''
    retrieve the uploads
    it renders the uploads page where admins can edit or delete uploads
    '''
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # prepare the table with eager loading of images
    results = Sneakers.query.options(joinedload(Sneakers.images)).order_by(Sneakers.id.desc())

    # paginate the results
    sneakers = results.paginate(page=page, per_page=per_page)
    return render_template('uploads.html', sneakers=sneakers)

@post.route('/send_image/<filename>')
def send_image(filename):
    '''
    retrieves images from the upload folder and sends them to the frontend
    '''

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@post.route('/upload_details/<int:sneaker_id>')
@login_required
@role_required('admin')
def upload_details(sneaker_id):
    '''
    renders page to display upload details
    '''
    sneaker = Sneakers.query.options(joinedload(Sneakers.images)).filter(Sneakers.id == sneaker_id).first()
    return render_template('upload_details.html', sneaker=sneaker)

@post.route('/men')
@login_required
def men():
    '''
    fetch all men products and render them together with the men.html
    '''
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    results = Sneakers.query.filter(Sneakers.gender == 'men').options(joinedload(Sneakers.images)).order_by(Sneakers.id.desc())
    sneakers = results.paginate(page=page, per_page=per_page)
    return render_template('men.html', sneakers=sneakers)

@post.route('/women')
@login_required
def women():
    '''
    fetch all products whose gender is women and render them together with the women.html page
    '''

    page = request.args.get('page', 1, type=int)
    per_page = 12

    results = Sneakers.query.filter(Sneakers.gender == 'women').options(joinedload(Sneakers.images)).order_by(Sneakers.id.desc())
    sneakers = results.paginate(page=page, per_page=per_page)
    return render_template('women.html', sneakers=sneakers)

@post.route('/unisex')
@login_required
def unisex():
    '''
    fetch gender neutral products and render them
    '''

    page = request.args.get('page', 1, type=int)
    per_page = 12

    results = Sneakers.query.filter(Sneakers.gender == 'unisex').options(joinedload(Sneakers.images)).order_by(Sneakers.id.desc())
    sneakers = results.paginate(page=page, per_page=per_page)
    return render_template('unisex.html', sneakers=sneakers)

@post.route('/product_details/<int:product_id>')
@login_required
def product_details(product_id):
    '''
    renders details about the products
    '''
    form = SizeForm()

    sneaker = Sneakers.query.options(joinedload(Sneakers.images)).filter(sneaker.id == sneaker_id).first()
    return render_template('product_details.html', sneaker=sneaker, form=form)

@post.route('/collections')
def collections():
    '''
    fetch gender neutral products and render them
    '''

    page = request.args.get('page', 1, type=int)
    per_page = 12

    results = Sneakers.query.options(joinedload(Sneakers.images)).order_by(Sneakers.id.desc())
    sneakers = results.paginate(page=page, per_page=per_page)
    return render_template('collections.html', sneakers=sneakers)

@post.route('/guest_product_details/<int:product_id>')
def guest_product_details(product_id):
    '''
    renders details about the products
    '''
    form = SizeForm()

    sneaker = Sneakers.query.options(joinedload(Sneakers.images)).filter(sneaker.id == sneaker_id).first()
    return render_template('guest_product_details.html', sneaker=sneaker, form=form)
