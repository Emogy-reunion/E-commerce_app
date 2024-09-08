'''
This module contains routes that handle uploads and retrieval
'''
from flask import Blueprint, jsonify, render_template, current_app, request
from form import UploadForm
from model import db, Sneakers, Images
from utils.allowed import allowed_file
from flask_login import login_required, current_user
from utils.role import role_required
from werkzeug.utils import secure_filename
import os


post = Blueprint('post', __name__)

@post.route('/upload', methods=['GET', 'POST'])
@loginrequired
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
                sneaker = Sneakers(name=name, price=price, description=description, user_id=current_user.id)
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
                        db.session.commit()
                        uploads.append(filename)

                        if uploads:
                            return jsonify({'success': 'Uploaded successfully!'})
                        else:
                            return jsonify({'error': "Failed to upload"})
                    else:
                        return jsonify({"error": 'File extension not allowed!'})
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": 'An unexpected error occured. Please try again!'})
        else:
            return jsonify({"errors": form.errors})

    return render_template('upload.html', form=form)
